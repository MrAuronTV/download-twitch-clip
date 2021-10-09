#!/usr/bin/env python3
import pickle
import numpy
import requests
import json
import time
import datetime
import os
import sys
import urllib.request
import argparse


from pathlib import Path
from urllib import request
from urllib.error import HTTPError
from json import loads

d = datetime.datetime.utcnow()
d = d + datetime.timedelta(days=-30) # -30 = number day before today you want donwload
d = d.isoformat("T") + "Z"

name = "mraurontv" #streamer name
path = "{}/".format(name)

if os.path.exists(path)==False:
   os.mkdir(path)

basepath = '{}/'.format(name)

def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()

API_ENDPOINT = 'https://api.twitch.tv/helix/users?login={0}'.format(name)

#Create app https://dev.twitch.tv/console/apps
Client_ID = 'CLIENT_ID'
#Get twitch token https://id.twitch.tv/oauth2/authorize?client_id=CLIENT_APP_ID&redirect_uri=URI_APP&response_type=token
TOKEN = 'Bearer YOUR_TOKEN'
  
#data to be sent to api
head = {
"Authorization":  TOKEN,
'Client-ID' : Client_ID
}

#api call here
r = requests.get(url = API_ENDPOINT, headers = head)

ENDPOINT = 'https://api.twitch.tv/helix/clips?broadcaster_id={0}&started_at={1}'.format(loads(r.text)['data'][0]['id'],d)

c = requests.get(url = ENDPOINT, headers = head)

for clip in loads(c.text)['data']:
    clip_info = requests.get("https://api.twitch.tv/helix/clips?id=" + clip['id'], headers = head).json()
    thumb_url = clip_info['data'][0]['thumbnail_url']
    mp4_url = thumb_url.split("-preview",1)[0] + ".mp4"
    out_filename = clip['id'] + ".mp4"
    output_path = (basepath + out_filename)
    
    if os.path.exists('{}/{}'.format(name,clip['id']))==True:
       print('exist')
    else:
       urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
       open('{}/{}'.format(name,clip['id']), "x")