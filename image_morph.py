from PIL import Image
from numpy import *
from pylab import *
import os
import cv
import SimpleCV
import time

def detect(imcolor):
    # loading the classifiers
    haarFace = cv.Load('haarcascades/haarcascade_fullbody.xml')
    # running the classifiers
    storage = cv.CreateMemStorage()
    detectedFace = cv.HaarDetectObjects(imcolor, haarFace, storage)
    # eyes are always inside the face ASSUMPTION MADE IS ONLY ONE FACE IS DETECTED
    face = detectedFace[0]
    lim_x = face[0][0] + face[0][2] 
    lim_y = face[0][1] + face[0][3]
    faces = []
    ## draw a green rectangle where the face is detected
    if detectedFace:
        for face in detectedFace:
            main = face
            cv.Rectangle(imcolor,(face[0][0], face[0][1]), (face[0][0]+face[0][2], face[0][1]+face[0][3]), cv.RGB(155, 255, 25),2)
            faces.append(face)
    cv.NamedWindow('Face Detection', cv.CV_WINDOW_AUTOSIZE)
    cv.ShowImage('Face Detection', imcolor) 
    cv.WaitKey()
    return faces
    
def crop(name, image):
    imcolor = cv.LoadImage(name)
    try :
        faces = detect(imcolor)
        print faces
        if len(faces) != 1:
            assert False
        faces = faces[0]
    except:  
        print "Cannot detect face properly"
        return None
    tlx = faces[0][0]
    tly = faces[0][1]
    h = faces[0][2]
    w = faces[0][3]
    blx = tlx + w
    bly = tly + h
    border = (tlx, tly, blx, bly)
    image = image.crop(border)
    image = image.resize((100,150), Image.ANTIALIAS)
    return image
    
def average(l):
    return sum(l) / len(l)

def main():
    name = "database/bb.jpg"
    img = Image.open(name)
    crop(name, img)
if __name__ == "__main__":
    main()
