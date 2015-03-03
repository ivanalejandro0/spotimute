#!/usr/bin/env python
# encoding: utf-8

from audiomanager import AudioManager
from spotify import Spotify


def status(audio, spotify):
    print '-' * 50
    print "Sink name:", audio._sink_name
    print "Sink id:", audio._sink_id
    print "is muted:", audio.is_muted()
    print "volume:", audio.get_volume()
    print '-' * 5
    print "Spotify title:", spotify.get_title().encode('utf-8')
    print "Spotify title type:", type(spotify.get_title())
    # print "Spotify title unicode:", spotify.get_title().decode('')
    print "Spotify is blacklisted:", spotify.is_blacklisted()
    print '-' * 50


def loop(audio, spotify):
    import time

    a = audio

    while True:
        if spotify.is_blacklisted():
            if not a.is_muted():
                a.mute()
                status(audio, spotify)
        else:
            if a.is_muted():
                a.unmute()
                status(audio, spotify)
        time.sleep(0.1)


if __name__ == '__main__':
    audio = AudioManager()
    spotify = Spotify()

    status(audio, spotify)
    # loop(audio, spotify)
