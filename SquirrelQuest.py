from random import randint
import location
import sched
import time
import ui

# GPS Functions

file_name = (
    "SquirrelQuest_"
    + time.strftime("%Y_%m_%d_%H_%M_%S_")
    + str(randint(0, 9999)).zfill(4)
    + ".txt"
)
count = 0
gps_time_gap = 1
scheduler = sched.scheduler()
active_event = False

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
        truncated_data = {
            "lat": round(lat, 5),
            "lon": round(lon, 5),
            "alt": round(alt, 3),
            "ts": int(ts),
            "hac": round(hac, 3),
            "vac": round(vac, 3),
            "sql": 1 if active_event else 0
        }
        return str(truncated_data)
    else:
        return '{"ts": "NaN"}'
        
def write_location():
    scheduler.enter(gps_time_gap, 1, write_location)
    global count
    count += 1
    datum_raw = get_location()
    datum = datum_raw.replace("'",'"')
    with open(file_name, "a") as f:
        f.write(datum.replace(
            "{",'{"idx": '+str(count)+", "))
        f.write("\n")
        f.close()

write_location()

# UI Config

def handle_switch(sender):
    global active_event
    active_event = sender.value
    
rootView = ui.load_view('Squirrel_UI')
textView = rootView.subviews[0]

rootView.present('fullscreen')

# File Display

def display_file_contents():
    scheduler.enter(gps_time_gap, 2, display_file_contents)
    with open(file_name, "r") as f:
        lines = f.readlines()
        if len(lines) >= 5:
            textView.text = '\n'.join(lines[-5:])
        else:
            textView.text = '\n'.join(lines)
        f.close()
        
display_file_contents()
scheduler.run()
