import dbus
from dbus.mainloop.glib import DBusGMainLoop
from youtube_dl import YoutubeDL
import gobject


# ---------- CONFIG ----------

MUSIC_FOLDER__ABSOLUTE_PATH = '/home/filipe/Music/'
ORGANIZE_BY_ARTIST = True
ORGANIZE_BY_ALBUM = True


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def yt_hook(d):
    print d['status']
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

YOUTUBE_OBJ = YoutubeDL({
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [yt_hook],
    })

# ---------- END CONFIG ----------


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
        'title': str(title),
        'album': str(album),
        'artist': str(artist)
        }


def youtube_grabber(tit, art, alb):
    if not (tit and art and alb):
        print "problem grabbing iformation from spotify not downloading"
        return
    query_url = 'https://www.youtube.com/results?search_query='+tit+art+alb+'&page=1'
    result = YOUTUBE_OBJ.extract_info(query_url, download=False, process=False)

    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result
    video_url = video['url']

    print '----- youtube info -----'
    print 'Title: '+video["title"]
    print 'URL: '+video_url
    print '------------------------'
    return video_url


def youtube_downloader(video_url):
    pass


def spotify_handler(*args):
    music_data = spotify_grabber(args[1]["Metadata"])
    video_url = youtube_grabber(music_data.get("title"), music_data.get("artist"), music_data.get("album"))

if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    session_bus.add_signal_receiver(spotify_handler, 'PropertiesChanged', None, 'org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')

    loop = gobject.MainLoop()
    loop.run()
    
    
    