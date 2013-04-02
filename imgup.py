#!/usr/bin/env python2.7
# file: imgup.py

# simple anonymous photo upload to imgur (by default)
# returns the url for the image

import os
import requests
from argparse import ArgumentParser, FileType
def upload_sloth(image_name):
    post_url = 'https://api.imgur.com/3/image.json'
    client_id = # INSERT CLIENT ID
    image = open(image_name)
    res = requests.post(
        post_url,
        verify = False,
        params = {'type': 'file'},
        files  = {'image': image},
        headers= {'Authorization': "Client-ID " + client_id})
    j = res.json()

    if j['success']:
        url = 'http://imgur.com/' + j['data']['id']
        return url
    else:
        print 'status: {0}\nerror: {1}'.format(j['status'], j['data']['error'])
        sys.exit(1)
