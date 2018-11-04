import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT)
print "on"
GPIO.output(12,GPIO.LOW)

time.sleep(2)
print "off"
GPIO.output(12, GPIO.HIGH)
time.sleep(3)
print "on"
GPIO.output(12, GPIO.LOW)
time.sleep(1)
print "off"
GPIO.output(12, GPIO.HIGH)
GPIO.cleanup()
