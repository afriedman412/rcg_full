from django.shortcuts import render
import pandas as pd
import numpy as np
import requests
import urllib3
import certifi
import logging
import json
import re
import os
from rcg_func_dj import pull_rc, pull_artists, artist_cycle, tally

from .models import Weekly_Count, Gender, Groups
import random

def index(request):
	latest_count = Weekly_Count.objects.order_by('-date_created')[0]
	rando = random.randint(1,10)
	context = {'latest_count': latest_count, 'rando':rando}
	return render(request, 'rcg_app/index.html', context)

def go(request):
	latest_count = Weekly_Count.objects.order_by('-date_created')[0]

	http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
	spot_id = os.environ['SPOT_ID']
	spot_sec = os.environ['SPOT_SEC']

	rc = pull_rc(spot_id, spot_sec)
	artists_unprocessed = pull_artists(rc)
	artists_processed = artist_cycle(artists_unprocessed)
	tally(artists_processed)

	latest_count_prime = Weekly_Count.objects.order_by('-date_created')[0]

	context = {'lc':latest_count, 'lc_prime':latest_count_prime}
	return render(request, 'rcg_app/go.html', context)
