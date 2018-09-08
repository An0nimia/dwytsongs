# dwytsongs
This project has been created to download songs, albums or playlists with spotify or deezer link from youtube.
The songs are similar at 75%.
* ### OS Supported ###
    ![Linux Support](https://img.shields.io/badge/Linux-Support-brightgreen.svg)
    ![macOS Support](https://img.shields.io/badge/macOS-Support-brightgreen.svg)
    ![Windows Support](https://img.shields.io/badge/Windows-Support-brightgreen.svg)
* ### Installation ###
      pip3 install dwytsongs
* ### Important ###
    You need to install ffmpeg
  - Windows (https://www.wikihow.com/Install-FFmpeg-on-Windows)
  - Linux ("For debian like 'apt-get install ffmpeg'")
  - macOS ('brew install ffmpeg')
### Download song
Download track by spotify link
```python
import dwytsongs
dwytsongs.download_trackspo("Insert the spotify link of the track to download", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```
Download track by deezer link
```python
import dwytsongs
dwytsongs.download_trackdee("Insert the deezer link of the track to download", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```
### Download album
Download album by spotify link
```python
import dwytsongs
dwytsongs.download_albumspo("Insert the spotify link of the album to download", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```
Download album from deezer link
```python
import dwytsongs
dwytsongs.download_albumdee("Insert the deezer link of the album to download", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```
### Download playlist
Download playlist by spotify link
```python
import dwytsongs
dwytsongs.download_playlistspo("Insert the spotify link of the playlist to download", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```
Download playlist from deezer link
```python
import dwytsongs
dwytsongs.download_playlistdee("Insert the deezer link of the playlist to download", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```
### Download name
Download by name
```python
import dwytsongs
dwytsongs.download_name(artist="Eminem", song="Berzerk", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```