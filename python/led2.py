import RPi.GPIO as GPIO
import time
import random
 

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(pin, GPIO.OUT)
#GPIO.output(pin, GPIO.HIGH)

def setup():
    global pwm, pin
    pin = 19
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    pwm = GPIO.PWM(pin, 2000)  # set PWM pin to 2 KHz
    pwm.start(0)   # initially set to 0 duty cycle
    #try:    
     #   pwm = GPIO.PWM(pin, 2000)  # set PWM pin to 2 KHz
      #  pwm.start(0)   # initially set to 0 duty cycle
    #except RuntimeError:
     #   print("PWM ya iniciada")
    
    
    
def led(num_duty):
    decision = input("Led On/Off: ")
    if decision == "ON" or decision == "On" or decision == "on" or decision == "1":
        pwm.ChangeDutyCycle(num_duty)
    elif decision == "OFF" or decision == "Off" or decision == "off" or decision == "0":
        pwm.ChangeDutyCycle(0)
    else:
        raise KeyboardInterrupt
