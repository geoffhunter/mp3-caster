import sys
import time

import pychromecast

device = "Miss Google"

if len(sys.argv) > 1:
    args = ""
    for arg in range(1, len(sys.argv)):
#        print (str(sys.argv[arg]))
        args = args + " " + str(sys.argv[arg])
        args = args.lstrip()
else:
    args = "0"

vol = args.lower()

chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[device])
cast = chromecasts[0]
cast.wait()
pychromecast.discovery.stop_discovery(browser)

time.sleep(0.5)

current_vol = round(cast.status.volume_level,2)*10 
print ("Old vol:", current_vol)

if vol == "up":
    vol = current_vol + 1
if vol == "down":
    vol = current_vol - 1

if vol == "0":
    vol = 0
    
if vol < 0:
    vol = 0
if vol > 6:
    vol = 6
fvol = float(vol)
if fvol <= 6:
    cast.set_volume(fvol/10)
else:
    vol = current_vol
    print("Can't set that volume")

print ("New vol:", vol)
