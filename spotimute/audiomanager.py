#!/usr/bin/env python
# encoding: utf-8

import re
import sh


class NoSinkToUse(Exception):
    pass


class AudioManager(object):
    def __init__(self):
        try:
            self._update_sink_to_use()
        except:
            pass

    def _update_sink_to_use(self):
        self._sink_name = None
        self._sink_id = None
        sinks = sh.pactl('list', 'short', 'sinks').splitlines()

        for s in sinks:
            sink = s.split('\t')
            if sink[-1] in ("IDLE", "RUNNING"):
                self._sink_name = sink[1]
                self._sink_id = int(sink[0])

        if self._sink_name is None or self._sink_id is None:
            raise NoSinkToUse

    def has_sink(self):
        try:
            self._update_sink_to_use()
            return True
        except NoSinkToUse:
            return False

    def is_muted_old(self):
        """This uses `pacmd dump`"""
        self._update_sink_to_use()
        pacmd_dump = sh.pacmd('dump').strip().splitlines()

        for l in pacmd_dump:
            _title_re = 'set-sink-mute {0} (.*)'.format(self._sink_name)
            match = re.search(_title_re, l)

            if match is not None:
                return match.group(1) == "yes"

    def is_muted(self):
        """This uses the sink info we get from get_sinks"""
        self._update_sink_to_use()
        sink_info = self._get_sinks()[self._sink_id]
        _title_re = 'Mute:(.*)'
        match = re.search(_title_re, sink_info)
        return match.group(0).split(':')[-1].strip() == 'yes'

    def mute(self):
        self._update_sink_to_use()
        sh.pactl('set-sink-mute', self._sink_id, 1)

    def unmute(self):
        self._update_sink_to_use()
        sh.pactl('set-sink-mute', self._sink_id, 0)

    def _get_sinks(self):
        sinks_list = sh.pactl('list', 'sinks').stdout

        sinks = {}

        match = re.findall('Sink #', sinks_list)
        count = len(match)

        for i in range(count):
            if i+1 == count:
                sink_re = 'Sink #{0}(.*)'.format(i)
            else:
                sink_re = 'Sink #{0}(.*)Sink #'.format(i)

            match = re.findall(sink_re, sinks_list, re.MULTILINE | re.DOTALL)
            sinks[i] = match[0]

        return sinks

    def get_volume(self):
        self._update_sink_to_use()
        sink_info = self._get_sinks()[self._sink_id]
        _title_re = 'Volume(.*)'
        match = re.search(_title_re, sink_info)
        return match.group(0).split(':')[-1].strip()

    def set_volume(self, volume):
        try:
            vol = str(volume) + '%'
        except:
            print "The 'volume' parameter needs to be an int"

        self._update_sink_to_use()
        sh.pactl('set-sink-volume', self._sink_id, vol)

    def status(self):
        self._update_sink_to_use()
        print '-' * 50
        print "Sink name:", self._sink_name
        print "Sink id:", self._sink_id
        print "is muted:", self.is_muted()
        print "volume:", self.get_volume()
        print '-' * 50
