import PySimpleGUI as sg
from fileget import animallist, fileget, filegetzoo, foldersget, whatempty, whatemptylst, PATH
from onlineget import get_featured
from GameDirLst import GameDirLst, LocDirLst
from Splash import SplashScreen
import os, shutil
from OpenNaja.ZooInject import zooinject
import glob2

a=len(animallist)
b=len(animallist)-1

#get featured mod
try:
    featured = get_featured()
except:
    featured = 'none'

#get lang info
savedirfile = open('LangInfo.txt', 'r')
langcur = savedirfile.readline(20)
savedirfile.close()

#acquire data
modfolders = fileget()
zoofolders = filegetzoo()
foldersonly = foldersget(modfolders)
emptydir = whatempty(modfolders)

#read savedir.txt
savedirfile = open('SaveDir.txt', 'r')
setdir = savedirfile.readline(100)
savedirfile.close()
print(setdir)

sg.theme('Green')

animaltab = []
for i in range(0,a):
    animaltab.append([[sg.Radio(f'{foldersonly[i][k]}', str(i), size=(18, 1), font='Any 12', key='CB_'+str(i)+'_'+str(f'{k}'))] for k in range(0,len(foldersonly[i]))])

SplashScreen()

layout = [ [ sg.Button('Submit'), sg.Button('?'), sg.Button('Exit'), sg.Button('Download'), sg.Button('Uninstall a Mod'), sg.Combo(['Czech', 'Danish', 'Dutch', 'English US', 'English UK', 'French', 'German', 'Hungarian', 'Italian', 'Japanese', 'Korean', 'Norwegian', 'Polish', 'Portuguese', 'Russian', 'SimpleChinese', 'Spanish Mexico', 'Spanish Spain', 'Swedish', 'TraditionalChinese'], default_value=langcur, key='language')],
           [sg.InputText(default_text=setdir, size=(65,1), key='PlanetDir'), sg.Button(image_filename='folder.png', image_size=(20,20), key='finddir'), sg.Button('Save Directory')],
           [sg.Text('Featured Mod: '+featured)] ]

layout += [[sg.TabGroup([[sg.Tab(animallist[i], animaltab[i]) for i in range(0,a)]], tab_location='left')]]

window = sg.Window('Planet Zoo Animal Loader').Layout([[sg.Column(layout, size=(600,500), scrollable=True, vertical_scroll_only=True)]])

window.finalize()

#update empty folders to active
inuse = whatemptylst(modfolders)
for i in range(0,a):
    window['CB_'+str(i)+'_'+str(inuse[i])].Update(True)

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':           # always,  always give a way out!
        break
    if event == 'Download':
        savedirfile = open('Search.txt', 'w')
        savedirfile.truncate(0)
        savedirfile.write('All')
        savedirfile.close()
        savedirfile = open('RefreshInfo.txt', 'w')
        savedirfile.truncate(0)
        savedirfile.write('0')
        savedirfile.close()
        window.close()
        exec(open('DownloadGUI.py').read())
    if event == 'Uninstall a Mod':
        window.close()
        exec(open('Uninstallgui.py').read())
    if event == 'finddir':
        popupdir = sg.PopupGetFolder('Planet Zoo Directory', no_window=True)
        if popupdir != '':
            window['PlanetDir'].Update(popupdir)
    if event == 'Save Directory':
        savedirfile = open('SaveDir.txt', 'w')
        savedirfile.truncate(0)
        savedirfile.write(str(values['PlanetDir']))
        savedirfile.close()
    if event == '?':
        sg.Popup('Select the animal tab you want to replace. Then select the replacement mod. Press submit to finalize your mod changes. The Save Directory button saves the game directory you input. Input the language your game is in in the language selector. Open the uninstall tab with the uninstall button. Download and view mods from the internet by clicking download. Read the Readme for more info.')
    if event == 'Submit':
        #change saved lang
        savedirfile = open('LangInfo.txt', 'w')
        savedirfile.truncate(0)
        savedirfile.write(values['language'])
        savedirfile.close()
        GameDir = str(values['PlanetDir'])
        for i in range(0,b):
            #return modfiles not being used anymore
            if values['CB_'+str(i)+'_'+str(inuse[i])] == False:
                files = os.listdir(GameDir+'\\win64\\ovldata\\'+GameDirLst[i]+'\\')
                for f in files:
                    shutil.move(GameDir+'\\win64\\ovldata\\'+GameDirLst[i]+'\\'+f, modfolders[i][inuse[i]])
                for k in range(0,len(modfolders[i])):
                    if values['CB_'+str(i)+'_'+str(k)] == True:
                        #set content num
                        if i in [animallist.index('Dall Sheep'), animallist.index('Arctic Wolf'), animallist.index('Reindeer'), animallist.index('Polar Bear')]:
                            contnum = str(1)
                            contsuffix = '_Content1'
                        elif i in [animallist.index('Giant Anteater'), animallist.index('Colombian White-Faced Capuchin Monkey'), animallist.index('Jaguar'), animallist.index('Red-Eyed Tree Frog'), animallist.index('Llama')]:
                            contnum = str(2)
                            contsuffix = '_Content2'
                        else:
                            contnum = str(0)
                            contsuffix = ''
                        #set lang dir
                        locdir = LocDirLst(values['language'])
                        #inject zoopedia
                        files_as, files_ash, files_asz, files_at, files_s, files_zm, files_loc = [], [], [], [], [], [], []
                        try:
                            files_as = glob2.glob(PATH+'/Zoopedia/'+animallist[i]+'/'+foldersonly[i][k]+'\\AnimalSpecies\\'+'*.png')
                        except:
                            print('No Zoopedia Files')
                        try:
                            files_ash = glob2.glob(PATH+'/Zoopedia/'+animallist[i]+'/'+foldersonly[i][k]+'\\AnimalSpeciesHeader\\'+'*.png')
                        except:
                            print('No Zoopedia Files')
                        try:
                            files_asz = glob2.glob(PATH+'/Zoopedia/'+animallist[i]+'/'+foldersonly[i][k]+'\\AnimalSpeciesZoopedia\\'+'*.png')
                        except:
                            print('No Zoopedia Files')
                        try:
                            files_at = glob2.glob(PATH+'/Zoopedia/'+animallist[i]+'/'+foldersonly[i][k]+'\\AnimalThumbnails\\'+'*.png')
                        except:
                            print('No Zoopedia Files')
                        try:
                            files_s = glob2.glob(PATH+'/Zoopedia/'+animallist[i]+'/'+foldersonly[i][k]+'\\Species\\'+'*.png')
                        except:
                            print('No Zoopedia Files')
                        try:
                            files_zm = glob2.glob(PATH+'/Zoopedia/'+animallist[i]+'/'+foldersonly[i][k]+'\\ZoopediaMaps\\'+'*.png')
                        except:
                            print('No Zoopedia Files')
                        try:
                            files_loc = glob2.glob(PATH+'/Zoopedia/'+animallist[i]+'/'+foldersonly[i][k]+'\\Loc\\'+'*.txt')
                        except:
                            print('No Zoopedia Files')
                        if files_as != []:
                            sg.OneLineProgressMeter('Loading '+animallist[i], 0, 7, key="Guiprogress")
                            zooinject(GameDir+'\\win64\\ovldata\\Content'+contnum+'\\UI\\Textures\\AnimalSpecies'+contsuffix+'\\AnimalSpecies'+contsuffix+'.ovl', GameDir+'\\win64\\ovldata\\Content'+contnum+'\\UI\\Textures\\AnimalSpecies'+contsuffix+'\\AnimalSpecies'+contsuffix+'.ovl', files_as)
                        if files_ash != []:
                            sg.OneLineProgressMeter('Loading '+animallist[i], 1, 7, key="Guiprogress")
                            zooinject(GameDir+'\\win64\\ovldata\\Content'+contnum+'\\UI\\Textures\\AnimalSpeciesHeader'+contsuffix+'\\AnimalSpeciesHeader'+contsuffix+'.ovl', GameDir+'\\win64\\ovldata\\Content'+contnum+'\\UI\\Textures\\AnimalSpeciesHeader'+contsuffix+'\\AnimalSpeciesHeader'+contsuffix+'.ovl', files_ash)
                        if files_asz != []:
                            sg.OneLineProgressMeter('Loading '+animallist[i], 2, 7, key="Guiprogress")
                            zooinject(GameDir+'\\win64\\ovldata\\Content'+contnum+'\\UI\\Textures\\AnimalSpeciesZoopedia'+contsuffix+'\\AnimalSpeciesZoopedia'+contsuffix+'.ovl', GameDir+'\\win64\\ovldata\\Content'+contnum+'\\UI\\Textures\\AnimalSpeciesZoopedia'+contsuffix+'\\AnimalSpeciesZoopedia'+contsuffix+'.ovl', files_asz)
                        if files_at != []:
                            sg.OneLineProgressMeter('Loading '+animallist[i], 3, 7, key="Guiprogress")
                            zooinject(GameDir+'\\win64\\ovldata\\Content'+contnum+'\\UI\\Textures\\AnimalThumbnails'+contsuffix+'\\AnimalThumbnails'+contsuffix+'.ovl', GameDir+'\\win64\\ovldata\\Content'+contnum+'\\UI\\Textures\\AnimalThumbnails'+contsuffix+'\\AnimalThumbnails'+contsuffix+'.ovl', files_at)
                        if files_s != []:
                            sg.OneLineProgressMeter('Loading '+animallist[i], 4, 7, key="Guiprogress")
                            zooinject(GameDir+'\\win64\\ovldata\\Content0\\UI\\Textures\\Species\\Species.ovl', GameDir+'\\win64\\ovldata\\Content0\\UI\\Textures\\Species\\Species.ovl', files_s)
                        if files_zm != []:
                            sg.OneLineProgressMeter('Loading '+animallist[i], 5, 7, key="Guiprogress")
                            zooinject(GameDir+'\\win64\\ovldata\\Content'+contnum+'\\UI\\Textures\\ZoopediaMaps'+contsuffix+'\\ZoopediaMaps'+contsuffix+'.ovl', GameDir+'\\win64\\ovldata\\Content'+contnum+'\\UI\\Textures\\ZoopediaMaps'+contsuffix+'\\ZoopediaMaps'+contsuffix+'.ovl', files_zm)
                        if files_loc != []:
                            sg.OneLineProgressMeter('Loading '+animallist[i], 6, 7, key="Guiprogress")
                            zooinject(GameDir+'\\win64\\ovldata\\Content'+contnum+'\\Localised\\'+locdir+'Loc.ovl', GameDir+'\\win64\\ovldata\\Content'+contnum+'\\Localised\\'+locdir+'Loc.ovl', files_loc)
                        sg.OneLineProgressMeterCancel('Guiprogress')
            #add new files marked as true
            for k in range(0,len(modfolders[i])):
                files = os.listdir(modfolders[i][k])
                if values['CB_'+str(i)+'_'+str(k)] == True:
                    for f in files:
                        shutil.move(modfolders[i][k]+f, GameDir+'\\win64\\ovldata\\'+GameDirLst[i]+'\\')
		#repeat for main.ovl
        for i in [b]:
            if values['CB_'+str(b)+'_'+str(inuse[i])] == False:
                shutil.move(GameDir+'\\win64\\ovldata\\Content0\\Main.OVL', modfolders[i][inuse[i]])
            for k in range(0,len(modfolders[i])):
                files = os.listdir(modfolders[i][k])
                if values['CB_'+str(b)+'_'+str(k)] == True:
                    for f in files:
                        shutil.move(modfolders[b][k]+f, GameDir+'\\win64\\ovldata\\Content0\\')
        sg.Popup('Mods loaded. You can now start Planet Zoo.')
        break