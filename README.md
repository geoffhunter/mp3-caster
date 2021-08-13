# mp3-caster

Utilities to cast locally stored MP3 files from a Windows computer to a Chromecast device, e.g. Google Home

Overview

These utilities allow the user to play their owned and locally stored MP3 files on a Chromecast device, without using the ad-based Youtube or 
subscription-based Youtube Premium services. 

MP3 files are organised in a 'Music' folder containing a separate folder for each artist and a separate folder within each artist for each album.

e.g. C:\Music\Bill Evans\Waltz for Debby\01 My Foolish Heart.mp3
				
In the above example, the directory containing the 'Music' folder is C:\\. The artist is 'Bill Evans', and the album is 'Waltz for Debby'. Track names 
may start with the track number to specify the play order.

The Music folder must contain an MP3 file called 'Blank.mp3' which is played by the Music Player when it needs to stop the Chromecast device playing.

The modules are:

http-server.bat	- This is a DOS batch file that launches an HTTP Server which is required to service requests from the Chromecast device. It first changes directory to the folder containing the 'Music' folder then runs Python with a command to run the http.server module.
			
music-player.exe - This is the Music Player. It connects to the Chromecast device, then loops, waiting for it to be idle, before sending it the location and name of the next MP3 file to be played. 

music-chooser.exe - This is the Music Chooser. It processes keyed or spoken commands to queue MP3 files for a specified artist or album. It responds to commands with a text response and a voice response if enabled. Initally it accepts commands from the keyboard. Voice command is a bit flakey and doesn't really work when something is already playing.
			
It recognises the following commands (not case-sensitive). 			
			
play		e.g. 'play bill evans' will queue all tracks where the artist is 'Bill Evans'. 'play waltz for debby' will queue all tracks where the album is 'Waltz for Debby'

talk to me - start voice responses

be quiet - stop voice responses

shut up	- stop voice responses

use mike - start accepting voice commands

mike off - stop accepting voice commands

reset - clear the queue

stop - exit Music Chooser

quit - exit Music Chooser

The queue of music to be played is in a folder named 'Queue' below the current one (where the Music Player runs). The queue consists of 1 or more text 
files named with the date and time the file was created, e.g. 2021-05-25 15.09.29.570212.txt. Each file contains the location (within the 'Music' folder) 
and name of the MP3 file to be played, e.g. Bill Evans\Waltz for Debby\01 My Foolish Heart.mp3

Module details

http-server.bat

The HTTP Server starter. It assumes the 'Music' folder is in "C:/Users/geoff/OneDrive" and that python.exe is in 
"C:\Users\geoff\AppData\Local\Programs\Thonny". Change these if necessary. 

musicplayer.py

The Music Player module. This module initialises the connection to the Chromecast device, sends an instruction to play the blank MP3, then loops,
checking the status of the Chromecast device every second to see if it is playing something and if not, calls play_next_track. It assumes the 'Music'
folder is "C:/Users/geoff/OneDrive/Music". Change this if necessary. It also assumes the Chromecast device is called 'Miss Google'. Change this if 
necessary.

play_next_track checks if there are any files in the queue and if so, extracts the MP3 file name and location from the first file, calls play_track with
this information, then deletes the file from the queue.

play_track sends an instruction to play the MP3 file, to the Chromecast device.

musicchooser.py

The Music Chooser module. This module calls get_tracks to get the details of all tracks in the 'Music' folder. It then loops, calling get_command to get 
input from the user. If the user issues command 'stop' or 'quit', it exits the loop. Otherwise it calls respond_to_command.

get_tracks gets a list of all MP3 files below the 'Music' folder and populates a 'tracks' list with the artist, album, folder and filename of each track.

get_command either calls get_speech_from_mic or gets input from the keyboard, depending on the current input method, and returns the command.

get_speech_from_mic listens for input from the microphone and returns the spoken command.

respond_to_command examines the command. If the command starts with 'play' it extracts the artist/album from the command and calls search_tracks to get 
the details. If the command is 'reset' in calls clear_tracks_from_queue. If the command is 'talk to me' it enables voice responses.If the command is 'be 
quiet' or 'shut up' it disables voice responses. If the command is 'use mike' it enables voice input. If the command is 'mike off' it disables voice 
input.

clear_tracks_from_queue deletes all files in the 'Queue' folder.

search_tracks scans the 'tracks' list for the specified album/artist and where there is a match it calls add_track_to_queue

add_track_to_queue creates a file named with the current date/time in the 'Queue' folder and writes the MP3 file location and name to it.
