#!/usr/env/python -tt
# -*- encoding=utf8 -*-
#
#   Copyright 2009-2012 Michal Sadowski (sq6jnx at hamradio dot pl)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import urllib
import debug
import json
import os 
import BeautifulSoup
lang=None

def safe_name(s):
    """Returns "safe" name for i.e. geographical name for languages with
    non-latin characters i.e. polish, where there are boty Ślęża and Ślęza
    rivers (both are usually converted to Sleza, but should be read aloud
    differently.
    
    I've no idea if such situation appears in czech, but... just in case..."""

    if str(s.__class__)=="<type 'str'>":
        s=unicode(s, 'utf-8')
    return s.replace(u'á','a_').replace(u'é','e_').\
        replace(u'ě','e!').replace(u'í','i_').replace(u'ó','o_').\
        replace(u'ú','o!').replace(u'ů','u_').replace(u'ý','y_').\
        replace(u'ď','d_').replace(u'ť','t_').replace(u'ň','n_').\
        replace(u'ř','r_').replace(u'š','s_').replace(u'č','c_').\
        replace(u'ž','z_').replace(u'Á','a_').replace(u'É','e_').\
        replace(u'Ě','e!').replace(u'Í','i_').replace(u'Ó','o_').\
        replace(u'Ú','o!').replace(u'Ů','u_').replace(u'Ý','y_').\
        replace(u'Ď','d_').replace(u'Ť','t_').replace(u'Ň','n_').\
        replace(u'Ř','r_').replace(u'Š','s_').replace(u'Č','c_').\
        replace(u'Ž','z_').lower().replace(' ','_').replace(u'–','_')

awareness_levels = {
        '-1':-1, # information is not available, station offline
        ';?':-1, # information is not available (st. broke down?)
        ';':  0, # 0  (State of Normal)
        ';1': 1, # 1  (State of Alert)
        ';2': 2, # 2  (State of Emergency)     # not verified!
        ';3': 3, # 3  (State of Danger)        # not verified!
        ';4': 4, # 3! (State of Extreme Flood) # not verified!
        # couldn't verify `drought`!
        }

def downloadFile(url):
    """Returns contents of file available via URL"""
    webFile = urllib.urlopen(url)
    return webFile.read()

def my_import(name):
    """Imports module which name is given as a ``name`` parameter"""
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def getData(l):
    global lang
    lang = my_import(l+"."+l)
    data = {"data":"", "needCTCSS":False, "allOK":True}
    

    conf_regions = get_config_regions()
    
    if not os.path.exists('povodi_cz.json'):
        regions = generate_json(regions=regions.keys(), dont_save=True)
    else:
        regions = json.loads(unicode(open('povodi_cz.json','r').read(),'utf-8'))

    awarenesses = {}

    for region in conf_regions.keys():
        for river in regions[region]:
            for station in regions[region][river].keys():
                station_name, level = regions[region][river][station]
                if level>0 and station in conf_regions[region]:
                    if not awarenesses.has_key(str(level)):
                        awarenesses[str(level)]={}
                    if not awarenesses[str(level)].has_key(safe_name(river)):
                        awarenesses[str(level)][safe_name(river)]=[]
                    awarenesses[str(level)][safe_name(river)].\
                          append(safe_name(regions[region][river][station][0]))

    if awarenesses!={}:
        data['data']+= lang.povodi_cz_welcome
        for level in sorted(awarenesses.keys())[::-1]:
            if level>1:
                data['needCTCSS']=True
            data['data']+=' '+lang.awalvls[int(level)]
            for river in sorted(awarenesses[level].keys()):
                data['data']+=' '+lang.river+' '+river
                for station in sorted(awarenesses[level][river]):
                    data['data']+=' '+lang.station+' '+station

    debug.log("POVODI_CZ", "finished...")
    return data

def show_help():
    print u"""
Uruchamiając ten skrypt z linii komend możesz wygenerować w łatwy sposób 
fragment słownika sr0wx dla rzek i wodowskazów wskazanych w pliku config.py

Należy uruchomić povodi_cz podając jako parametr gen, np.

python povodi_cz.py gen > pl_google/povodi_cz_dict.py

a następnie

python google_tts_downloader.py povodi_cz_dict.py

aby dociągnąć niezbędne pliki."""

def get_region(region):
    """Returns dictionary with all rivers and stations with flood awareness
    levels on these stations.
    
    This dictionary is constructed as: ::
        
        rv[river][(station_id, station)]=awareness_level
    """

    url = 'http://www.%s.cz/portal/sap/en/mapa_vse.htm'
    html =BeautifulSoup.BeautifulSoup(downloadFile(url%region))
    rv = {}

    try:
    #if 1==1:
        for station in html.findAll('div'):
            if station.has_key('id') and 'text' in station['id']:
                r1, r2 = station.findAll('table')
                r1=r1.findAll('td')[0].text.split('&nbsp')
                r2=r2.findAll('td')[0].text.split('&nbsp')
                # We're almost done. What we have is:
                # r1 = [u'', u';Moravice', u';LG Val\u0161ov']
                # r2 = [u'Flood level:', u';', u';']
                # so now it's easy to see that:
                stid= station['id'][4:] # station id
                river = r1[1][1:]
                station=r1[2][4:]
                if 'porucha stanice' in r2[0]:
                    level = '-1'
                else:
                    level = r2[1]
                try:
                #if 1==1:
                    if not rv.has_key(river):
                        rv[river]={}
                    rv[river][stid]=[station, awareness_levels[level]]
                    # debug trick: WE are steering water levels
                    #from random import uniform
                    #level = int(uniform(1,5))
                    #rv[river][stid]=[station, int(uniform(1,5))]
                    # end of trick
                except:
                #else:
                    debug.log('POVODI_CZ', ("Couldn't parse region %s "\
                            + "river %s station %s data. Original "\
                            + "awareness info is "
                            +" (%s)")%(region,river,station,str(r2)),
                                buglevel=5)
        pass
    except:
    #else:
        debug.log('POVODI_CZ', "Couldn't parse region %s data"%region,\
                buglevel=5)
        pass

    return rv

def generate_json(regions=None, dont_save=False):
    """Generates povodi_cz.json file and returns its contents (dictionary).
    
    This file contains all river stations and the way it's constructed is: ::
        
        rv[region][river][station]=awareness_level
    """
    rv = {}
    if regions is None:
        regions=['poh','pla','pod','pmo','pvl']

    for region in regions:
        #try:
        if 1==1:
            rv[region]=get_region(region)
        #except:
        else:
            debug.log('POVODI_CZ',\
                    "Couldn't download data for region %s"%region,buglevel=5)
            pass

    if dont_save==False:
        json.dump(rv, open('povodi_cz.json','w'))

    return rv        

def generate_config():
    regions=generate_json(dont_save=True)

    print 'povodi_cz.stations = ['

    for region in sorted(regions.keys()):
        for river in sorted(regions[region].keys()):
            for station in sorted(regions[region][river].keys()):
                print "    ['%s','%s'],\t# %s, station %s"%\
                        (region,station,river,regions[region][river][station][0])
    print ']'

def get_config_regions():
    regions = {}
    for station in config.stations:
        if station[0] not in regions:
            regions[station[0]]=[]
        regions[station[0]].append(station[1])
    return regions

def generate_dictionary():
    regions = get_config_regions()

    phrases = []
    for region in regions.keys():
        region_data = get_region(region)
        for river in sorted(region_data.keys()):
            for station in sorted(region_data[river].keys()):
                if station in regions[region] and \
                        region_data[river][station][0] not in phrases:
                     phrases.append(region_data[river][station][0])
                     if river not in phrases:
                        phrases.append(river)

    print u"""#!/usr/bin/python
# -*- coding: utf-8 -*-

# Caution! I am not responsible for using these samples. Use at your own risk
# Google, Inc. is the copyright holder of samples downloaded with this tool.

# Generated automatically by imgw_podest.py. Feel free to modify it SLIGHTLY.

LANGUAGE = 'cs'

START_MARKER = '@'
END_MARKER = '@'

CUT_START = 0.9
CUT_END=0.7

download_list = [ """

    for phrase in phrases:
        print u"    [\"%s\", \"%s\"], # %s"%\
                (phrase, safe_name(phrase),phrase)

    print u']'

if __name__ == '__main__':
    class DummyDebug:
        def log(self,module,message,buglevel=None):
            print message

    debug = DummyDebug()
    import sys
    # I know it would be better to use getopt or similar, but is there a point
    # for using such a moloch for barely two options?
    
    if len(sys.argv)==2 and sys.argv[1]=='dict':
        from config import povodi_cz as config
        generate_dictionary()
    elif len(sys.argv)==2 and sys.argv[1]=='conf':
        generate_config()
    #else:
    #    show_stations()
    #    #show_help()
else:
    from config import povodi_cz as config
