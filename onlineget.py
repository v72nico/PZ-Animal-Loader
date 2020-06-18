import urllib.request as on
import PySimpleGUI as sg

def get_featured():
    link = "http://www.worldofzt2.com/planet/featured"
    f = on.urlopen(link)
    featuredold = str(f.read())
    featured = featuredold[2:][:-1]
    return featured
	
def get_titles():
	link = "http://www.worldofzt2.com/planet/titles"
	f = on.urlopen(link)
	text = str(f.read())
	textlst = text.split("&#39;")
	finallst = []
	finalfinallst = []
	for i in range(0, len(textlst)):
		if i % 2 != 0:
			finallst.append(textlst[i])
	for i in range(0, len(finallst)):
		if i % 2 != 0:
			finalfinallst.append(finallst[i])
	return finalfinallst

def get_description(title):
	link = "http://www.worldofzt2.com/planet/mods/"+str(title)
	f = on.urlopen(link)
	text = str(f.read())
	textlst = text.split("&quot;")
	finaltext = textlst[1].replace('&#39;', "'")
	return finaltext

def get_animal(title):
    link = "http://www.worldofzt2.com/planet/mods/"+str(title)
    f = on.urlopen(link)
    text = str(f.read())
    textlst = text.split("animal&#39;: &#39;")
    finaltext = textlst[1].split("&#39;")
    return finaltext[0]

def get_tags(title):
	link = "http://www.worldofzt2.com/planet/mods/"+str(title)
	f = on.urlopen(link)
	text = str(f.read())
	textlst = text.split("tags&#39;: &#39;")
	finallst = textlst[1].split("&#39;")
	finalfinallst = finallst[0].split(",")
	return finalfinallst

def get_images(titles):
	for i in range(0, len(titles)):
		sg.OneLineProgressMeter('Getting Download Info', i, len(titles), key="progress")
		link = "http://www.worldofzt2.com/media/planet/images/"+titles[i]+".png"
		on.urlretrieve(link, 'Temp//images//'+titles[i]+".png")
	sg.OneLineProgressMeterCancel('progress')
		
def get_file(title):
	link = "http://www.worldofzt2.com/media/planet/mods/"+title+".zip"
	def update(blocks, bs, size):
		sg.OneLineProgressMeter('Downloading '+title, blocks*8060, size, key="DownloadBar")
	on.urlretrieve(link, 'Temp//files//'+title+".zip", reporthook = update)
	sg.OneLineProgressMeterCancel('DownloadBar')




