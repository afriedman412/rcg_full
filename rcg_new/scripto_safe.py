import pandas as pd
import numpy as np
import requests
import urllib
import urllib3
import certifi
import json
import re
from rcg_func_dj import pull_rc, pull_artists, artist_cycle, tally

import logging


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rcg_new.settings")
import django
django.setup()

from rcg_app.models import Gender, Groups

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


spot_id = os.environ['SPOT_ID']
spot_sec = os.environ['SPOT_SEC']

print('running rcg...')
rc = pull_rc(spot_id, spot_sec)
artists_unprocessed = pull_artists(rc)
artists_processed = artist_cycle(artists_unprocessed)
tally(artists_processed)
print('rcg done!')