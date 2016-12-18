#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

folder_path = os.path.dirname(os.path.abspath(__file__))


from EmeraldAI.Logic.Modules import Global

print Global.OS


print eval('1 ^ 0')
print eval('1 ^ 1')
print eval('1 ^ 2')
print eval('1 ^ 3')

print eval('1 + 0')
print eval('1 * 4')
print eval('16 / 4')

print eval('1 * (2 + 2)')
namespace = {'__builtins__': None}
print eval('123 + 987', namespace)

import math
ns = vars(math).copy()
ns['__builtins__'] = None
print eval('cos(pi/3)', ns)

"""
#windows only
def __checkEnterPressed():
  import msvcrt
  if msvcrt.kbhit():
    key = msvcrt.getch()
    print key
    return (key == "\r")
  return False



print "gogog"
while True:
  print "."
  if __checkEnterPressed():
    break
print "the end"
"""

from EmeraldAI.Logic.KnowledgeGathering.Wikipedia import *

wp = Wikipedia()
data = wp.GetSummary("USB Kabel")
print data.encode(sys.stdout.encoding, errors='replace')


from EmeraldAI.Logic.KnowledgeGathering.Weather import *

we = Weather()

cuwe = we.GetCurrentWeather("Bad Vilbel")
print cuwe.get_wind()                  # {'speed': 4.6, 'deg': 330}
print cuwe.get_humidity()              # 87
# {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
print cuwe.get_temperature('celsius')
print cuwe.get_detailed_status()
print cuwe.get_status()
print cuwe.get_snow()
print cuwe.get_rain()
print cuwe.get_weather_icon_name()
print cuwe.get_sunrise_time('iso')  # GMT
print cuwe.get_sunset_time('iso')  # GMT


# https://docs.python.org/2/library/subprocess.html
#from subprocess import call
#call(["ls", "-l"])
#call('echo $HOME', shell=True)

#from subprocess import Popen
#instance = Popen(['open', '-a', "/Applications/VLC.app"])


"""
from string import Template

# first argument is the haarcascades path
face_cascade_path = folder_path + "/haarcascades/haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(os.path.expanduser(face_cascade_path))

scale_factor = 1.1
min_neighbors = 3
min_size = (30, 30)
flags = cv2.cv.CV_HAAR_SCALE_IMAGE

img_name = "exampleimage1"
image_path = os.path.expanduser(folder_path + "/{0}.jpg".format(img_name))
print image_path

image = cv2.imread(image_path)

faces = face_cascade.detectMultiScale(image, scaleFactor = scale_factor, minNeighbors = min_neighbors, minSize = min_size, flags = flags)
print faces
for( x, y, w, h ) in faces:
  cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 2)
  outfname = folder_path + "/%s.faces.jpg" % os.path.basename("/{0}.jpg".format(img_name))
  print outfname
  cv2.imwrite(os.path.expanduser(outfname), image)
cv2.imshow("Faces found" ,image)
cv2.waitKey(0)
"""


"""
import cv2

cascPath = folder_path + "/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    smallframe = cv2.resize(frame, (frame.shape[1]/2, frame.shape[0]/2), interpolation = cv2.INTER_CUBIC)
    cv2.imshow('Video', smallframe)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

"""


"""
import Tkinter as tk
from PIL import ImageTk, Image

#This creates the main window of an application
window = tk.Tk()
window.title("Join")
window.geometry("800x600")
window.configure(background='grey')

path = folder_path+"/exampleimage1.jpg"

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img = ImageTk.PhotoImage(Image.open(path))

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel = tk.Label(window, image = img)

#The Pack geometry manager packs widgets in rows or columns.
panel.pack(side = "bottom", fill = "both", expand = "yes")

#Start the GUI
window.mainloop()
"""

