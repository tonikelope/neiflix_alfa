# -*- coding: utf-8 -*-
import base64
import json
import os
import urllib
import xml.etree.ElementTree as ET

import xbmc
import xbmcaddon
import xbmcgui


def improve_streaming():
    if os.path.exists(xbmc.translatePath('special://userdata/advancedsettings.xml')):
        settings_xml = ET.parse(xbmc.translatePath('special://userdata/advancedsettings.xml'))
    else:
        settings_xml = ET.ElementTree(ET.Element('advancedsettings'))

    cache = settings_xml.find("cache")

    if not cache:
        cache = ET.Element('cache')
        memorysize = ET.Element('memorysize')
        memorysize.text = '52428800'
        readfactor = ET.Element('readfactor')
        readfactor.text = '8'
        cache.append(memorysize)
        cache.append(readfactor)
        settings_xml.getroot().append(cache)

    network = settings_xml.find("network")

    if not network:
        network = ET.Element('network')
        curlclienttimeout = ET.Element('curlclienttimeout')
        curlclienttimeout.text = '60'
        network.append(curlclienttimeout)
        settings_xml.getroot().append(network)

    playlisttimeout = settings_xml.find("playlisttimeout")

    if not playlisttimeout:
        playlisttimeout = ET.Element('playlisttimeout')
        playlisttimeout.text = '60'
        settings_xml.getroot().append(playlisttimeout)

    settings_xml.write(xbmc.translatePath('special://userdata/advancedsettings.xml'))


def update_favourites():
    if os.path.exists(xbmc.translatePath('special://userdata/favourites.xml')):
        favourites_xml = ET.parse(xbmc.translatePath('special://userdata/favourites.xml'))
    else:
        favourites_xml = ET.ElementTree(ET.Element('favourites'))

    neiflix = favourites_xml.findall("favourite[@name='NEIFLIX']")

    if not neiflix:
        with open(xbmc.translatePath('special://home/addons/plugin.video.neiflix/favourite.json'), 'r') as f:
            favourite = json.loads(f.read())

        favourite['fanart'] = xbmc.translatePath('special://home/addons/plugin.video.alfa' + favourite['fanart'])
        favourite['thumbnail'] = xbmc.translatePath('special://home/addons/plugin.video.alfa' + favourite['thumbnail'])
        neiflix = ET.Element('favourite', {'name': 'NEIFLIX', 'thumb': xbmc.translatePath(
            'special://home/addons/plugin.video.alfa/resources/media/channels/thumb/neiflix2_t.png')})
        neiflix.text = 'ActivateWindow(10025,"plugin://plugin.video.alfa/?' + urllib.quote(base64.b64encode(json.dumps(favourite)))  + '",return)'
        favourites_xml.getroot().append(neiflix)
        favourites_xml.write(xbmc.translatePath('special://userdata/favourites.xml'))

ALFA_URL = "https://raw.githubusercontent.com/tonikelope/neiflix_alfa/master/plugin.video.alfa/"

ALFA_PATH = xbmc.translatePath('special://home/addons/plugin.video.alfa/')

FILES = ['channels/neiflix.py', 'channels/neiflix.json', 'servers/nei.py', 'servers/nei.json',
         'resources/media/channels/banner/neiflix2_b.png', 'resources/media/channels/thumb/neiflix2_t.png',
         'resources/media/channels/fanart/neiflix2_f.png']

if not os.path.exists(xbmc.translatePath('special://home/addons/plugin.video.neiflix/installed')):

    with open(xbmc.translatePath('special://home/addons/plugin.video.neiflix/installed'), 'w+') as f:
        pass

    for f in FILES:
        if not os.path.exists(ALFA_PATH + f):
            urllib.urlretrieve(ALFA_URL + f, ALFA_PATH + f)

    improve_streaming()
    update_favourites()
    ret = xbmcgui.Dialog().yesno(xbmcaddon.Addon().getAddonInfo('name'), 'Se ha añadido NEIFLIX a ALFA.\n\nES NECESARIO REINICIAR KODI PARA QUE TODOS LOS CAMBIOS TENGAN EFECTO.\n\n¿Quieres reiniciar KODI ahora mismo?')

    if ret:
        xbmc.executebuiltin('RestartApp')
else:
    xbmcgui.Dialog().ok(xbmcaddon.Addon().getAddonInfo('name'), 'Para entrar a NEIFLIX tienes que hacerlo a través del icono con la estrellita (dentro de FAVORITOS) o bien buscar NEIFLIX en la lista de canales de ALFA.')
