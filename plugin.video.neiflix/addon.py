# -*- coding: utf-8 -*-

import os
import urllib
import xbmc
import xbmcaddon
import xbmcgui

ALFA_URL= "https://raw.githubusercontent.com/tonikelope/neiflix_alfa/master/plugin.video.alfa/"

ALFA_PATH=xbmc.translatePath('special://home/addons/plugin.video.alfa/')

FILES=['servers/nei.json', 'servers/nei.py', 'channels/neiflix.py', 'channels/neiflix.json', 'resources/media/channels/banner/neiflix2_b.png', 'resources/media/channels/thumb/neiflix2_t.png', 'resources/media/channels/fanart/neiflix2_f.png']

installed = False

for f in FILES:
    if not os.path.exists(ALFA_PATH + f):
        urllib.urlretrieve(ALFA_URL + f, ALFA_PATH + f)
        installed=True

addon = xbmcaddon.Addon()

addonname = addon.getAddonInfo('name')

if installed:
    xbmcgui.Dialog().ok(addonname, 'Se ha añadido NEIFLIX a ALFA. (Ahora debería salirte en la lista de canales de ALFA).')
else:
    xbmcgui.Dialog().ok(addonname, 'Para entrar a NEIFLIX tienes que hacerlo a través de la lista de canales de ALFA. (Este icono sólo se usa para instalar NEIFLIX la primera vez).')
