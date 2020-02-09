# -*- coding: utf-8 -*-

import os
import urllib
import xbmc
import xbmcaddon
import xbmcgui

BASE_URL="https://raw.githubusercontent.com/tonikelope/neiflix/master/libreelec/storage/.kodi/addons/plugin.video.alfa/"

BASE_PATH=xbmc.translatePath('special://home/addons/plugin.video.alfa/')

FILES=['servers/nei.json', 'servers/nei.py', 'channels/neiflix.py', 'channels/neiflix.json', 'resources/media/channels/banner/neiflix2_b.png', 'resources/media/channels/thumb/neiflix2_t.png', 'resources/media/channels/fanart/neiflix2_f.png']

for f in FILES:
    if not os.path.exists(BASE_PATH + f):
        urllib.urlretrieve(BASE_URL + f, BASE_PATH + f)

addon = xbmcaddon.Addon()

addonname = addon.getAddonInfo('name')

xbmcgui.Dialog().ok(addonname, 'Se ha instalado el CANAL NEIFLIX en ALFA. Ahora debería salirte en la lista de canales de ALFA.')
