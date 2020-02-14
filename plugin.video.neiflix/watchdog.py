# -*- coding: utf-8 -*-
import hashlib
import os
import re
import urllib
import xbmc
import xbmcaddon
import xbmcgui

MONITOR_TIME = 15

ALFA_URL= "https://raw.githubusercontent.com/tonikelope/neiflix_alfa/master/plugin.video.alfa/"

KODI_TEMP_PATH=xbmc.translatePath('special://temp/')

ALFA_PATH=xbmc.translatePath('special://home/addons/plugin.video.alfa/')

FILES=['channels/neiflix.py', 'channels/neiflix.json', 'servers/nei.py', 'servers/nei.json', 'resources/media/channels/banner/neiflix2_b.png', 'resources/media/channels/thumb/neiflix2_t.png', 'resources/media/channels/fanart/neiflix2_f.png']

#CHECK NEIFLIX CHANNEL UPDATES

urllib.urlretrieve(ALFA_URL + 'channels/checksum.sha1', KODI_TEMP_PATH + 'neiflix_channel.sha1')

sha1_checksums = {}

with open(KODI_TEMP_PATH + 'neiflix_channel.sha1') as f:
    for line in f:
        strip_line = line.strip()
        if strip_line:
            parts = re.split(' +', line.strip())
            sha1_checksums[parts[1]]=parts[0]

updated = False

broken = False

for filename, checksum in sha1_checksums.iteritems():
    if os.path.exists(ALFA_PATH + 'channels/' + filename):
        with open(ALFA_PATH + 'channels/' + filename, 'rb') as f:
            file_hash = hashlib.sha1(f.read()).hexdigest()

        if file_hash != checksum:
            updated=True
            break
    else:
        broken = True

os.remove(KODI_TEMP_PATH + 'neiflix_channel.sha1')

if updated:
    for f in FILES:
        urllib.urlretrieve(ALFA_URL + f, ALFA_PATH + f)

    xbmcgui.Dialog().notification('NEIFLIX', '¡Canal NEIFLIX actualizado!', os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources', 'icon.png'), 5000)

elif broken:
    for f in FILES:
        urllib.urlretrieve(ALFA_URL + f, ALFA_PATH + f)

    xbmcgui.Dialog().notification('NEIFLIX', '¡Canal NEIFLIX instalado/reparado!', os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources', 'icon.png'), 5000)


#MONITOR CHANGES

while True:

    xbmc.sleep(MONITOR_TIME * 1000)

    updated = False

    for f in FILES:
        if not os.path.exists(ALFA_PATH + f):
            urllib.urlretrieve(ALFA_URL + f, ALFA_PATH + f)
            updated=True

    if updated:
        xbmcgui.Dialog().notification('NEIFLIX', '¡Canal NEIFLIX reparado!', os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources', 'icon.png'), 5000)