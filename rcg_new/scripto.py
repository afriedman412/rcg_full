import pandas as pd
import numpy as np
import requests
import webapp2
import urllib2
import urllib3
import certifi
import json
import re
import unidecode
import logging
from bs4 import BeautifulSoup

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from rcg_func_dj import pull_rc, pull_artists, artist_cycle, tally


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rcg_new.settings")
import django
django.setup()
from rcg_app.models import Gender, Groups

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
spot_id = os.environ['SPOT_ID']
spot_sec = os.environ['SPOT_SEC']

class update_dbs(webapp2.RequestHandler):
    def get(self):

    	
        self.response.headers["Content-Type"] = "text/html"
        # self.response.write('running rcg...')
        rc = pull_rc(spot_id, spot_sec)
        artists_unprocessed = pull_artists(rc)
        artists_processed = artist_cycle(artists_unprocessed)
        tally(artists_processed)
        self.response.write('rcg done!')


routes = [('/rcg_app/count', update_dbs)]
app = webapp2.WSGIApplication(routes, debug=True)