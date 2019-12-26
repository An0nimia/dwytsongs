from setuptools import setup

setup(
	name = "dwytsongs",
	version = "2.5.2",
	description = "Downloads songs, albums or playlists through spotify or deezer link from youtube",
	license = "CC BY-NC-SA 4.0",
	author = "An0nimia",
	author_email = "An0nimia@protonmail.com",
	url = "https://github.com/An0nimia/dwytsongs",
	packages = ["dwytsongs"],
	install_requires = ["bs4", "ffmpeg-python", "mutagen", "pafy", "requests", "spotipy", "tqdm", "youtube-dl"]
)