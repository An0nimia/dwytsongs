#!/usr/bin/python3
import os
import pafy
import json
import ffmpeg
import spotipy
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import spotipy.oauth2 as oauth2
from mutagen.id3 import ID3, APIC
from mutagen.easyid3 import EasyID3
localdir = os.getcwd()
class TrackNotFound(Exception):
      def __init__(self, message):
          super().__init__(message)
class InvalidLink(Exception):
      def __init__(self, message):
          super().__init__(message)
def generate_token():
    credentials = oauth2.SpotifyClientCredentials(client_id="4fe3fecfe5334023a1472516cc99d805", client_secret="0f02b7c483c04257984695007a4a8d5c")
    token = credentials.get_access_token()
    return token
token = generate_token()
spo = spotipy.Spotify(auth=token)
def download_trackdee(URL, output=localdir + "/Songs/", check=True):
    if output == localdir + "/Songs":
     if not os.path.isdir("Songs"):
      os.makedirs("Songs")
    array = []
    music = []
    artist = []
    album = []
    tracknum = []
    discnum = []
    year = []
    genre = []
    ar_album = []
    if "?utm" in URL:
     URL,a = URL.split("?utm")
    URL = "http://www.deezer.com/track/" + URL.split("/")[-1]
    try:
       url = json.loads(requests.get("http://api.deezer.com/track/" + URL.split("/")[-1]).text)
    except:
       url = json.loads(requests.get("http://api.deezer.com/track/" + URL.split("/")[-1]).text)
    try:
       if url['error']['message'] == "Quota limit exceeded":
        raise QuotaExceeded("Too much requests limit yourself")
    except KeyError:
       None
    try:
       if "error" in str(url):
        raise InvalidLink("Invalid link ;)")
    except KeyError:
       None
    try:
       url1 = json.loads(requests.get("http://api.deezer.com/album/" + str(url['album']['id']), headers=header).text)
    except:
       url1 = json.loads(requests.get("http://api.deezer.com/album/" + str(url['album']['id']), headers=header).text)
    try:
       if url1['error']['message'] == "Quota limit exceeded":
        raise QuotaExceeded("Too much requests limit yourself")
    except KeyError:
       None
    try:
       image = url['album']['cover_xl'].replace("1000", "1200")
    except:
       try:
          image = requests.get(URL).text
       except:
          image = requests.get(URL).text
       image = BeautifulSoup(image, "html.parser").find("img", class_="img_main").get("src").replace("120", "1200")
    music.append(url['title'])
    for a in url['contributors']:
        array.append(a['name'])
    if len(array) > 1:
     for a in array:
         for b in range(len(array)):
             try:
                if a in array[b] and a != array[b]:
                 del array[b]
             except IndexError:
                break
    artist.append(", ".join(array))
    album.append(url['album']['title'])
    tracknum.append(url['track_position'])
    discnum.append(url['disk_number'])
    year.append(url['album']['release_date'])
    song = music[0] + " - " + artist[0]
    url = requests.get("https://www.youtube.com/results?search_query=" + music[0].replace("#", "") + "+" + artist[0].replace("#", ""))
    bs = BeautifulSoup(url.text, "html.parser")
    for topicplus in bs.find_all("a"):
        if len(topicplus.get("href")) == 20:
         down = topicplus.get("href")
         break
    try:
       if pafy.new("https://www.youtube.com" + down).length > 600:
        raise TrackNotFound("Track not found: " + song)
    except OSError:
       raise TrackNotFound("Error cannot determine the length of the video")
    dir = str(output) + "/" + artist[0].replace("/", "") + "/"
    try:
       if not os.path.isdir(dir):
        os.makedirs(dir)
    except:
       None
    name = artist[0].replace("/", "") + " " + music[0].replace("/", "") + ".mp3"
    if os.path.isfile(dir + name):
     if check == False:
      return dir + name
     ans = input("Song already exist do you want to redownload it?(y or n):")
     if not ans == "y":
      return
    print("\nDownloading:" + song)
    file = URL.split("/")[-1]
    os.system('youtube-dl https://www.youtube.com' + down + ' -f best -o "' + dir + file + '"')
    try:
       ffmpeg.input(dir + file).output(dir + name).run(overwrite_output=True)
       try:
          os.remove(dir + file)
       except FileNotFoundError:
          None
       image = requests.get(image).content
       tag = EasyID3(dir + name)
       tag.delete()
       tag['artist'] = artist[0]
       tag['title'] = music[0]
       tag['date'] = year[0]
       tag['album'] = album[0]
       tag['tracknumber'] = str(tracknum[0])
       tag['discnumber'] = str(discnum[0])
       tag['albumartist'] = ", ".join(ar_album)
       tag.save(v2_version=3)
       audio = ID3(dir + name)
       audio['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=image)
       audio.save()
    except ffmpeg._run.Error:
       os.remove(dir + file)
       print("Error while downloading: " + song)
    return dir + name
def download_albumdee(URL, output=localdir + "/Songs/", check=True):
    if output == localdir + "/Songs":
     if not os.path.isdir("Songs"):
      os.makedirs("Songs")
    array = []
    music = []
    artist = []
    album = []
    tracknum = []
    discnum = []
    year = []
    genre = []
    ar_album = []
    urls = []
    names = []
    if "?utm" in URL:
     URL,a = URL.split("?utm")
    URL = "http://www.deezer.com/album/" + URL.split("/")[-1]
    try:
       url = json.loads(requests.get("http://api.deezer.com/album/" + URL.split("/")[-1], headers=header).text)
    except:
       url = json.loads(requests.get("http://api.deezer.com/album/" + URL.split("/")[-1], headers=header).text)
    try:
       if url['error']['message'] == "Quota limit exceeded":
        raise QuotaExceeded("Too much requests limit yourself")
    except KeyError:
       None
    try:
       if "error" in str(url):
        raise InvalidLink("Invalid link ;)")
    except KeyError:
       None
    try:
       image = url['cover_xl'].replace("1000", "1200")
    except:
       try:
          image = requests.get(URL).text
       except:
          image = requests.get(URL).text
       image = BeautifulSoup(image, "html.parser").find("img", class_="img_main").get("src").replace("200", "1200")
    for a in url['tracks']['data']:
        music.append(a['title'])
        urls.append(a['link'])
    for a in url['tracks']['data']:
        del array[:]
        try:
           ur = json.loads(requests.get("https://api.deezer.com/track/" + str(a['id'])).text)
        except:
           ur = json.loads(requests.get("https://api.deezer.com/track/" + str(a['id'])).text)
        try:
           if ur['error']['message'] == "Quota limit exceeded":
            raise QuotaExceeded("Too much requests limit yourself")
        except KeyError:
           None
        tracknum.append(ur['track_position'])
        discnum.append(ur['disk_number'])
        for a in ur['contributors']:
            array.append(a['name'])
            if len(array) > 1:
             for a in array:
                 for b in range(len(array)):
                     try:
                        if a in array[b] and a != array[b]:
                         del array[b]
                     except IndexError:
                        break
    artist.append(", ".join(array))
    album.append(url['title'])
    year.append(url['release_date'])
    try:
       for a in url['genres']['data']:
           genre.append(a['name'])
    except KeyError:
       None
    for a in url['contributors']:
        if a['role'] == "Main":
         ar_album.append(a['name'])
    dir = str(output) + "/" + album[0].replace("/", "") + "/"
    try:
       if not os.path.isdir(dir):
        os.makedirs(dir)
    except:
       None
    image = requests.get(image).content
    for a in tqdm(range(len(music))):
        name = artist[a].replace("/", "") + " " + music[a].replace("/", "") + ".mp3"
        names.append(dir + name)
        url = requests.get("https://www.youtube.com/results?search_query=" + music[a].replace("#", "") + "+" + artist[a].replace("#", ""))
        bs = BeautifulSoup(url.text, "html.parser")
        for topicplus in bs.find_all("a"):
            if len(topicplus.get("href")) == 20:
             down = topicplus.get("href")
             break
        try:     
           if pafy.new("https://www.youtube.com" + down).length > 600:
            print("Track not found: " + music[a] + "  " + artist[a])
            continue
        except OSError:
           print("Error cannot determine the length of the video")
           continue    
        if os.path.isfile(dir + name):
         if check == False:
          continue
         print(dir + name)
         ans = input("Song already exist do you want to redownload it?(y or n):")
         if not ans == "y":
          return
        file = urls[a]
        os.system('youtube-dl https://www.youtube.com' + down + ' -f best -o "' + dir + file + '"')
        try:
           ffmpeg.input(dir + file).output(dir + name).run(overwrite_output=True)
           try:
              os.remove(dir + file)
           except FileNotFoundError:
              None
        except ffmpeg._run.Error:
           os.remove(dir + file)
           continue
        tag = EasyID3(dir + name)
        tag.delete()
        tag['artist'] = artist[a]
        tag['title'] = music[a]
        tag['date'] = year[0]
        tag['album'] = album[0]
        tag['tracknumber'] = str(tracknum[a])
        tag['discnumber'] = str(discnum[a])
        tag['albumartist'] = ", ".join(ar_album)
        tag.save(v2_version=3)
        audio = ID3(dir + name)
        audio['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=image)
        audio.save()
    return names     
def download_playlistdee(URL, output=localdir + "/Songs/", check=True):
    array = []
    if "?utm" in URL:
     URL,a = URL.split("?utm")
    try:
       url = json.loads(requests.get("https://api.deezer.com/playlist/" + URL.split("/")[-1] + "/tracks").text)
    except:
       url = json.loads(requests.get("https://api.deezer.com/playlist/" + URL.split("/")[-1] + "/tracks").text)
    try:
       if url['error']['message'] == "Quota limit exceeded":
        raise QuotaExceeded("Too much requests limit yourself")
    except KeyError:
       None
    try:
       if "error" in str(url):
        raise InvalidLink("Invalid link ;)")
    except KeyError:
       None
    for a in url['data']:
        array.append(download_trackdee(a['link'], output, check))
    return array
def download_trackspo(URL, output=localdir + "/Songs/", check=True):
    global spo
    if output == localdir + "/Songs":
     if not os.path.isdir("Songs"):
      os.makedirs("Songs")
    array = []
    music = []
    artist = []
    album = []
    tracknum = []
    discnum = []
    year = []
    genre = []
    ar_album = []
    if "?" in URL:
     URL,a = URL.split("?")
    try:
       url = spo.track(URL)
    except Exception as a:
       if not "The access token expired" in str(a):
        raise InvalidLink("Invalid link ;)")
       token = generate_token()
       spo = spotipy.Spotify(auth=token)
       url = spo.track(URL)
    music.append(url['name'])
    for a in range(20):
        try:
           array.append(url['artists'][a]['name'])
        except IndexError:
           artist.append(", ".join(array))
           del array[:]
           break
    album.append(url['album']['name'])
    image = url['album']['images'][0]['url']
    tracknum.append(url['track_number'])
    discnum.append(url['disc_number'])
    year.append(url['album']['release_date'])
    song = music[0] + " - " + artist[0]
    url = requests.get("https://www.youtube.com/results?search_query=" + music[0].replace("#", "") + "+" + artist[0].replace("#", ""))
    bs = BeautifulSoup(url.text, "html.parser")
    for topicplus in bs.find_all("a"):
        if len(topicplus.get("href")) == 20:
         down = topicplus.get("href")
         break
    try:
       if pafy.new("https://www.youtube.com" + down).length > 600:
        raise TrackNotFound("Track not found: " + song)
    except OSError:
       raise TrackNotFound("Error cannot determine the length of the video")
    dir = str(output) + "/" + artist[0].replace("/", "") + "/"
    try:
       if not os.path.isdir(dir):
        os.makedirs(dir)
    except:
       None
    name = artist[0].replace("/", "") + " " + music[0].replace("/", "") + ".mp3"
    if os.path.isfile(dir + name):
     if check == False:
      return dir + name
     ans = input("Song already exist do you want to redownload it?(y or n):")
     if not ans == "y":
      return
    print("\nDownloading:" + song)
    file = URL.split("/")[-1]
    os.system('youtube-dl https://www.youtube.com' + down + ' -f best -o "' + dir + file + '"')
    try:
       ffmpeg.input(dir + file).output(dir + name).run(overwrite_output=True)
       try:
          os.remove(dir + file)
       except FileNotFoundError:
          None
       image = requests.get(image).content
       tag = EasyID3(dir + name)
       tag.delete()
       tag['artist'] = artist[0]
       tag['title'] = music[0]
       tag['date'] = year[0]
       tag['album'] = album[0]
       tag['tracknumber'] = str(tracknum[0])
       tag['discnumber'] = str(discnum[0])
       tag['albumartist'] = ", ".join(ar_album)
       tag.save(v2_version=3)
       audio = ID3(dir + name)
       audio['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=image)
       audio.save()
    except ffmpeg._run.Error:
       os.remove(dir + file)
       print("Error while downloading: " + song)
    return dir + name
def download_albumspo(URL, output=localdir + "/Songs/", check=True):
    global spo
    if output == localdir + "/Songs":
     if not os.path.isdir("Songs"):
      os.makedirs("Songs")
    array = []
    music = []
    artist = []
    album = []
    tracknum = []
    discnum = []
    year = []
    genre = []
    ar_album = []
    urls = []
    names = []
    if "?" in URL:
     URL,a = URL.split("?")
    try:
       tracks = spo.album(URL)
    except Exception as a:
       if not "The access token expired" in str(a):
        raise InvalidLink("Invalid link ;)")
       token = generate_token()
       spo = spotipy.Spotify(auth=token)
       tracks = spo.album(URL)
    album.append(tracks['name'])
    for a in tracks['artists']:
        ar_album.append(a['name'])
    for track in tracks['tracks']['items']:
        music.append(track['name'])
        tracknum.append(track['track_number'])
        discnum.append(track['disc_number'])
        urls.append(track['external_urls']['spotify'])
    for artists in tracks['tracks']['items']:
        for a in range(20):
            try:
               array.append(artists['artists'][a]['name'])
            except IndexError:
               artist.append(", ".join(array))
               del array[:]
               break
    year.append(tracks['release_date'])
    image = tracks['images'][0]['url']
    artis = tracks['artists'][0]['name']
    for a in range(tracks['total_tracks'] // 50):
        try:
           tracks = spo.next(tracks['tracks'])
        except:
           token = generate_token()
           spo = spotipy.Spotify(auth=token)
           tracks = spo.next(tracks)['items']
        for track in tracks['items']:
            music.append(track['name'])
            tracknum.append(track['track_number'])
            discnum.append(track['disc_number'])
            urls.append(track['external_urls']['spotify'])
        for artists in tracks['items']:
            for a in range(20):
                try:
                   array.append(artists['artists'][a]['name'])
                except IndexError:
                   artist.append(", ".join(array))
                   del array[:]
                   break
    dir = str(output) + "/" + album[0].replace("/", "") + "/"
    try:
       if not os.path.isdir(dir):
        os.makedirs(dir)
    except:
       None
    image = requests.get(image).content
    for a in tqdm(range(len(music))):
        name = artist[a].replace("/", "") + " " + music[a].replace("/", "") + ".mp3"
        names.append(dir + name)
        url = requests.get("https://www.youtube.com/results?search_query=" + music[a].replace("#", "") + "+" + artist[a].replace("#", ""))
        bs = BeautifulSoup(url.text, "html.parser")
        for topicplus in bs.find_all("a"):
            if len(topicplus.get("href")) == 20:
             down = topicplus.get("href") 
             break
        try:
           if pafy.new("https://www.youtube.com" + down).length > 600:
            print("Track not found: " + music[a] + "  " + artist[a])
            continue
        except OSError:
           print("Error cannot determine the length of the video")
           continue    
        if os.path.isfile(dir + name):
         if check == False:
          continue
         print(dir + name)
         ans = input("Song already exist do you want to redownload it?(y or n):")
         if not ans == "y":
          return
        file = urls[a]
        os.system('youtube-dl https://www.youtube.com' + down + ' -f best -o "' + dir + file + '"')
        try:
           ffmpeg.input(dir + file).output(dir + name).run(overwrite_output=True)
           try:
              os.remove(dir + file)
           except FileNotFoundError:
              None
        except ffmpeg._run.Error:
           os.remove(dir + file)
           continue
        tag = EasyID3(dir + name)
        tag.delete()
        tag['artist'] = artist[a]
        tag['title'] = music[a]
        tag['date'] = year[0]
        tag['album'] = album[0]
        tag['tracknumber'] = str(tracknum[a])
        tag['discnumber'] = str(discnum[a])
        tag['albumartist'] = ", ".join(ar_album)
        tag.save(v2_version=3)
        audio = ID3(dir + name)
        audio['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=image)
        audio.save()
    return names
def download_playlistspo(URL, output=localdir + "/Songs/", check=True):
    global spo
    array = []
    if "?" in URL:
     URL,a = URL.split("?")
    URL = URL.split("/")
    try:
       tracks = spo.user_playlist_tracks(URL[-3], playlist_id=URL[-1])
    except Exception as a:
       if not "The access token expired" in str(a):
        raise InvalidLink("Invalid link ;)")
       token = generate_token()
       spo = spotipy.Spotify(auth=token)
       tracks = spo.user_playlist_tracks(URL[-3], playlist_id=URL[-1])
    for a in tracks['items']:
        try:
           array.append(download_trackspo(a['track']['external_urls']['spotify'], output, check, True))
        except IndexError:
           print("\nTrack not found " + a['track']['name'])
           array.append(localdir + "/Songs/" + a['track']['name'])
    for a in range(tracks['total'] // 100):
        try:
           tracks = spo.next(tracks)
        except:
           token = generate_token()
           spo = spotipy.Spotify(auth=token)
           tracks = spo.next(tracks)
    for a in tracks['items']:
        try:
           array.append(download_trackspo(a['track']['external_urls']['spotify'], output, check, True))
        except IndexError:
           print("\nTrack not found " + a['track']['name'])
           array.append(localdir + "/Songs/" + a['track']['name'])
    return array
def download_name(artist, song, output=localdir + "/Songs/", check=True):
    global spo
    try:
       search = spo.search(q="track:" + song + " artist:" + artist)
    except:
       token = generate_token()
       spo = spotipy.Spotify(auth=token)
       search = spo.search(q="track:" + song + " artist:" + artist)
    try:
       return download_trackspo(search['tracks']['items'][0]['external_urls']['spotify'], output, check)
    except:
       raise TrackNotFound("Track not found: " + song + " - " + artist)