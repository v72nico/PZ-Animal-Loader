import time
import PySimpleGUI as sg

def SplashScreen():
	#Splash Screen
	layout =  [[sg.Image(filename='Splash.png', key='splash')]]

	window = sg.Window('Planet Zoo Animal Loader', no_titlebar=True, keep_on_top=True).Layout(layout)
	#sg.one_line_progress_meter('title', 5, 10, key='progressmeter')
	event, values = window.Read(timeout=1000, close=True)