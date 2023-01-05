import RPi.GPIO as GPIO
import time
import random
from led2 import led
from led2 import setup as setup_led
from stepper_driver_dm542_v2 import motor
from rele2 import lampara
import sys

GPIO.setwarnings(False)
duty_cycle_led = 100
delay = 3E-004              # By playing with this delay you can influence the rotational speed.
pulses_per_rev = 6000       # This can be configured on the driver using the DIP-switches


def menu_principal():
    avanzar = 0
    print("*******Interface Menu********")
    print("(1) Move stepper motor")
    print("(2) Turn On/Off White Led")
    print("(3) Turn On/Off Thorium-Argon Lamp")
    print("(x) Exit")
    decision = input("Your choice: ")
    if decision == "1":
        try: 
            motor(delay, pulses_per_rev)
        except KeyboardInterrupt:
            avanzar = 0
    elif decision == "2":
        try:
            led(duty_cycle_led)
        except KeyboardInterrupt:
            avanzar = 0
    elif decision == "3":
        try: 
            lampara()
        except KeyboardInterrupt:
            avanzar = 0
    else:
        sys.exit()
    
    

if __name__ == '__main__':
    setup_led()
    while (1):
        menu_principal()