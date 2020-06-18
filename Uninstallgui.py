import PySimpleGUI as sg
from fileget import animallist, fileget, foldersget, whatempty, whatemptylst, filegetzoo, PATH
from GameDirLst import GameDirLst
import shutil
import os

b=len(animallist)-1

#acquire data
modfolders = fileget()
zoofolders = filegetzoo()
foldersonly = foldersget(modfolders)
emptydir = whatempty(modfolders)

#read savedir.txt
savedirfile = open('SaveDir.txt', 'r')
GameDir = str(savedirfile.readline(100))
savedirfile.close()

animaltab = []
for i in range(0,b):
    animaltab.append([[sg.Checkbox(f'{foldersonly[i][k]}', str(i), size=(18, 1), font='Any 12', key='UNCB_'+str(i)+'_'+str(f'{k}'))] for k in range(0,len(modfolders[i]))])

layout = [[sg.Button('Unselect All'), sg.Button('Uninstall Selected')]]
layout += [[sg.TabGroup([[sg.Tab(animallist[i], animaltab[i]) for i in range(0,b)]], tab_location='left')]]

window = sg.Window('Planet Zoo Animal Loader').Layout([[sg.Column(layout, size=(600,500), scrollable=True, vertical_scroll_only=True)]])

window.finalize()

#Update All to false
for i in range(0,b):
	for k in range(0,len(foldersonly[i])):
		window['UNCB_'+str(i)+'_'+str(k)].Update(False)

inuse = whatemptylst(modfolders)

while True:
	event, values = window.Read()
	if event is None or event == 'Exit':           # always,  always give a way out!
		break
	if event == 'Unselect All':
		for i in range(0,b):
			for k in range(0,len(foldersonly[i])):
				window['UNCB_'+str(i)+'_'+str(k)].Update(False)
	if event == 'Uninstall Selected':
		ConfirmUn = sg.PopupOKCancel('Are you sure you want to uninstall the selected mods?')
		if ConfirmUn == 'OK':
			for i in range(0,b):
				if values['UNCB_'+str(i)+'_'+str(inuse[i])] == True:
					selectedlst = []
					Counter = 0
					for k in range(0,len(foldersonly[i])):
						if values['UNCB_'+str(i)+'_'+str(k)] == True:
							Counter = Counter+1
					print(Counter)
					if (len(foldersonly[i])-Counter) == 0:
						sg.Popup("Can't uninstall. You won't have any versions of this animal left.")
						break
					if (len(foldersonly[i])-Counter) != 0:
						#Return mod files for deletion
						files = os.listdir(GameDir+'\\win64\\ovldata\\'+GameDirLst[i]+'\\')
						for f in files:
							shutil.move(GameDir+'\\win64\\ovldata\\'+GameDirLst[i]+'\\'+f, modfolders[i][inuse[i]])
						for k in range(0,len(modfolders[i])):
							if values['UNCB_'+str(i)+'_'+str(k)] == False:
								files = os.listdir(modfolders[i][k])
								for f in files:
									shutil.move(modfolders[i][k]+f, GameDir+'\\win64\\ovldata\\'+GameDirLst[i]+'\\')
								break
				#Delete time
				for k in range(0,len(modfolders[i])):
					if values['UNCB_'+str(i)+'_'+str(k)] == True:
						print('deleteing')
						shutil.rmtree(modfolders[i][k])
						try:
							shutil.rmtree(PATH+'/Zoopedia/'+animallist[i]+'/'+foldersonly[i][k])
						except:
							print('no zoopedia files')
			sg.Popup('Uninstall Complete')
			window.close()
			break