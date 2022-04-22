import RPi.GPIO as GPIO
import time
import random
from led2 import led
from led2 import setup as setup_led
from stepper3 import motor
import sys

GPIO.setwarnings(False)
duty_cycle_led = 60
pasos_motor = 400

def menu_principal():
    avanzar = 0
    print("***** MENU INTERFAZ ******")
    print("(1) Mover motor")
    print("(2) Encender/Apagar Led Continuo")
    print("(3) Encender/Apagar Lámpara Torio-Argón")
    print("(x) Salir")
    decision = input("Su decisión: ")
    if decision == "1":
        try: 
            motor(pasos_motor)
        except KeyboardInterrupt:
            avanzar = 0
    elif decision == "2":
        try:
            led(duty_cycle_led)
        except KeyboardInterrupt:
            avanzar = 0
    elif decision == "3":
        pass
    else:
        sys.exit()
    
    

if __name__ == '__main__':
    setup_led()
    while (1):
        menu_principal()