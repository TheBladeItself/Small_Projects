#!/usr/bin/python 
import os 
import urllib.parse

search = 'google-chrome'	# 'firefox'

google = os.popen('zenity --entry --text="Enter what you want to google: " --title="google.py"').read() 
google = urllib.parse.quote(google) 
os.system(search + ' http://www.google.com/search?q=%s' % (google))  
