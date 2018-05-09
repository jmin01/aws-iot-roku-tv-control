#Required packages: roku - https://pypi.python.org/pypi/roku
import time
import datetime
import os
from roku import Roku
import json

#Variables
tvIpAddress = '##IP ADDRESS OF TV##'
buttonObjectFilePath = '/home/pi/iot/buttonclicktype'
rokutv = Roku(tvIpAddress)
AVinput = rokutv['AV']
HDMITVinput = rokutv['tvinput.hdmi1']

#Give Node-RED enough time to write to buttonclicktype file
time.sleep(.25)

#If it’s a single button click, change the TV input to AV
#If it’s a long button click, change the TV input to HDMI 1
#If it’s a double button click, turn off the TV
buttonClickJSON = open(buttonObjectFilePath)
buttonClickData = json.load(buttonClickJSON)
buttonClickType = buttonClickData["clickType"]
buttonClickJSON.close()

if buttonClickType == 'SINGLE':
	AVinput.launch()
	print str(datetime.datetime.now()) + ": Changing TV Input to AV"
elif buttonClickType == 'LONG':
	HDMITVinput.launch()
	print str(datetime.datetime.now()) + ": Changing TV Input to HDMI 1"
else:
	rokutv._post('/keypress/Power')
	print str(datetime.datetime.now()) + ": Turning Off TV"
