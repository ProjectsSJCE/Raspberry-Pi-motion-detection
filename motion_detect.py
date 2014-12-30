import cv2
import cv
import numpy as np
from PIL import Image
from pylab import *

cam = cv2.VideoCapture(0) #Set camera parameters
#threshold_sum = 85000
threshold_max = 180

#Gets the differential images given the previous, current and the next frame
def get_differential_image(frame_before, frame_now, frame_after):

    differential_1 = cv2.absdiff(frame_after, frame_now)
    differential_2 = cv2.absdiff(frame_now, frame_before)
    return cv2.bitwise_and(differential_1, differential_2)
	
def detect_human(imcolor):
    
    haarFace = cv.Load('haarcascade_profileface.xml')
    # running the classifiers
    storage = cv.CreateMemStorage()
    cvmat_array = cv.fromarray(imcolor)
    detectedFace = cv.HaarDetectObjects(cvmat_array, haarFace, storage)
    # eyes are always inside the face ASSUMPTION MADE IS ONLY ONE FACE IS DETECTED
#    faces = detectedFace[0]
#    lim_x = face[0][0] + face[0][2] 
#    lim_y = face[0][1] + face[0][3]
#    faces = []
    ## draw a green rectangle where the face is detected
#    if detectedFace:
#        for face in detectedFace:
#            main = face
##            cv2.Rectangle(imcolor,(face[0][0], face[0][1]), (face[0][0]+face[0][2], face[0][1]+face[0][3]), cv2.RGB(155, 255, 25),2)
#            faces.append(face)
    try :
        faces = detectedFace[0]
    except:  
        print "Cannot detect face properly"
        return None
    tlx = faces[0][0]
    tly = faces[0][1]
    h = faces[0][2]
    w = faces[0][3]
    brx = tlx + w
    bry = tly + h
#    border = (tlx, tly, blx, bly)
#    imcolor = np.array(imcolor)
#    imcolor = imcolor[tlx:brx][tly:bry]
#    image = imcolor
    cv2.rectangle(imcolor, (brx, bry), (tlx, tly), (0,255,0), 2)
    print type(imcolor)
    return imcolor           
             
#Gets the initial three consecutive frames
def get_three_frames():

    global cam
    ret, frame_before = cam.read()
#    ret, frame_now = cam.read()
#    ret, frame_after = cam.read()
    frame_before = detect_human(frame_before)
#    frame_now = detect_human(frame_now)
#    frame_after = detect_human(frame_after)
#    frame_before = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
#    frame_now = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
#    frame_after = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    return [frame_before, frame_now, frame_after]
    
#Main function
def main():

    
    global cam, threshold_max, threshold_sum 
    cv2.namedWindow("Differential Image", cv2.CV_WINDOW_AUTOSIZE)
	     
    #Capture initial three frames and convert them to RGB
#    [frame_before,frame_now, frame_after] = get_three_frames()
    

#    print len(req_image)
#    print len(req_image[0])
    count = 0	 

    while True:
    
        ret, req_image = cam.read()
        req_image = detect_human(req_image)
#       Getting the differential image
#        req_image = get_differential_image(frame_before, frame_now, frame_after)

#        Calculate sum, minimum and maximum of the pixel values of the differential image
#        sum_image = req_image.sum()
#        minimum = req_image.min()
#        maximum = req_image.max()
        
##        print "sum ", sum_image
##        print "min ", minimum
##        print "max", maximum
        
#        if maximum value of the differential image is greater than the threshold of maximum value, declare that there is motion
#        if maximum > threshold_max: #This threshold value has to be adjusted based on the sensitivity required
#            print "motion", count
#            print "max ", maximum
#            count += 1
#        print type(req_image)
        
        if req_image != None:
            cv2.imshow("Differential Image", req_image )
            
    #       Capture next frame (i.e., shift right)
    #        frame_before = frame_now
    #        frame_now = frame_after
    #        frame_after = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
	         
            key = cv2.waitKey(10)

main()
