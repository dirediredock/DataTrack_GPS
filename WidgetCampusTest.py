from random import randint
import location
import sched
import time
import ui
import ctypes

# Haptics

c = ctypes.CDLL(None)

def vibrate():
    p = c.AudioServicesPlaySystemSound
    p.restype = None
    p.argtypes = [ctypes.c_int32]
    vibrate_id = 1106
    p(vibrate_id)

# GPS Functions

file_name = (
    "Stream_"
    + time.strftime("%Y_%m_%d_%H_%M_%S_")
    + str(randint(0, 9999)).zfill(4)
    + ".txt"
)
count = 0
gps_time_gap = 1
scheduler = sched.scheduler(time.time, time.sleep)
active_event = False
active_event_idx = 0
is_running = False
current_squirrel_color = ''
current_squirrel_odor = ''

def get_location():
    location.start_updates()
    loc = location.get_location()
    location.stop_updates()
    if loc:
        lat = loc["latitude"]
        lon = loc["longitude"]
        alt = loc["altitude"]
        ts = loc["timestamp"]
        hac = loc["horizontal_accuracy"]
        vac = loc["vertical_accuracy"]
        if active_event:
            vibrate()
        truncated_data = {
            "obs_idx": active_event_idx if active_event else 0,
            "ts": int(ts),
            "lat": round(lat, 7),
            "lon": round(lon, 7),
            "alt": round(alt, 3),
            "hac": round(hac, 3),
            "vac": round(vac, 3),
        }
        return str(truncated_data)
    else:
        return '{"ts": "NaN"}'
        
def write_location():
    if is_running:
        global count
        count += 1
        datum_raw = get_location()
        datum = datum_raw.replace("'",'"')
        with open("./saved_data/Quant" + file_name, "a") as f:
            f.write(datum.replace(
                "{",'{"idx": '+str(count)+", "))
            f.write("\n")
            f.close()
            
def write_event():
    with open('./saved_data/Qual'+ file_name, 'a') as f:
        f.write('{"obs_idx": ' + str(active_event_idx) + ', "type": "' + current_squirrel_color + '", "rating": "' + current_squirrel_odor + '"}')
        f.write("\n")
        f.close()
            
            
# File Display

def display_file_contents():
    if is_running:
        try:
            with open('./saved_data/Quant' + file_name, "r") as f:
                lines = f.readlines()
                if len(lines) >= 9:
                    quantView.text = '\n'.join(lines[-9:])
                else:
                    quantView.text = '\n'.join(lines)
                f.close()
            with open('./saved_data/Qual' + file_name, "r") as f:
                lines = f.readlines()
                if len(lines) >= 8:
                    qualView.text = '\n'.join(lines[-8:])
                else:
                    qualView.text = '\n'.join(lines)
                f.close()
        except:
            return

def run():
    scheduler.enter(gps_time_gap, 1, run)
    if is_running:
        write_location()
        display_file_contents()

# UI Config

def color_change(sender):
    global current_squirrel_color
    current_squirrel_color = sender.segments[sender.selected_index]
    
def odor_change(sender):
    global current_squirrel_odor
    current_squirrel_odor = sender.segments[sender.selected_index]
    
def submit_survey(sender):
    sender.superview.close()
    write_event()

surveyView = ui.load_view('Widget')

def handle_session(sender):
    global is_running
    is_running = not is_running
    sender.title = 'Pause' if is_running else 'Resume'
    event_button.enabled = is_running

def handle_event(sender):
    global active_event
    global active_event_idx
    active_event = not active_event
    if active_event:
        surveyView.present('popover', hide_title_bar=True)
        active_event_idx += 1
        sender.title = 'Submit!'
        session_button.enabled = False
    else:
        sender.title = 'Widget'
        current_squirrel_color = ''
        session_button.enabled = True
    
def find(list, matcher):
    for x in list:
        if matcher(x):
            return x
    return None

rootView = ui.load_view('MainView')
quantView = find(rootView.subviews, lambda x : x.name == 'quantView')
qualView = find(rootView.subviews, lambda x : x.name == 'qualView')
session_button = find(rootView.subviews, lambda x : x.name == 'sessionButton')
event_button = find(rootView.subviews, lambda x : x.name == 'eventButton')
event_button.enabled = False

rootView.present('fullscreen')

run()
scheduler.run()
