import PySimpleGUI as sg
from onlineget import get_titles, get_description, get_animal, get_tags, get_images, get_file
from zipfile import ZipFile
import shutil, os

#clear temp
try:
    shutil.rmtree('Temp/files')
except:
    print('No files dir')
try:
    shutil.rmtree('Temp/images')
except:
    print('No images dir')
os.mkdir('Temp/files')
os.mkdir('Temp/images')


#Search
savedirfile = open('Search.txt', 'r')
searchcur = savedirfile.readline(100)
savedirfile.close()

#refresh?
savedirfile = open('RefreshInfo.txt', 'r')
refreshinfo = savedirfile.readline(1)
savedirfile.close()

#retrieve from net
Titles = get_titles()
modnum = len(Titles)
if refreshinfo == '0':
	get_images(Titles)
Tags = []
Description = []
Animal = []
for i in range(0,modnum):
	Description.append(get_description(Titles[i]))
	Animal.append(get_animal(Titles[i]))
	Tags.append(get_tags(Titles[i]))

#set active list
Activelst = []
for i in range(0,modnum):
	for c, value in enumerate(Tags[i], 0):
		if searchcur in value:
			Activelst.append(i)
print(Activelst)

layout = [ [sg.Combo(['All', 'Exhibit Animals', 'Habitat Animals', 'Ungulates', 'Canines', 'Cats', 'Reptiles', 'Amphibians', 'Primates', 'North America', 'South America', 'Australia', 'Africa', 'Asia', 'Europe'], default_value=searchcur, key='combosearch'), sg.Button('Search')] ]
layout += [[sg.Frame(Titles[i], [ [sg.Image('Temp/images/'+Titles[i]+'.png', size=(300,300)), sg.Multiline(default_text=Description[i], disabled=True, size=(32,20))],
								[sg.Button('Download', key=Titles[i]+'_Down')] ])] for i in Activelst ]
								
window = sg.Window('Planet Zoo Animal Loader').Layout([[sg.Column(layout, size=(600,500), scrollable=True, vertical_scroll_only=True, justification="center")]])

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':           # always,  always give a way out!
        break
    if event == 'Search':
        savedirfile = open('Search.txt', 'w')
        savedirfile.truncate(0)
        savedirfile.write(str(values['combosearch']))
        savedirfile.close()
        savedirfile = open('RefreshInfo.txt', 'w')
        savedirfile.truncate(0)
        savedirfile.write('1')
        savedirfile.close()
        window.close()
        exec(open("DownloadGUI.py").read())
    for i in range(0, len(Titles)):
        if event == Titles[i]+'_Down':
            get_file(Titles[i])
            with ZipFile('Temp/files/'+Titles[i]+'.zip', 'r') as zip:
                zip.extractall('Temp/files/')
            try:
                shutil.move('Temp/files/'+Titles[i]+'/'+Titles[i], 'mods/'+Animal[i]+'/')
            except:
                sg.Popup('Mod already installed. To reinstall the mod uninstall it then download again.')
            try:
                shutil.move('Temp/files/'+Titles[i]+'/Zoopedia/'+Titles[i], 'mods/Zoopedia/'+Animal[i]+'/')
            except:
                print('no zoopedia')