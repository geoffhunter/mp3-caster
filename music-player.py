import time
import pychromecast
import socket
import os

device = "Miss Google"

def play_track(track, ext):
    if track != "Blank.mp3":
        print ("Playing track: " + track)

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    path = "http://" + ip_address + ":8000/Music/" + track
    mc.play_media(path, content_type = "video/" + ext)
    mc.block_until_active()
    mc.pause()
    time.sleep(1)
    
def play_next_track():
    dir = os.listdir(".\\Queue\\")
    filecount = len([name for name in os.listdir('.\\Queue\\')])
    if filecount > 0:
        fname = dir[0]
        ext = fname[27:]
        if ext == "txt":
            f = open(".\\Queue\\" + fname)
            lines = f.readlines()
            track = lines[0]
            ext = track[len(track)-3:]
            play_track(track, ext)
            f.close()
            os.remove(".\\Queue\\" + fname)

chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[device])
cast = chromecasts[0]
mc = cast.media_controller
cast.wait()
pychromecast.discovery.stop_discovery(browser)

play_track("Blank.mp3","mp3")

while True:
    mc.update_status()
    try:
        remaining = (mc.status.duration - mc.status.current_time)
        remaining = int(remaining)
    except:
        play_next_track()

    if mc.status.player_is_paused:
        if remaining == 0 or remaining == 1:
            play_next_track()
                
    elif mc.status.player_is_idle:
        play_next_track()
    
    time.sleep(1)

