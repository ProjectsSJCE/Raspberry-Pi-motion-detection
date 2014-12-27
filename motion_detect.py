import cv2

cam = cv2.VideoCapture(0) #Set camera parameters
#threshold_sum = 85000
threshold_max = 180

#Gets the differential images given the previous, current and the next frame
def get_differential_image(frame_before, frame_now, frame_after):

    differential_1 = cv2.absdiff(frame_after, frame_now)
    differential_2 = cv2.absdiff(frame_now, frame_before)
    return cv2.bitwise_and(differential_1, differential_2)
	 
#Gets the initial three consecutive frames
def get_three_frames():

    global cam
    frame_before = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    frame_now = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    frame_after = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    return [frame_before, frame_now, frame_after]
    
#Main function
def main():

    
    global cam, threshold_max, threshold_sum 
    cv2.namedWindow("Differential Image", cv2.CV_WINDOW_AUTOSIZE)
	     
    #Capture initial three frames and convert them to RGB
    [frame_before,frame_now, frame_after] = get_three_frames()
    

#    print len(req_image)
#    print len(req_image[0])
    count = 0	 

    while True:

#       Getting the differential image
        req_image = get_differential_image(frame_before, frame_now, frame_after)

#        Calculate sum, minimum and maximum of the pixel values of the differential image
        sum_image = req_image.sum()
        minimum = req_image.min()
        maximum = req_image.max()
        
#        print "sum ", sum_image
#        print "min ", minimum
#        print "max", maximum
        
#        if maximum value of the differential image is greater than the threshold of maximum value, declare that there is motion
        if maximum > threshold_max: #This threshold value has to be adjusted based on the sensitivity required
            print "motion", count
            print "max ", maximum
            count += 1
            
        
        cv2.imshow("Differential Image", req_image )
        
#       Capture next frame (i.e., shift right)
        frame_before = frame_now
        frame_now = frame_after
        frame_after = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
	     
        key = cv2.waitKey(10)

main()
