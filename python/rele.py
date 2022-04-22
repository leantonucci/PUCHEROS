import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
buttonIn = 22
alto = 21
positivo = 23
signal = 24
GPIO.setup(alto,GPIO.OUT)
GPIO.setup(positivo,GPIO.OUT)
GPIO.setup(signal,GPIO.OUT)
GPIO.setup(buttonIn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.output(alto,GPIO.HIGH)
GPIO.output(positivo,GPIO.HIGH)
GPIO.output(signal,GPIO.LOW)
while True:
    if GPIO.input(buttonIn) == 1:
        GPIO.output(signal,GPIO.HIGH)
    else:
        GPIO.output(signal,GPIO.LOW)
    print("ButtonIn = ",GPIO.input(buttonIn))
    print("Signal = ",GPIO.input(signal))
    time.sleep(1)