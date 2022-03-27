from pytube import YouTube, Playlist
import os, sys
from pytube.cli import on_progress # progress bar

def mkdir(dir_name):
  # makes directory in specified location
  # ensure you change parent_dir to your home directory
  
  parent_dir = sys.path[0]
  path = os.path.join(parent_dir, dir_name)
  if not(os.path.isdir(f'{path}')):
    os.mkdir(path)
    print("Directory '%s' created" % dir_name)


def title_formatter(title):
  # removes file path location and .mp4 extension
  # removing file path location
  title = title.replace('/Home/Runner/Youtube-Video-Downloader/', '')
  # removing .mp4 extension
  title = title.replace('.Mp4', '')
  # returns file title
  return title

def is_audio_func():
  # defaults to video
  is_audio = input('Download video or audio [V/a]?: ')
  if is_audio == 'V' or is_audio == 'v' or is_audio == '':
    return False
  elif is_audio == 'A' or is_audio == 'a':
    return True
  else:
    print('Invalid input.')
    is_audio_func()

def is_yt_vid(url):
  # checks if URL is a real YouTube video
  try:
    test = YouTube(url)
  except:
    return False
  else:
    return True
def is_yt_playlist(url):
  # checks if URL is a real YouTube playlist
  if 'https://www.youtube.com/playlist?list=' in url:
    return True
  else:
    return False


def vid_download(url):
  # downloads 1 YouTube video
  # asks user if they want audio. defaults to video
  is_audio = is_audio_func()
  
  if is_audio:
    # Downloads highest quality mp4 YouTube audio available
    yt = YouTube(url, on_progress_callback=on_progress().streams.filter(only_audio=True, file_extension='mp4').order_by('abr').last().download())
  else:
    # Downloads highest quality mp4 YouTube video available using progressive
    yt = YouTube(url, on_progress_callback=on_progress).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').last().download()

  
  yt_title = yt.title()
  print('Downloaded: '+ title_formatter(yt_title))


def playlist_download(url):
  # downloads 1 YouTube playlist
  # asks user if they want audio. defaults to video
  is_audio = is_audio_func()
  
  pl = Playlist(url)

  # Warns user that they are about to download {x} videos from {y} playlist
  print(f'WARNING! You are about to download {len(pl.videos)} videos from {pl.title}.')
  warning = input('Type \'Yes\' to continue: ')
  
  # user decides to download playlist
  if warning == 'Yes':
    print(f'Downloading {len(pl.videos)} videos from {pl.title}.')

    # makes folder for playlist
    dir = pl.title
    mkdir(dir)
    path = sys.path[0]

    # checking if audio or video
    if is_audio:
      for aud in pl.videos:
        # Downloads highest quality mp4 YouTube audio available
        aud.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').last().download(output_path=f'{path}/{dir}')
    else:
      for vid in pl.videos:
        # Downloads highest quality mp4 YouTube audio available using progressive
        vid.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').last().download(output_path=f'{path}/{dir}')

    print('Download completed')
  else:
    # user decides not to download and is brought to start()
    print('Download aborted.')
    start()

def start():
  url = input('Enter YouTube URL: ')
  # checking if url is a valid YT video or playlist url
  is_vid = is_yt_vid(url)
  is_playlist = is_yt_playlist(url)

  # redirects user depending on whether URL is a video, playlist, or invalid
  if is_vid == True:
    vid_download(url)
  elif is_playlist == True:
    playlist_download(url)
  else:
    print('ERROR: Enter invalid YouTube URL.')
    start()
      
  start()
start()