#!/usr/bin/python3

import os
import pafy
import ffmpeg
from tqdm import tqdm
from spotipy import Spotify
from bs4 import BeautifulSoup
from dwytsongs.utils import *
from dwytsongs import exceptions

stock_output = "%s/Songs" % os.getcwd()
stock_recursive_download = False
stock_not_interface = False
stock_zip = False

spo = Spotify(
	auth = generate_token()
)

def download(directory, name, recursive_download, not_interface, datas):
	song = "{} - {}".format(datas['music'], datas['artist'])

	body = request(
		"https://www.youtube.com/results?search_query=%s" % song.replace("#", "")
	).text

	links = BeautifulSoup(body, "html.parser").find_all("a")

	for link in links:
		href = link.get("href")

		if len(href) == 20:
			down = href
			break

	out_yt = directory + down
	out = "%s.mp3" % name

	try:
		if pafy.new("https://www.youtube.com" + down).length > 800:
			raise exceptions.TrackNotFound("Track not found: " + song)
	except (OSError, NameError):
		raise exceptions.TrackNotFound("Error cannot get information about video")

	if os.path.isfile(out):
		if recursive_download:
			return out

		ans = input("Song already exist do you want to redownload it?(y or n): ")

		if not ans in ["Y", "y", "Yes", "YES"]:
			return out

	quiet = "-q"

	if not not_interface:
		quiet = ""
		print("Downloading: %s" % song)

	os.system(
		"youtube-dl %s https://www.youtube.com%s -f best -o '%s'"
		% (
			quiet,
			down,
			out_yt
		)
	)

	try:
		(
			ffmpeg
			.input(out_yt)
			.output(out)
			.run(
				quiet = not_interface,
				overwrite_output = True
			)
		)
	except KeyError:
		try:
			os.remove(out_yt)
		except FileNotFoundError:
			pass

		raise exceptions.TrackNotFound("Error while downloading: " + song)

	os.remove(out_yt)
	write_tags(out, datas)
	return out

def download_trackdee(
	URL,
	output = stock_output + "/",
	recursive_download = stock_recursive_download,
	not_interface = stock_not_interface
):
	datas = {}

	ids = (
		URL
		.split("?utm")[0]
		.split("/")[-1]
	)

	URL1 = "https://www.deezer.com/track/%s" % ids
	URL2 = "https://api.deezer.com/track/%s" % ids
	url = request(URL2, True).json()

	url1 = request(
		"http://api.deezer.com/album/%d" % url['album']['id'], True
	).json()

	image = url1['cover_xl']

	if not image:
		body = request(URL1).text

		image = (
			BeautifulSoup(body, "html.parser")
			.find("meta", property = "og:image")
			.get("content")
			.replace("500x500", "1200x1200")
		)

	image = request(
		image.replace("1000x1000", "1200x1200")
	).content

	if len(image) == 13:
		image = request("https://e-cdns-images.dzcdn.net/images/cover/1200x1200-000000-80-0-0.jpg").content

	datas['image'] = image
	datas['music'] = url['title']
	array = []

	for a in url['contributors']:
		if a['name'] != "":
			array.append(a['name'])

	array.append(
		url['artist']['name']
	)

	datas['artist'] = artist_sort(array)
	datas['album'] = url1['title']
	datas['tracknum'] = str(url['track_position'])
	datas['discnum'] = str(url['disk_number'])
	datas['year'] = url['release_date']
	datas['genre'] = []

	try:
		for a in url1['genres']['data']:
			datas['genre'].append(a['name'])
	except KeyError:
		pass

	datas['genre'] = " & ".join(datas['genre'])
	datas['ar_album'] = []

	for a in url1['contributors']:
		if a['role'] == "Main":
			datas['ar_album'].append(a['name'])

	datas['ar_album'] = " & ".join(datas['ar_album'])
	datas['label'] = url1['label']
	datas['bpm'] = str(url['bpm'])
	datas['gain'] = str(url['gain'])
	datas['duration'] = str(url['duration'])
	datas['isrc'] = url['isrc']
	album = var_excape(datas['album'])

	directory = (
		"%s%s %s/"
		% (
			output,
			album,
			url1['upc']
		)
	)

	check_dir(directory)

	name = (
		"%s%s CD %s TRACK %s"
		% (
			directory,
			album,
			datas['discnum'],
			datas['tracknum']
		)
	)

	out = download(
		directory, name,
		recursive_download, not_interface, datas
	)

	return out

def download_albumdee(
	URL,
	output = stock_output + "/",
	recursive_download = stock_recursive_download,
	not_interface = stock_not_interface,
	zips = stock_zip
):
	datas = {}
	detas = {}
	datas['music'] = []
	datas['artist'] = []
	datas['tracknum'] = []
	datas['discnum'] = []
	datas['bpm'] = []
	datas['gain'] = []
	datas['duration'] = []
	datas['isrc'] = []
	names = []
	array = []
	nams = []

	ids = (
		URL
		.split("?utm")[0]
		.split("/")[-1]
	)

	URL1 = "https://www.deezer.com/album/%s" % ids
	URL2 = "https://api.deezer.com/album/%s" % ids
	url = request(URL2, True).json()
	datas['album'] = url['title']
	datas['label'] = url['label']
	datas['year'] = url['release_date']
	image = url['cover_xl']

	if not image:
		URL = "https://www.deezer.com/album/%s" % ids
		body = request(URL).text

		image = (
			BeautifulSoup(body, "html.parser")
			.find("img", class_ = "img_main")
			.get("src")
			.replace("200x200", "1200x1200")
		)

	image = request(
		image.replace("1000x1000", "1200x1200")
	).content

	if len(image) == 13:
		image = request("https://e-cdns-images.dzcdn.net/images/cover/1200x1200-000000-80-0-0.jpg").content

	datas['image'] = image
	datas['genre'] = []

	try:
		for a in url['genres']['data']:
			datas['genre'].append(a['name'])
	except KeyError:
		pass

	datas['genre'] = " & ".join(datas['genre'])
	datas['ar_album'] = []

	for a in url['contributors']:
		if a['role'] == "Main":
			datas['ar_album'].append(a['name'])

	datas['ar_album'] = " & ".join(datas['ar_album'])
	album = var_excape(datas['album'])

	directory = (
		"%s%s %s/"
		% (
			output,
			album,
			url['upc']
		)
	)

	check_dir(directory)

	for a in url['tracks']['data']:
		del array[:]
		datas['music'].append(a['title'])

		ur = request(
			"https://api.deezer.com/track/%d" % a['id'], True
		).json()

		discnum = str(ur['disk_number'])
		tracknum = str(ur['track_position'])

		names.append(
			"%s%s CD %s TRACK %s"
			% (
				directory,
				album,
				discnum,
				tracknum
			)
		)

		datas['tracknum'].append(tracknum)
		datas['discnum'].append(discnum)

		datas['bpm'].append(
			str(ur['bpm'])
		)

		datas['gain'].append(
			str(ur['gain'])
		)

		datas['duration'].append(
			str(ur['duration'])
		)

		datas['isrc'].append(ur['isrc'])

		for a in ur['contributors']:
			if a['name'] != "":
				array.append(a['name'])

		array.append(
			ur['artist']['name']
		)

		datas['artist'].append(
			artist_sort(array)
		)

	detas['image'] = image
	detas['album'] = datas['album']
	detas['year'] = datas['year']
	detas['genre'] = datas['genre']
	detas['ar_album'] = datas['ar_album']
	detas['label'] = datas['label']

	for a in tqdm(
		range(
			len(names)
		), 
		disable = not_interface
	):
		detas['music'] = datas['music'][a]
		detas['artist'] = datas['artist'][a]
		detas['tracknum'] = datas['tracknum'][a]
		detas['discnum'] = datas['discnum'][a]
		detas['bpm'] = datas['bpm'][a]
		detas['gain'] = datas['gain'][a]
		detas['duration'] = datas['duration'][a]
		detas['isrc'] = datas['isrc'][a]
		song = "{} - {}".format(detas['music'], detas['artist'])

		try:
			nams.append(
				download(
					directory, names[a],
					recursive_download, not_interface, detas
				)
			)
		except exceptions.TrackNotFound:
			nams.append(names[a])
			print("Track not found: %s :(" % song)
			continue

	if zips:
		zip_name = "{}{}.zip".format(
			directory, directory.split("/")[-2] 
		)

		create_zip(zip_name, nams)
		return nams, zip_name

	return nams

def download_playlistdee(
	URL,
	output = stock_output + "/",
	recursive_download = stock_recursive_download,
	not_interface = stock_not_interface,
	zips = stock_zip
):
	array = []

	ids = (
		URL
		.split("?utm")[0]
		.split("/")[-1]
	)

	url = request(
		"https://api.deezer.com/playlist/%s" % ids, True
	).json()

	for a in url['tracks']['data']:
		try:
			array.append(
				download_trackdee(
					a['link'], output,
					recursive_download, not_interface
				)
			)
		except (exceptions.TrackNotFound, exceptions.NoDataApi):
			song = "{} - {}".format(a['title'], a['artist']['name'])
			print("Track not found: %s" % song)
			array.append(song)

	if zips:
		zip_name = "{}playlist {}.zip".format(output, ids)
		create_zip(zip_name, array)
		return array, zip_name

	return array

def download_trackspo(
	URL,
	output = stock_output + "/",
	recursive_download = stock_recursive_download,
	not_interface = stock_not_interface
):
	global spo

	datas = {}
	URL = URL.split("?")[0]

	try:
		url = spo.track(URL)
	except Exception as a:
		if not "The access token expired" in str(a):
			raise exceptions.InvalidLink("Invalid link ;)")

		spo = Spotify(
			generate_token()
		)

		url = spo.track(URL)

	URL1 = url['album']['external_urls']['spotify']

	try:
		url1 = spo.album(URL1)
	except Exception as a:
		if not "The access token expired" in str(a):
			raise exceptions.InvalidLink("Invalid link ;)")

		spo = Spotify(
			generate_token()
		)

		url1 = spo.album(URL1)

	datas['image'] = request(
		url1['images'][0]['url']
	).content

	datas['music'] = url['name']

	array = [
		a['name'] for a in url['artists']
	]

	datas['artist'] = ", ".join(array)
	datas['album'] = url1['name']
	datas['tracknum'] = str(url['track_number'])
	datas['discnum'] = str(url['disc_number'])
	datas['year'] = url1['release_date']
	datas['genre'] = " & ".join(url1['genres'])

	array = [
		a['name'] for a in url1['artists']
	]

	datas['ar_album'] = ", ".join(array)
	datas['label'] = url1['label']
	datas['bpm'] = ""
	datas['gain'] = "0"
	datas['duration'] = str(url['duration_ms'] * 1000)
	datas['isrc'] = url['external_ids']['isrc']
	album = var_excape(datas['album'])

	directory = (
		"%s%s %s/"
		% (
			output,
			album,
			url1['external_ids']['upc']
		)
	)

	check_dir(directory)

	name = (
		"%s%s CD %s TRACK %s"
		% (
			directory,
			album,
			datas['discnum'],
			datas['tracknum']
		)
	)

	out = download(
		directory, name,
		recursive_download, not_interface, datas
	)

	return out

def download_albumspo(
	URL,
	output = stock_output + "/",
	recursive_download = stock_recursive_download,
	not_interface = stock_not_interface,
	zips = stock_zip
):
	global spo

	datas = {}
	detas = {}
	datas['music'] = []
	datas['artist'] = []
	datas['tracknum'] = []
	datas['discnum'] = []
	datas['duration'] = []
	names = []
	nams = []

	try:
		url = spo.album(URL)
	except Exception as a:
		if not "The access token expired" in str(a):
			raise exceptions.InvalidLink("Invalid link ;)")

		spo = Spotify(
			generate_token()
		)

		url = spo.album(URL)

	detas['image'] = request(
		url['images'][0]['url']
	).content

	detas['album'] = url['name']
	detas['year'] = url['release_date']
	detas['genre'] = " & ".join(url['genres'])

	array = [
		a['name'] for a in url['artists']
	]

	detas['ar_album'] = ", ".join(array)
	detas['label'] = url['label']
	detas['bpm'] = ""
	detas['gain'] = "0"	
	detas['isrc'] = ""
	album = var_excape(detas['album'])

	directory = (
		"%s%s %s/"
		% (
			output,
			album,
			url['external_ids']['upc']
		)
	)

	check_dir(directory)
	tot = url['total_tracks']

	def lazy(a):
		datas['music'].append(a['name'])
		discnum = str(a['disc_number'])
		tracknum = str(a['track_number'])

		names.append(
			"%s%s CD %s TRACK %s"
			% (
				directory,
				album,
				discnum,
				tracknum
			)
		)

		datas['tracknum'].append(tracknum)
		datas['discnum'].append(discnum)

		datas['duration'].append(
			str(a['duration_ms'] * 1000)
		)

		array = [
			b['name'] for b in a['artists']
		]

		datas['artist'].append(
			", ".join(array)
		)

	for a in url['tracks']['items']:
		lazy(a)

	for a in range(tot // 50 - 1):
		try:
			url = spo.next(url['tracks'])
		except:
			spo = Spotify(
				generate_token()
			)

			url = spo.next(url['tracks'])

		for a in url['items']:
			lazy(a)

	for a in tqdm(
		range(
			len(names)
		), 
		disable = not_interface
	):
		detas['music'] = datas['music'][a]
		detas['artist'] = datas['artist'][a]
		detas['tracknum'] = datas['tracknum'][a]
		detas['discnum'] = datas['discnum'][a]
		detas['duration'] = datas['duration'][a]
		song = "{} - {}".format(detas['music'], detas['artist'])

		try:
			nams.append(
				download(
					directory, names[a],
					recursive_download, not_interface, detas
				)
			)
		except exceptions.TrackNotFound:
			nams.append(names[a])
			print("Track not found: %s :(" % song)
			continue

	if zips:
		zip_name = "{}{}.zip".format(
			directory, directory.split("/")[-2] 
		)

		create_zip(zip_name, nams)
		return nams, zip_name

	return nams

def download_playlistspo(
	URL,
	output = stock_output + "/",
	recursive_download = stock_recursive_download,
	not_interface = stock_not_interface,
	zips = stock_zip
):
	global spo

	array = []

	URL = (
		URL
		.split("?")[0]
		.split("/")
	)

	try:
		tracks = spo.user_playlist_tracks(URL[-3], URL[-1])
	except Exception as a:
		if not "The access token expired" in str(a):
			raise exceptions.InvalidLink("Invalid link ;)")

		spo = Spotify(
			generate_token()
		)

		tracks = spo.user_playlist_tracks(URL[-3], URL[-1])

	def lazy(tracks):
		for a in tracks['items']:
			try:
				array.append(
					download_trackspo(
						a['track']['external_urls']['spotify'],
						output, recursive_download, not_interface
					)
				)
			except:
				print("Track not found :(")
				array.append("None")

	lazy(tracks)
	tot = tracks['total']

	for a in range(tot // 100 - 1):
		try:
			tracks = spo.next(tracks)
		except:
			spo = Spotify(
				generate_token()
			)

			tracks = spo.next(tracks)

		lazy(tracks)

	if zips:
		zip_name = "{}playlist {}.zip".format(output, URL[-1])			
		create_zip(zip_name, array)
		return array, zip_name

	return array

def download_name(
	artist, song,
	output = stock_output + "/",
	recursive_download = stock_recursive_download,
	not_interface = stock_not_interface
):
	global spo

	query = "track:{} artist:{}".format(song, artist)

	try:
		search = spo.search(query)
	except:
		spo = Spotify(
			generate_token()
		)

		search = spo.search(query)

	try:
		return download_trackspo(
			search['tracks']['items'][0]['external_urls']['spotify'],
			output, recursive_download, not_interface
		)
	except IndexError:
		raise exceptions.TrackNotFound("Track not found: :(")