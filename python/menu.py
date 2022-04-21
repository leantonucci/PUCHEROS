import RPi.GPIO as GPIO
import time
import random
from led import led
from led import setup as setup_led
from stepper import motor
import sys

GPIO.setwarnings(False)

def menu_principal():
    avanzar = 0
    print("***** MENU INTERFAZ ******")
    print("(1) Mover motor")
    print("(2) Encender Led")
    print("(x) Salir")
    decision = input("Su decisión: ")
    if decision == "1":
        try: 
            motor()
        except KeyboardInterrupt:
            avanzar = 0
    elif decision == "2":
        try:
            led()
        except KeyboardInterrupt:
            avanzar = 0
    else:
        sys.exit()
    
    

if __name__ == '__main__':
    setup_led()
    while (1):
        menu_principal()