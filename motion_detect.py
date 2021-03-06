import io
import picamera
import os
import cv2
import numpy as np
import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'
import smtplib
import email
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
no_mail = 1

#Threshold for saying that motion has been detected. 
threshold_max = 120

PIN = 7 #The pin where the led is supposed to be connected, the other end of led has to be connected to via a resistor(absence of which burns the led) to ground(PIN 6)
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setup(PIN, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
TIME = 1 #this is the time in seconds the led should glow when motion is detected

#Size to which the frame has to be reduced and processed
FRAME_WIDTH = 150
FRAME_HEIGHT = 150

#Parameters for the resolution of the image being captured
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

send_to = str(raw_input("Enter your email ID, example john@gmail.com"))
image_no = 1
#Logging into fullfake01@gmail.com
try:
    s = smtplib.SMTP('smtp.gmail.com:587') #smtp.gmail because it has to login to gmail mailing service.
    s.starttls() #start
except:
    print "Network Error"

#logging into motionproject2015@gmail.com
try:
    print "logging in:"
    s.login('motionproject2015@gmail.com','raspberrypi')
    print "logged in"
except:
    print "Couldn't login"
    
    
#cam = cv2.VideoCapture(0) #Set camera parameters

# Setting the classifier upperbody
faceCascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')

#Function for differential image
def get_differential_image(frame_before, frame_now, frame_after):
    differential_1 = cv2.absdiff(frame_after, frame_now)
    differential_2 = cv2.absdiff(frame_now, frame_before)
    return cv2.bitwise_and(differential_1, differential_2)

def get_image():
    stream = io.BytesIO()

    #Setup pi camera for capturing video
    with picamera.PiCamera() as camera:
        camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
        camera.start_preview()
        # capture frame
        camera.capture(stream, format='jpeg')

#        # Construct a numpy array from the stream
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)

#        # "Decode" the image from the array, preserving colour
    act_image = cv2.imdecode(data, 1)
    return act_image

#Function which detects a human in a frame and return an image with a box drawn around the human and his coordinates
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
#        print type(imcolor)
        return [imcolor, border]
    return [imcolor, None]           

#Function which compares the current and previous location of the human detected
#If difference of locations is > 24, it classifies it as motion             
def compare_borders(prev_border, border, req_image):
    
    global TIME, s, send_to 
    diff = abs(border - prev_border)
#    print sum(diff)
    if sum(diff) > 24:
        print "Human intruder detected"
#            Now turning on the led for 'TIME' seconds
#        past_time = time.now()
#        while True:
#            delta_time = int(time.now() - past_time)
#            if delta_time > TIME:
#                break
#            GPIO.output(PIN, GPIO.HIGH)# Switch on led
        GPIO.output(PIN, GPIO.HIGH)
        time.sleep(TIME)
        GPIO.output(PIN, GPIO.LOW)# Switch off led
#        save frame as image.jpg
        cv2.imwrite("image.jpg", req_image)
#        cv2.imwrite("image" + str(image_no) + ".jpg", req_image)

#        Create an attachment for image.jpg
        try:
            #Mail details
            msg = email.mime.Multipart.MIMEMultipart()
            msg['Subject'] = "Motion detected"
            msg['From'] = 'motionproject2015@gmail.com'
            msg['To'] = send_to


            # Image attachment
            filename = "image.jpg"
#            filename = "image" + str(image_no) + ".jpg"
            fp=open(filename,'rb')
            #create mime image object
            img = MIMEImage(fp.read())
            fp.close()
            #attach mail
            msg.attach(img)
            print "File attached"
    #        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.1, 700))
            s.sendmail('motionproject2015@gmail.com',[send_to], msg.as_string())
            print "sent"
        except:
            print "couldn't mail, sorry."
            cv2.imwrite("image_couldn't_mail" + str(no_mail) + ".jpg", req_image)
            no_mail += 1
        image_no += 1
            
#Main function
def main():
    #global variables being used
    global cam, threshold_max, threshold_sum, FRAME_HEIGHT, FRAME_WIDTH, send_to 
        
    cv2.namedWindow("Differential Image", cv2.CV_WINDOW_AUTOSIZE)
    count = 0
    flag = 1	 
    motion_count = 1
    
#    Capture first three frames
    frame_before = get_image()
    frame_now = get_image()
    frame_after = get_image()
    frame_before = cv2.cvtColor(frame_before, cv2.COLOR_RGB2GRAY)
    frame_now = cv2.cvtColor(frame_now, cv2.COLOR_RGB2GRAY)
    frame_after = cv2.cvtColor(frame_after, cv2.COLOR_RGB2GRAY)
    
    while True:
        
        # Getting the differential image
        req_image = get_differential_image(frame_before, frame_now, frame_after)
        
        # Calculate sum, minimum and maximum of the pixel values of the differential image
#        sum_image = req_image.sum()
#        minimum = req_image.min()
        maximum = req_image.max()
        # print "sum ", sum_image
        # print "min ", minimum
        # print "max", maximum
        
        # if maximum value of the differential image is greater than the threshold of maximum value, declare that there is motion
        if maximum > threshold_max: #This threshold value has to be adjusted based on the sensitivity required
            print "motion detected"
            GPIO.output(PIN, GPIO.HIGH)
            time.sleep(TIME)
            GPIO.output(PIN, GPIO.LOW)# Switch off led
#            print "max ", maximum
            count += 1

        # Capture next frame (i.e., shift right)
        frame_before = frame_now
        frame_now = frame_after

        # Create the in-memory stream
        stream = io.BytesIO()

        #Setup pi camera for capturing video
        with picamera.PiCamera() as camera:
            camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
            camera.start_preview()
            # capture frame
            camera.capture(stream, format='jpeg')

#        # Construct a numpy array from the stream
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)

#        # "Decode" the image from the array, preserving colour
        act_image = cv2.imdecode(data, 1)
        frame_after = cv2.cvtColor(act_image, cv2.COLOR_RGB2GRAY)


#        ret, act_image = cam.read()
        #Resize the image
        req_image = cv2.resize(act_image, (FRAME_WIDTH, FRAME_HEIGHT))
        #Perform human detection on one of five frames for real-time output
        if count % 5 == 0:
            [req_image, border] = detect_human(req_image)
            count += 1 
        else: 
            count += 1
            continue

        #tells if human is present in a given frame or not  
#        if border == None:
#            print "no human"
#        else:
#            print "human"

        #compare the coordinates of the human of the current and the previous frame
        if flag == 1 and border != None:#Very first frame
            prev_border = [border[i] for i in xrange(len(border))]
            flag = 0
        elif border != None:#Call compare_borders on two locations
            compare_borders(np.array(prev_border), np.array(border), req_image)
            prev_border = [border[i] for i in xrange(len(border))]

main()
