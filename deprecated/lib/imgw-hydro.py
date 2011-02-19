#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

url = """http://www.pogodynka.pl/hydrobiuletyn.php"""

poczatek = """<CENTER><BR><B>STANY WODY W WYBRANYCH PROFILACH WODOWSKAZOWYCH W DORZECZU WISŁY</B><BR>dnia 26.03.2009, godz. 06 UTC<BR><BR></CENTER>"""
koniec   = """<CENTER><I><SMALL>Dane hydrologiczne pochodzą z operacyjnej bazy danych i mogą ulec zmianie po weryfikacji.</SMALL></I></CENTER><!-- KONIEC --></TD>"""


import urllib

def downloadFile(url):
    webFile = urllib.urlopen(url)
    return webFile.read()

file = downloadFile(url)

#data = " ".join(file[file.index(poczatek)-3].split("<")).split(">")[2].split("(")[1].split(")")[0].split(".")
#print data


dane = file.replace("\r\n","").split("<!-- SEKCJA -->")



for line in dane[1].split("<TABLE")[1].split("</TR><TR>"):
    for l in line.split("</TR><TR"):
        if len(l.split(">"))>10:
            l=l.replace("<div style=\"color:red\"","").replace("</div>","")
            rzeka = l.split(">")[2].split("</TD")[0].strip()
            wodowskaz = l.split(">")[4].split("</TD")[0].strip()
            strefaStanu = l.split(">")[6].split("</TD")[0]
            stanAlarmowy = l.split(">")[8].split("</TD")[0]
            przeplyw = l.split(">")[10].split("</TD")[0]
            stanWody=l.split(">")[-11].split("<")[0]
            zmianaDobowa = l.split(">")[-8].split("<")[0]

            print [rzeka,wodowskaz,strefaStanu,stanAlarmowy,przeplyw,stanWody,zmianaDobowa]

for line in dane[2].split("<TABLE")[1].split("</TR><TR>"):
    for l in line.split("</TR><TR"):
        if len(l.split(">"))>10:
            l=l.replace("<div style=\"color:red\"","").replace("</div>","")
            rzeka = l.split(">")[2].split("</TD")[0].strip()
            wodowskaz = l.split(">")[4].split("</TD")[0].strip()
            strefaStanu = l.split(">")[6].split("</TD")[0]
            stanAlarmowy = l.split(">")[8].split("</TD")[0]
            przeplyw = l.split(">")[10].split("</TD")[0]
            stanWody=l.split(">")[-11].split("<")[0]
            zmianaDobowa = l.split(">")[-8].split("<")[0]

            print [rzeka,wodowskaz,strefaStanu,stanAlarmowy,przeplyw,stanWody,zmianaDobowa]
