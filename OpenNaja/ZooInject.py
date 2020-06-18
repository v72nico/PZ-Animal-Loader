from OpenNaja.ovl_tool_gui import MainWindow
import sys

def zooinject(filepath, filepathdest, injectfile):
	#filepath = 'C:\\Users\\Matias\\Desktop\\planet zoo modding\\Animal Loader\\Planet Mod loader\\New folder\\Loc.ovl'
	#filepathdest = 'C:\\Users\\Matias\\Desktop\\planet zoo modding\\Animal Loader\\Planet Mod loader\\New folder (2)\\Loc.ovl'
	#injectfile = ['C:\\Users\\Matias\\Desktop\\planet zoo modding\\Animal Loader\\Planet Mod loader\\New folder (2)\\zoopedia_socialneedsdescription_reindeer.txt']
	a = MainWindow()
	a.load_ovl(filepath)
	a.inject(injectfile)
	a.save_ovl(filepathdest)