from __future__ import unicode_literals
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from youtube_dl import YoutubeDL
import gobject, shutil, uuid
from os import makedirs
from os.path import expanduser, isfile, exists
import sys
from inspect import getmodule
from multiprocessing import Pool


# ---------- CONFIG ----------

home = expanduser("~")
MUSIC_FOLDER_ABSOLUTE_PATH = home+'/Music'

# ---------- END CONFIG ----------

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def yt_hook(d):
    if d['status'] == 'downloading':
        print '.',
        sys.stdout.flush()
    elif d['status'] == 'finished':
        print '\nDone downloading, now converting ...'

#  decorator to send download function to background
def async(decorated):
    module = getmodule(decorated)
    decorated.__name__ += str('_original')
    setattr(module, decorated.__name__, decorated)

    def send(*args, **opts):
        return async.pool.apply_async(decorated, args, opts)

    return send


def spotify_grabber(metadata):
    title = metadata['xesam:title']
    album = metadata['xesam:album']
    artist = metadata['xesam:artist']
    if isinstance(title, dbus.Array):
        title = title[0]
    if isinstance(album, dbus.Array):
        album = album[0]
    if isinstance(artist, dbus.Array):
        artist = artist[0]
    print '----- spotify info -----'
    print 'Title: ' + title
    print 'Artist: ' + artist
    print 'Album: ' + album
    print '------------------------'
    return {
        'title': str(title.encode('ascii','ignore')),
        'album': str(album.encode('ascii','ignore')),
        'artist': str(artist.encode('ascii','ignore'))
        }



def youtube_grabber(music_data):
    query_url = 'https://www.youtube.com/results?search_query='+music_data.get('artist')+music_data.get('title')+music_data.get('album')+'&page=1'

    yt_opts = {
        'format': 'bestaudio/best',
        'logger': MyLogger(),
        'progress_hooks': [yt_hook],
    }
    
    ydl = YoutubeDL(yt_opts)
    result = ydl.extract_info(query_url, download=False, process=False)

    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result

    video_url = video['url']

    print '----- youtube downloading -----'
    print 'Title: '+video["title"]
    print 'URL: '+video_url
    print 'Downloading... '
    youtube_downloader(video_url, music_data)


@async
def youtube_downloader(video_url, music_data):
    output_folder_path = '%s/%s/%s' % (MUSIC_FOLDER_ABSOLUTE_PATH, music_data.get('artist'), music_data.get('album'))
    output_file_path = '%s/%s.mp3' % (output_folder_path, music_data.get('title'))
    temp_file_path = '/tmp/%s-%s.%s' % (uuid.uuid4(), music_data.get('title'), '%(ext)s')

    # check if file already exists
    if isfile(output_file_path):
        print "Music alread downloaded: %s" % output_file_path
        return

    # create folder if needed
    if not exists(output_folder_path):
        makedirs(output_folder_path)

    yt_opts = {
    'format': 'bestaudio/best',
    'outtmpl': temp_file_path,
    'extractaudio': True,
    'noplaylist': True,
    'matchtitle': music_data.get('title'),
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',

        },
        {
            'key': 'FFmpegMetadata'
            
        }
    ],
    'logger': MyLogger(),
    'progress_hooks': [yt_hook],
    }

    with YoutubeDL(yt_opts) as ydl:
      result = ydl.download([video_url])


    if result == 0:
        temp_file_path = temp_file_path.replace('.%(ext)s', ".mp3")
        shutil.move(temp_file_path, output_file_path)

    print music_data.get('title')+': download finished -----'


def get_playing_now(session_bus):
    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
    spotify_properties = dbus.Interface(spotify_bus, "org.freedesktop.DBus.Properties")
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
    spotify_handler(metadata)


def spotify_handler(*args):
    print '----- DOWNLOAD STARTED - To exit Ctrl-C -----'
    try:
        metadata=args[1]["Metadata"]
    except:
        metadata = args[0]

    music_data = spotify_grabber(metadata)
    youtube_grabber(music_data)



if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)
    async.pool = Pool(32)
    session_bus = dbus.SessionBus()
    # if theres a music playing now, download it
    get_playing_now(session_bus)
    # look for spotify signals (new music starts)
    session_bus.add_signal_receiver(spotify_handler, 'PropertiesChanged', None, 'org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')

    loop = gobject.MainLoop()
    loop.run()
    
    
    