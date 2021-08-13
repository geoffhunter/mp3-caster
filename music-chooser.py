import speech_recognition as sr
import pyttsx3
from pyttsx3.drivers import sapi5
import sys
import time
import datetime
import os
import glob

voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
INITIAL_TALKING = True
INITIAL_USING_MIC = False
MUSIC_DIR = "C:/Users/geoff/OneDrive/Music"

class tracks_class(object):
    def __init__(self, artist=None, album=None, folder=None, filename=None):
        self.artist = artist
        self.album = album
        self.folder = folder
        self.filename = filename

tracks = []

def add_track(artist, album, folder, filename):
    tracks.append(tracks_class(artist, album, folder, filename))

def add_track_to_queue(track):
    if track != "Blank.mp3":
        print ("Adding track: " + track)
    d = str(datetime.datetime.now())
    fname = d + ".txt"
    fname = fname.replace(":",".")
    f = open(".\\Queue\\" + fname, "w")
    f.write(track)
    f.close()
    time.sleep(0.001)

def clear_tracks_from_queue():
    fileList = glob.glob(".\\Queue\\20*.txt")
    for filePath in fileList:
        os.remove(filePath)
   
def get_tracks(walk_dir):
    tracks.clear()  

    for dirpath, dirs, files in os.walk(walk_dir):  
        for filename in files:
            if filename.endswith(".mp3") or filename.endswith(".m4a") or filename.endswith(".wma"):
                folder = dirpath[len(walk_dir)+1:]
                slpos = folder.find("\\")
                artist_album = folder[slpos+1:]
                slpos = artist_album.find("\\")
                artist = artist_album[0:slpos]
                album = artist_album[slpos+1:]
                add_track (artist, album, folder, filename)
                print(dirpath)                

def respond_to_command(w):
    global talking
    global using_mic
#    print ("Responding to:", w)
#    print (w[0:4])
    if w[0:4] == "play":
        key = w[5:]
        if key != "":
            say("Playing " + key)
            search_tracks(key)
    elif w == "reset":
        clear_tracks_from_queue()
    elif w == "talk to me":
        talking = True
        say ("OK")
    elif w == "be quiet" or w == "shut up":
        talking = False
    elif w == "use mike":
        using_mic = True
    elif w == "mike off":
        using_mic = False
    elif w != "":
        print ("Don't understand")
        
def get_command():
    if using_mic:
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        w = ""
        s = ""
        response = get_command_from_mic(recognizer, microphone)
        if response["transcription"]:
            s = response["transcription"]
            print("You said:",s)

#        if response["error"]:
#            print("{}".format(response["error"]))
    else:
        s = input("Enter command: ")
        
    w = s.lower()
    return (w)

def get_command_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening ...")
        audio = recognizer.listen(source)
        print("Got something")

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Didn't understand"

    return response

def say(text):
    if talking:
        print("Saying", text)
        engine = pyttsx3.init('sapi5')
        engine.setProperty('voice', voice_id)
        engine.say(text)
        engine.runAndWait()

def search_tracks(w):
    found = False
    print ("Scanning library for:",w)
    for i in range(0, len(tracks)):
        artist = tracks[i].artist
        album = tracks[i].album
        folder = tracks[i].folder
        filename = tracks[i].filename
        if artist != None and album != None:
            if artist.lower() == w or album.lower() == w:
                found = True
                add_track_to_queue(folder + "\\" + filename)
    if not found:
        print ("No match for " + w)
        say ("No match for " + w)

get_tracks(MUSIC_DIR)

talking = INITIAL_TALKING

if len(sys.argv) > 1:
    args = ""
    for arg in range(1, len(sys.argv)):
        args = args + " " + str(sys.argv[arg])
        args = args.lstrip()
    search_tracks(args)
    sys.exit()
        
using_mic = INITIAL_USING_MIC
command = ""
while True:
    command = get_command()
    if command == "stop" or command == "quit":
        say("Stopping")
        add_track_to_queue("Blank.mp3")
        break
    respond_to_command(command)
