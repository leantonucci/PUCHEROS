import RPi.GPIO as io
io.setmode(io.BOARD)
import sys, tty, termios, time
from getch import getch

delay = 3E-004              # By playing with this delay you can influence the rotational speed.
pulses_per_rev = 10        # This can be configured on the driver using the DIP-switches


# This section of code defines the methods used to determine
# whether the stepper motor needs to spin forward or backwards. 
# Different directions are acheived by setting the
# direction GPIO pin to true or to false. 
# My driver required:
#   DIR must be ahead of PUL effective edge by 5 micro-s to ensure correct direction;
#   Pulse width not less than 2.5 micro-s;
#   Pulse low-level width not less than 2.5 micro-s.

def stepper_enable():
    io.output(motor_enable_pin, False)

def stepper_disable():
    io.output(motor_enable_pin, True)

def step_once():
    io.output(motor_step_pin, True)
    time.sleep(delay)
    io.output(motor_step_pin, False)
    time.sleep(delay)

def step_forward():
    io.output(motor_direction_pin, True)
    time.sleep(delay)
    step_once()
        

def step_reverse():
    io.output(motor_direction_pin, False)
    time.sleep(delay)
    if io.input(limit_switch_pin)==0:
        step_once()
    

def setup_dm542():
    global motor_enable_pin, motor_direction_pin, motor_step_pin, limit_switch_pin, limit_switch_common
    # This blocks of code defines the three GPIO
    # pins used for the stepper motor
    motor_enable_pin = 18
    motor_direction_pin = 11
    motor_step_pin = 13
    limit_switch_pin = 22
    limit_switch_common = 21
    io.setup(motor_enable_pin, io.OUT)
    io.setup(motor_direction_pin, io.OUT)
    io.setup(motor_step_pin, io.OUT)
    io.setup(limit_switch_pin, io.IN, pull_up_down=io.PUD_DOWN)
    io.setup(limit_switch_common, io.OUT)
    io.output(limit_switch_common, True)
    # Setting the stepper pins to false so the motors will not move
    # until the user presses the first key
    io.output(motor_enable_pin, False)
    io.output(motor_step_pin, False)


    

def loop_dm542(delay, pulses_per_rev):
    print("*******Calibration Mirror Motor Control Program: Started*******")
    print("Instructions: ")
    # Print instructions for when the user has an interface
    print("e/d: enable/disable")
    print("f/r: step forward / reverse")
    print("g/t: rotate forward / reverse")
    print("p: custome number of steps")
    print("x: exit")
    # Infinite loop that will not end until the user presses the
    # exit key
    stepper_enable()
    while True:
        print(io.input(limit_switch_pin))
        if io.input(limit_switch_pin)==1:
            print("The mirror motor is activating the limit switch on the interface wall, turn the direction back")
        print("Choose an option: ")
                # Keyboard character retrieval method is called and saved
        # into variable
        char = getch()
        print(char)
        
        # The stepper will be enabled when the "e" key is pressed
        if (char == "e"):
            stepper_enable()

        # The stepper will be disabled when the "d" key is pressed
        if (char == "d"):
            stepper_disable()

        # The "f" key will step the motor forward
        if (char == "f"):
            step_forward()

        # The "r" key will step the motor in reverse
        if (char == "r"):
            step_reverse()

        # The "g" key will step the motor 1 rotation forwards
        if (char == "g"):
            for x in range(0, pulses_per_rev):
                step_forward()

        # The "t" key will step the motor 1 rotation in reverse
        if (char == "t"):
            for x in range(0, pulses_per_rev):
                step_reverse()
                
        if (char == "c"):
            str_custom_steps = input("Choose a number of steps: ")
            custom_steps = int(str_custom_steps)
            if custom_steps > 0:
                print(custom_steps)
                for i in range(0,custom_steps):
                    step_forward()
            else:
                print(custom_steps)
                neg_custom_steps = -1*custom_steps
                for i in range(neg_custom_steps):
                    step_reverse()
            

        # The "x" key will break the loop and exit the program
        if (char == "x"):
            print("*******Calibration Mirror Motor Control Program: Ended*******")
            raise KeyboardInterrupt
            break

        # The keyboard character variable will be set to blank, ready
        # to save the next key that is pressed
        char = ""

    # Program will cease all GPIO activity before terminating
    io.cleanup()
    
def motor(delay, pulse_per_rev):
    setup_dm542()
    loop_dm542(delay,pulse_per_rev)
