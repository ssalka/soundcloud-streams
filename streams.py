import soundcloud
import webbrowser
import json
from datetime import datetime
from dateutil import parser, relativedelta
from inputs import *


# Set stream properties in inputs.py
stream = {'Title': title,
		  'Permalink': permalink,
		  'Sharing': 'public' if public else 'private'}


def connect(config):
	print 'Connecting to SoundCloud API...'
	return soundcloud.Client(**config)


def readfile(file):
	print 'Reading stream parameters...'
	file_type = str.split(file, '.')[1]
	if file_type == 'json':
		with open(file) as json_data:
			data = json.load(json_data)
			json_data.close()
		data['users'].sort(key=lambda name: name)
		if 'filters' not in data.keys():
			data['filters'] = {}
		if 'duration' not in data['filters'].keys():
			data['filters']['duration'] = {}
		return data['users'], data['filters']
	else:
		raise TypeError('Unsupported file type: %s' % file_type)


def new_playlist(name, share='public'):
	print 'Creating new playlist...'
	client.post('/playlists', playlist={'title': name,
										'genre': 'stream',
										'sharing': share})
	return client.get('/me/playlists', limit=1)[0]


def find_playlist(permalink):
	playlists = client.get('/me/playlists')
	for pl in playlists:
		if pl.permalink == permalink:
			global stream
			stream['Title'] = pl.title
			return pl
	if 'playlist' not in locals():
		print 'No playlist with the given permalink: \'%s\'' % permalink
		raise SystemExit


def increment(cutoff):
	new_date = parser.parse(cutoff) + relativedelta.relativedelta(seconds=+1)
	return new_date.strftime('%Y/%m/%d %H:%M:%S %z')


def setup_playlist(new, stream):
	if new:
		playlist = new_playlist(stream['Title'], stream['Sharing'])
		cutoff = None
	else:
		playlist = find_playlist(stream['Permalink'])
		cutoff = increment(playlist.tracks[0]['created_at'])
	return playlist, cutoff


def get_tracks(users, flt):
	print 'Checking for new tracks...'
	tracks = []
	date = flt['cutoff']
	for user in users:
		matches = client.get('/users/%s/tracks' % user,
							 duration=flt['duration'],
							 created_at=date)
		tracks.extend(matches)
	if not tracks:
		if new:
			print 'No tracks found - check your users and filters'
		else:
			print 'Playlist is already up-to-date!'
		raise SystemExit
	else:
		for track in tracks:
			track.post_date = parser.parse(track.created_at)
		tracks.sort(key=lambda t: t.post_date, reverse=True)
		limit = min(200, len(tracks))
		return tracks[:limit]


def write_description(users):
	with open('description.txt') as file:
		return file.readline().format('<br />@'.join(users),
									  datetime.now().strftime('%A, %B %d'))


def update(pl, tracks, body):
	print 'Updating your stream...'
	new_IDs = [track.id for track in tracks]
	n = len(new_IDs)
	m = pl.track_count
	if n < 200 and m > 0:
		limit = min(m, 200 - n + 1)
		old_IDs = [track['id'] for track in pl.tracks[:limit]]
		new_IDs.extend(old_IDs)
	post_IDs = map(lambda id: dict(id=id), new_IDs)
	client.put(pl.uri, playlist={'title': stream['Title'],
								 'tracks': post_IDs,
								 'description': body})


def success():
	action = 'created' if new else 'updated'
	print '\nYour stream "{}" has been {}!'.format(stream['Title'], action)
	if goto:
		webbrowser.open_new_tab(playlist.permalink_url)
	print '\nThank you for using soundcloud-streams'
	raise SystemExit


if __name__ == '__main__':
	client = connect(config)
	users, filters = readfile(params)
	playlist, filters['cutoff'] = setup_playlist(new, stream)
	tracks_to_add = get_tracks(users, filters)
	description = write_description(users)

	update(playlist, tracks_to_add, description)
	success()