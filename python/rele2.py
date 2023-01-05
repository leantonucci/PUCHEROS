import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

def setup():
    global positivo, signal
    GPIO.setmode(GPIO.BOARD)
    positivo = 23
    signal = 24
    GPIO.setup(positivo,GPIO.OUT)
    GPIO.setup(signal,GPIO.OUT)
    GPIO.output(positivo,GPIO.HIGH)

def rele():
    print("*******Thorium/Argon Lamp Control Program: Started*******")
    print("Write down On/Off to turn on/off the lamp")
    while True:
        decision = input("Your choice: ")
        if decision=="ON" or decision == "On" or decision == "on" or decision == "1":
            GPIO.output(signal,GPIO.HIGH)
        elif decision=="OFF" or decision == "Off" or decision == "off" or decision == "0":
            GPIO.output(signal,GPIO.LOW)
        else:
            print("*******Thorium/Argon Lamp Control Program: Ended*******")
            raise KeyboardInterrupt

def lampara():
    setup()
    rele()
