from setuptools import setup
setup(
      name = "dwytsongs",
      version = "1.4",
      description = "Downloads songs, albums or playlists through spotify or deezer link from youtube",
      license = "Apache-2.0",
      author = "An0nimia",
      author_email = "An0nimia@protonmail.com",
      url = "https://github.com/An0nimia/dwspo",
      packages = ["dwytsongs"],
      install_requires = ["bs4", "ffmpeg-python", "mutagen", "pafy", "requests", "spotipy", "tqdm", "youtube-dl"]
)