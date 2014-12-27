import cv2
import numpy as np
threshold = 90000
def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)
	 
cam = cv2.VideoCapture(0)
	 
winName = "Movement Indicator"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)
	 
	# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
new_image = diffImg(t_minus, t, t_plus)
print len(new_image)
print len(new_image[0])
count = 0	 
while True:
    old_image = new_image
    new_image = diffImg(t_minus, t, t_plus)

    diff = sum(sum(abs(new_image - old_image)))
    
#    changed = 0
#    for x in np.nditer(diff):
#        for y in np.nditer(diff[0]):
#            if diff[x][y] > threshold:
#                changed += 1
#    print changed
    print diff
    if diff > threshold:
        print "motion", count
        count += 1
        
    
    cv2.imshow( winName, new_image )
    
	  # Read next image
    t_minus = t
    t = t_plus
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
	 
    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(winName)
        break
