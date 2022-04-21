import RPi.GPIO as GPIO
import time
import random
 

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(pin, GPIO.OUT)
#GPIO.output(pin, GPIO.HIGH)

def setup():
    global pwm, pin
    pin = 32
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
    
    
    
def change_color(num_duty):
    pwm.ChangeDutyCycle(num_duty)

def led():
    while 1:
        duty = input("Inserte un porcentaje de duty cycle: ")
        try:
            num_duty = int(duty)
        except ValueError:
            raise KeyboardInterrupt
        change_color(num_duty)
    
if __name__ == '__main__':
    led()
    