#!/usr/bin/env python
from __future__ import print_function
from soco import SoCo
from time import sleep
import time
import nfc
from _common import get_api
import tweetpony

def touched(tag):
    currentHour = time.localtime()[3]
    isNight = 0
    if currentHour < daytimeRange[0] or currentHour > daytimeRange[1]: # is it nighttime?
        isNight = 1
        
    tag_uid = str(tag.uid).encode("hex")  # get the UID of the touched tag

    #Look up the song to play and set the right volume
    if tag_uid in songs:
        print("Tag touched: #" + songs[tag_uid][0] + ", UID: " + tag_uid)
        print ("  Song: " + songs[tag_uid][1])
        if isNight:
            vol = int(round(nightVol * songs[tag_uid][2],0))
            sonos.volume = vol
            print ("  Nighttime song volume is " + str(vol))
        else:
            vol = int(round(dayVol * songs[tag_uid][2],0))
            sonos.volume = vol
            print ("  Daytime song volume is " + str(vol))
        
        sonos.play_uri(songs[tag_uid][4])  # play the song
        print ("  Playing...")

        # if the song has a time offset, skip to it.
        if songs[tag_uid][3]:   
                sonos.seek(songs[tag_uid][3])
                print ("  Skipped to " + songs[tag_uid][3])                  
    else:
        print ("  No record for tag UID: " + tag_uid)

    # Tweet the song
    tweet = songs[tag_uid][1] + time.strftime("\n%b %d %Y %H:%M:%S", time.localtime()) 
    try:
        status = twitter_api.update_status(status = tweet)
    except tweetpony.APIError as err:
        print ("  Tweet failed: ", err.description)
    else:
        print ("  Tweet sent")

    return True


# Constants
dayVol = 50  # default daytime volume
nightVol = 25 # default nighttime volume
daytimeRange = [7,17] # daytime is 7:00a to 5:59p
sonos_ip = '10.0.1.98'
url = 'x-sonos-http:_t%3a%3a17790141.mp3?sid=11&flags=32'  #default url
time_offset = ''  #time offset (to skip song intros)

songs = {
# block_number, title, vol %, time_offset ('HH:MM:SS'), url
'04436522c52980' : ['1','Diamonds on the Soles of Her Shoes',1,time_offset,'x-sonos-http:_t%3a%3a17790141.mp3?sid=11&flags=32'],
'04926422c52980' : ['2','To Love Somebody',1,time_offset,'x-sonos-http:_t%3a%3a2995780.mp3?sid=11&flags=32'],
'04dd3a22c52980' : ['3','One Cup of Coffee',0.8,time_offset,'x-sonos-http:_t%3a%3a39299573.mp3?sid=11&flags=32'],
'04b56322c52980' : ['4','Best for Last',0.8,'00:00:36','x-sonos-http:_t%3a%3a2893061.mp3?sid=11&flags=32'],
'04e46422c52980' : ['5','We are Going to Be Friends',0.8,time_offset,'x-sonos-http:_t%3a%3a2807102%3a%3aa%3a%3a231444.mp3?sid=11&flags=32'],
'048b6322c52980' : ['6','The Mighty Quinn',0.8,time_offset,'x-sonos-http:_t%3a%3a2568562.mp3?sid=11&flags=32'],
'04216522c52980' : ['7','Baa Baa Black Sheep',1,time_offset,'x-sonos-http:_t%3a%3a5425710%3a%3aa%3a%3a441322.mp3?sid=11&flags=32'],
'04df3a22c52980' : ['8','In the Beginning',0.75,'00:00:13','x-sonos-http:_t%3a%3a5407313.mp3?sid=11&flags=32'],
'04cb6422c52980' : ['9','Honey Pie',1.3,'00:00:41','x-sonos-http:_t%3a%3a3053744.mp3?sid=11&flags=32'],
'04436422c52980' : ['10','Pata Pata',0.9,'00:00:09','x-sonos-http:_t%3a%3a1163595.mp3?sid=11&flags=32'],
'049e6422c52980' : ['11','Flight of the Bumblebee',1,time_offset,'x-sonos-http:_t%3a%3a8805968.mp3?sid=11&flags=32'],
'04536422c52980' : ['12','Babi Achchee',0.8,time_offset,'x-sonos-http:_t%3a%3a43013728.mp3?sid=11&flags=32'],
}

# Twitter setup
print("Connecting to Twitter...")
twitter_api = get_api()
if twitter_api:
    print ("Connected to Twitter")
else:
    print ("Twitter connection error")
print ("")


# Sonos setup
print("Connecting to Sonos...")
sonos = SoCo(sonos_ip)
print ("Connected to Sonos: " + sonos.player_name)

# Use this section to get the URIs of new songs we want to add
info = sonos.get_current_track_info()
print("Currently Playing: " + info['title'])
print("URI: " + info['uri'])
print("---")
print("") 


print("Setting up reader...")
reader = nfc.ContactlessFrontend('tty:AMA0:pn53x')
print(reader)
print("Ready!")
print("")

while True:
    reader.connect(rdwr={'on-connect': touched})
    print("Tag released")
    sonos.stop()
    print ("Sonos stopped")
    print ("---")
    print ("")
    sleep(0.1);
