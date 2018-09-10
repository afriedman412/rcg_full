import pandas as pd
import numpy as np
import requests
import urllib
import urllib3
import certifi
import json
import re
import unidecode
import datetime as datetime
from bs4 import BeautifulSoup

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# import Django models
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rcg_new.settings")
import django
django.setup()

from rcg_app.models import Gender, Groups, Weekly_Count

# prep 'http'
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

spot_id = '4263d6a900e94f1599974e3c90c28aa5'
spot_sec = '26333e019ca149a4b8f0f1633168dddd'

# reads the current Rap Caviar playlist using supplied ID and secret
# returns cleaned json of playlist
def pull_rc(spot_id, spot_sec, uri='spotify:user:spotify:playlist:37i9dQZF1DX0XUsuxWHRQd'):
	client_credentials_manager = SpotifyClientCredentials(spot_id, spot_sec)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	username = uri.split(':')[2]
	playlist_id = uri.split(':')[4]

	results = sp.user_playlist(username, playlist_id)
	rc_j = json.dumps(results, indent=4)
	rc_jd = (json.loads(rc_j))
	return rc_jd


# takes a string (ie an artist bio)
# counts number of gender-male and gender-female pronouns in the bio
# returns list of both counts ([M, F])
def pnoun_test(t):
	m_count = 0
	f_count = 0
	m = ['he', 'him', 'his', 'himself']
	f = ['she', 'her', 'hers', 'herself']
	for w in t.split():
		if w in m: 
			m_count += 1
		if w in f:
			f_count += 1
	return([m_count, f_count])


# returns a bio or None if none exists
# if group=True, returns list of group members (or None if no members listed)
def searchy(artist, group=False, test=True, rerun=False):
	if test:
		print(artist, group)

	# remove accents
	artist = unidecode.unidecode(artist)
	
	# execute search
	url = f'https://www.allmusic.com/search/artists/{"%20".join(artist.split())}'

	# make request
	r = http.request('GET', url)

	# if response is good, scrape biography
	if r.status == 200:
		if test:
			print('scraping...')
		soup = BeautifulSoup(r.data, 'lxml')
		try:
			link = soup.find('div', {'class':'name'}).find('a')['href']
		except AttributeError:
			if rerun:
				if test:
					print('rerun failed, returning dummy bio')
				return 'dummy bio'

			# re-runs 'searchy' with []() removed from artist to deal with typos
			if test:
				print('rerun')
			badchars_regex = re.compile('[\[\]\(\)]')
			artist_cleaned = badchars_regex.sub('', artist)
			searchy(artist_cleaned, group, test, rerun=True)
			return
		
		r2 = http.request('GET', (link + '/biography/'))
		if r2.status == 200:
			soup2 = BeautifulSoup(r2.data, 'lxml')
			
			# if group, pull group members instead of bio
			if test:
				print('finding group members...')
			if group:
				try:
					members = []
					for m in soup2.find('div', {'class':'group-members'}).find_all('a'):
						members.append(m.text.strip())
					return members
				
				# return NaN if no members
				except AttributeError:
					return None
			
			# else pull bio
			else:
				if test:
					print('finding bio...')
				try:
					return soup2.find('div', {'itemprop':'reviewBody'}).text

				# return NaN if no biography entry
				except AttributeError:
					return None


# takes an artist name and a pronoun count
# adds artist to Gender depending on count results
# if count != 2, raises an error
# pnoun count is (male, female), returns 'M' or 'F' depending on which is bigger
# returns 'X' if counts are equal
def write_gender(artist, pnoun_count):
	try:
		len(pnoun_count) == 2
	except TypeError:
		print('pronoun count error')
		return
	if pnoun_count[0] > pnoun_count[1]:
		gender = 'M'
	elif pnoun_count[1] > pnoun_count[0]:
		gender = 'F'
	else:
		gender = 'X'
	t = Gender(artist=artist, gender=gender)
	t.save()
	return


# returns the gender for an artist from Gender
def read_gender(artist):
	return Gender.objects.get(artist=artist).gender

# find gender, group status and members (if applicable) for unknown artist
def new_artist(artist):

	# check if group
	group_members = searchy(artist, group=True)

	# if group members found, add to Groups and set Gender to 'G'
	if group_members != None:
		write_group(artist, group_members)
		t = Gender(artist=artist, gender='G')
		t.save()
		return

	# if not group pull bio using 'searchy'
	# using bio to set Gender via 'pnoun_test' on bio
	else:
		bio = searchy(artist)
		if bio == None:
			t = Gender(artist=artist, gender='X')
			t.save()
			return

		else:
			pnoun_count = pnoun_test(bio)
			write_gender(artist, pnoun_count)
			return


# takes a group name and a list of members
# joins 'members' with '|' and adds entry to Groups
def write_group(group_name, members):
	g = Groups(group_name=group_name, members='|'.join(members))
	g.save()
	return


# takes a group_name
# pulls members from Groups
# splits on '|' and returns list of members
def read_group(group_name):
	return (Groups.objects.get(group_name=group_name).members).split('|')


# finds all artists associated with a track
# pulls group members and features
def process_track(artist, track_name):
	# initiate total_artists
	total_artists = [artist]

	# pull any features
	if 'feat.' in track_name:
		feat = re.findall('(?<=feat. ).*[^)]', track_name)
		for n in re.split('[,&]', feat[0]):
			total_artists.append(n.strip())
	elif 'ft.' in track_name:
		feat = re.findall('(?<=ft. ).*[^)]', track_name)
		for n in re.split('[,&]', feat[0]):
			total_artists.append(n.strip())

	# scan for groups
	total_artists_ungrouped = []
	for a in total_artists:
		if Gender.objects.filter(artist=a).exists():
			if Gender.objects.get(artist=a).gender == 'G':
				total_artists_ungrouped = total_artists_ungrouped + read_group(a)
			else:
				total_artists_ungrouped.append(a)
		else:
			total_artists_ungrouped.append(a)

	return total_artists_ungrouped


# takes a playlist in json form
# runs 'process_track' on all tracks
# returns un-processed list of artists
def pull_artists(playlist, test=False):
	total_artists = []
	for n in range(50):
		artist = playlist['tracks']['items'][n]['track']['artists'][0]['name']
		track = playlist['tracks']['items'][n]['track']['name']
		if test:
			print(len(total_artists))
		total_artists = total_artists + process_track(artist, track)
	return total_artists


# takes a list of artists
# for any unknown artists it finds, runs 'new_artist' then reruns 'artist_cycle'
# for any groups it finds, unpacks groups, makes new artist list with that instance of the group removed and members added
def artist_cycle(artists):
	for n in range(len(artists)):
		if Gender.objects.filter(artist=artists[n]).exists():
			gender = Gender.objects.get(artist=artists[n]).gender
		else:
			new_artist(artists[n])
			return artist_cycle(artists)

		if gender == 'G':
			members = read_group(artists[n])
			del artists[n]
			artists_extended = artists + members
			return artist_cycle(artists_extended)
		else:
			continue
	return artists

# takes the artists from 'artist_cycle'
# looks up all genders
# counts results
def tally(artists, week=None):
	df = pd.DataFrame(columns=['artist','gender'])
	for a in artists:
		if Gender.objects.filter(artist=a).exists():
			gender = Gender.objects.get(artist=a).gender
		else:
			gender = 'X'
		df = df.append({'artist':a, 'gender':gender}, ignore_index=True)
	M = df.gender.value_counts()['M']
	F = df.gender.value_counts()['F']
	X = df.gender.value_counts()['X']
	if week == None:
		d = datetime.datetime.today().strftime('%Y-%m-%d')
	else:
		d = week
	w = Weekly_Count(week=d, M=M, F=F, X=X)
	w.save()
	return