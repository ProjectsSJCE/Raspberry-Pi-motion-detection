#import io
#import picamera
import os
import cv2
import numpy as np
#import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'

PIN = 7 #The pin where the led is supposed to be connected, the other end of led has to be connected to via a resistor(absence of which burns the led) to ground(PIN 6)
#GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
#GPIO.setup(PIN, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
TIME = 1 #this is the time in seconds the led should glow when motion is detected

FRAME_WIDTH = 150
FRAME_HEIGHT = 150
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
VIDEO_INTERVAL = 1

cam = cv2.VideoCapture(0) #Set camera parameters
# running the classifiers
faceCascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')

def detect_human(imcolor):
    
    global haarFace, storage, faceCascade  
    gray = cv2.cvtColor(imcolor, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(2, 2),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    for (tlx, tly, w, h) in faces:
        brx = tlx + w
        bry = tly + h
        border = [tlx, tly, brx, bry]
        cv2.rectangle(imcolor, (brx, bry), (tlx, tly), (0,255,0), 2)
        print type(imcolor)
        return [imcolor, border]
    return [imcolor, None]           
             
def compare_borders(prev_border, border):
    
    global TIME 
    diff = abs(border - prev_border)
    print sum(diff)
    if sum(diff) > 40:
        print "Motion detected"
#            Now turning on the led for 'TIME' seconds
#        past_time = time.now()
#        while True:
#            delta_time = int(time.now() - past_time)
#            if delta_time > TIME:
#                break
#            GPIO.output(PIN, GPIO.HIGH)# Switch on led
#        GPIO.output(PIN, GPIO.HIGH)
#        time.sleep(TIME)
#        GPIO.output(PIN, GPIO.LOW)# Switch off led
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.1, 700))
        
#Main function
def main():
    
    global cam, threshold_max, threshold_sum, FRAME_HEIGHT, FRAME_WIDTH 
    cv2.namedWindow("Differential Image", cv2.CV_WINDOW_AUTOSIZE)
    count = 0
    flag = 1	 
    motion_count = 1
    while True:
        # Create the in-memory stream
#        stream = io.BytesIO()

#        with picamera.PiCamera() as camera:
#            camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
#            camera.start_preview()
#            camera.capture(stream, format='jpeg')

#        # Construct a numpy array from the stream
#        data = np.fromstring(stream.getvalue(), dtype=np.uint8)

#        # "Decode" the image from the array, preserving colour
#        act_image = cv2.imdecode(data, 1)

        ret, act_image = cam.read()
        req_image = cv2.resize(act_image, (FRAME_WIDTH, FRAME_HEIGHT))
#        if count % 5 == 0:
        [req_image, border] = detect_human(req_image)
        if border == None:
            print "no human"
        else:
            print "detected"
        cv2.imshow("Video", req_image)
        key = cv2.waitKey(VIDEO_INTERVAL)
#            count += 1 
#        else: 
#            count += 1
#            cv2.imshow("Video", req_image)
#            key = cv2.waitKey(VIDEO_INTERVAL)
#            continue            
        #compare the coordinates of the face of the current and the previous frame
        if flag == 1 and border != None:
            prev_border = [border[i] for i in xrange(len(border))]
            flag = 0
        elif border != None:
            compare_borders(np.array(prev_border), np.array(border)) #function yet to be defined :P
            prev_border = [border[i] for i in xrange(len(border))]
        
main()
