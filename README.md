# Spotify Music Downloader

Running this script while listening to spotify (Linux Desktop Version) will download the music played **from youtube**. The music will be saved first on /tmp and when finished on ~/Music/<artist>/<album>/song-name.mp3


# Requeriments

  * Linux distribution (tested on ubuntu 14.04.3)
  * youtube-dl
  ```
  sudo apt-get install youtube-dl
  ```
  * Audio conversion library
  ```
  sudo apt-get install libav-tools
  ```
  * Python 2.7

# Usage
```
python spotify_downloader.py
```

# Contributing

Feel free to open issues and send pull requests =]

# Release Notes

**TODO**
  * Find and fix bugs =p
  * Handle d-bus errors

**0.0.1**

It's works, music is downloaded while spotify is playing...


# License

The MIT License

Copyright (c) 2010-2016 Google, Inc. http://angularjs.org

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.