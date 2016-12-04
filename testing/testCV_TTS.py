#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import cv2
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')
from EmeraldAI.Logic.ComputerVision import *

from EmeraldAI.Logic.SpeechProcessing.Ivona import *

myCV = ComputerVision()
ivona = Ivona()
audioPlayer = Config().Get("TextToSpeech", "AudioPlayer") + " '{0}'"


def img_message(img_num):
    switcher = {
        0: "Schauen Sie bitte normal in die Kamera",
        1: "Lächeln bitte!",
        2: "Und jetzt ein wenig traurig schauen",
        3: "Als nächstes wäre ein überraschter Gesichtsausdruck nötig",
        4: "Bitte leicht nach rechts schauen",
        5: "und nun leicht nach links",
        6: "Fast geschafft! Schauen Sie bitte etwas nach oben",
        7: "und nun leicht nach unten",
        8: "Super! Jetzt bitte den kopf leicht schräg nach rechts drehen",
        9: "und das selbe mit links",
        10: "Zum Schluss bitte die Augen schließen"
    }
    return switcher.get(img_num, "nothing")


def img_name(img_num):
    switcher = {
        0: "normal",
        1: "happy",
        2: "sad",
        3: "suprised",
        4: "looking_right",
        5: "looking_left",
        6: "looking_up",
        7: "looking_down",
        8: "left_light",
        9: "right_light",
        10: "eyes_closed"
    }
    return switcher.get(img_num, "nothing")


def talk(textToSpeek):
    audioPath = ivona.Speak(textToSpeek)
    print "Playing file: '{0}'".format(audioPath)
    #os.system(audioPlayer.format(audioPath).replace('/', '\\'))
    os.system(audioPlayer.format(audioPath))


camera = cv2.VideoCapture(0)
ret = camera.set(3, 320)
ret = camera.set(4, 240)
talk('Hallo, ich werde in der kommenden Minute Ihr Gesicht lernen. Bitte tippen Sie Ihren Namen ein')
name = raw_input('Please enter your name: ')
talk('Danke ' + name)

max_img_num = 0

# Create the directory for positive training images if it doesn't exist.
img_dir = myCV.GetTrainingImageDir() + name
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
else:
    for root, dirs, filenames in os.walk(img_dir):
        for f in filenames:
            tmp_num = re.findall('\d+|$', f)[0]
            if(tmp_num > max_img_num):
                max_img_num = tmp_num

img_num = max_img_num

while img_num < 11:
    # Show the capture window
    talk(img_message(img_num))
    image = myCV.CapturePerson(camera, '')

    # Get coordinates of single face in captured image.
    result = myCV.DetectFaceInImage(image)

    if result is None:
        continue

    x, y, w, h = result
    # Crop image as close as possible to desired face aspect ratio.
    # Might be smaller if face is near edge of image.
    img_crop = myCV.CropImage(image, x, y, w, h)
    # Save image to file.
    filename = os.path.join(img_dir, '%02d_%s_%s.pgm' %
                            (img_num, name, img_name(img_num)))
    cv2.imwrite(filename, img_crop)
    talk('Ich habe das Bild gespeichert')
    img_num += 1

# No Enter 2 Eyes
while img_num < 25:
    image = myCV.CapturePerson(camera, '', False, True, True)

    # Get coordinates of single face in captured image.
    result = myCV.DetectFaceInImage(image)
    if result is None:
        continue

    x, y, w, h = result
    # Crop image as close as possible to desired face aspect ratio.
    # Might be smaller if face is near edge of image.
    img_crop = myCV.CropImage(image, x, y, w, h)
    # Save image to file.
    filename = os.path.join(img_dir, '%02d_%s_auto.pgm' % (img_num, name))
    cv2.imwrite(filename, img_crop)
    #talk ('Und schon wieder ein gespeichertes Bild')
    img_num += 1

# No Enter No Eyes
while img_num < int(max_img_num) + 50:
    image = myCV.CapturePerson(camera, '', False, True, False)

    # Get coordinates of single face in captured image.
    result = myCV.DetectFaceInImage(image)
    if result is None:
        continue

    x, y, w, h = result
    # Crop image as close as possible to desired face aspect ratio.
    # Might be smaller if face is near edge of image.
    img_crop = myCV.CropImage(image, x, y, w, h)
    # Save image to file.
    filename = os.path.join(img_dir, '%02d_%s_auto.pgm' % (img_num, name))
    cv2.imwrite(filename, img_crop)
    #talk ('Das Bild habe ich gespeichert')
    img_num += 1

talk("Das wars mit dem training, Danke für Ihre Zeit!")
cv2.destroyAllWindows()
