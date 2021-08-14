import time
import pychromecast
import socket

device = "Miss Google"

def play_track(track, ext):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    path = "http://" + ip_address + ":8000/Music/" + track
    mc.play_media(path, content_type = "video/" + ext)
    mc.block_until_active()
    mc.pause()
    time.sleep(1)
    
print("Casting to", device)
chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[device])
cast = chromecasts[0]
mc = cast.media_controller
cast.wait()
pychromecast.discovery.stop_discovery(browser)

play_track("Blank.mp3","mp3")

time.sleep(1)

