#!/usr/bin/env python
# encoding: utf-8

import re
import sh
import os


class Spotify(object):
    def __init__(self):
        self._BLK = None
        blacklisted_path = os.path.join(os.path.dirname(__file__),
                                        'blacklisted.txt')
        try:
            with open(blacklisted_path) as bl:
                self._BLK = bl.read().splitlines()
        except:
            print "WARNING: missing blacklisted.txt file."

    def get_title(self):
        try:
            xprop_text = sh.xprop('-name', "Spotify Free - Linux Preview")
            xprop_text = unicode(xprop_text)
        except sh.ErrorReturnCode_1:
            return None

        _title_re = '_NET_WM_ICON_NAME\(UTF8_STRING\) = \"(.*)\"'
        match = re.search(_title_re, xprop_text)

        if match is not None:
            title = match.group(1)
        else:
            return None

        return title

    def is_blacklisted(self):
        title = self.get_title()

        if title is None or self._BLK is None:
            return False

        for ad in self._BLK:
            if title.startswith(ad):
                return True

        return False

    def blacklist(self, title):
        try:
            with open(self._blacklisted_path, 'a') as f:
                f.write(title)

            self._BLK.append(title)
        except:
            print "ERROR: couldn't write to blacklist file."
