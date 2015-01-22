import RPi.GPIO as GPIO #
import time

PIN = 7 #The pin where the led is supposed to be connected, the other end of led has to be connected to via a resistor(absence of which burns the led) to ground(PIN 6)
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(PIN, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
TIME = 1 #this is the time in seconds the led should glow when motion is detected
past_time = time.now()
GPIO.output(PIN, GPIO.HIGH)# Switch on led
time.sleep(TIME)
GPIO.output(PIN, GPIO.LOW)# Switch off led
