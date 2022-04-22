import RPi.GPIO as GPIO
import time

def setup():
    global out1,out2,out3,out4,ena,enb,i,positive,negative,y, buttonIn, alto
    out1 = 13
    out2 = 11
    out3 = 15
    out4 = 12
    ena = 16
    enb = 18
    i=0
    positive=0
    negative=0
    y=0
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(out1,GPIO.OUT)
    GPIO.setup(out2,GPIO.OUT)
    GPIO.setup(out3,GPIO.OUT)
    GPIO.setup(out4,GPIO.OUT)
    GPIO.setup(ena,GPIO.OUT)
    GPIO.setup(enb,GPIO.OUT)
    
    buttonIn = 22
    alto = 21
    GPIO.setup(alto,GPIO.OUT)
    GPIO.setup(buttonIn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.output(alto,GPIO.HIGH)

def move(pasos_motor,out1,out2,out3,out4,i,positive,negative,y, buttonIn, alto):
    try:
       while(1):
          print(GPIO.input(buttonIn))
          time.sleep(1)
          GPIO.output(out1,GPIO.LOW)
          GPIO.output(out2,GPIO.LOW)
          GPIO.output(out3,GPIO.LOW)
          GPIO.output(out4,GPIO.LOW)
          GPIO.output(ena,GPIO.HIGH)
          GPIO.output(enb,GPIO.HIGH)
          x1= input("Mover motor a ON/OFF: ")
          if x1 == "ON" or x1 == "on" or x1 == "1":
              x = pasos_motor
          elif x1 == "OFF" or x1 == "Off" or x1 == "off" or x1 == "0":
              x = -1*pasos_motor
          else:
              raise KeyboardInterrupt
          if x>0 and x<=400:
              for y in range(x,0,-1):
                  if negative==1:
                      if i==7:
                          i=0
                      else:
                          i=i+1
                      y=y+2
                      negative=0
                  positive=1
                  #print((x+1)-y)
                  if GPIO.input(buttonIn)==0:
                      if i==0:
                          GPIO.output(out1,GPIO.HIGH)
                          GPIO.output(out2,GPIO.LOW)
                          GPIO.output(out3,GPIO.LOW)
                          GPIO.output(out4,GPIO.LOW)
                          time.sleep(0.03)
                          #time.sleep(1)
                      elif i==1:
                          GPIO.output(out1,GPIO.HIGH)
                          GPIO.output(out2,GPIO.HIGH)
                          GPIO.output(out3,GPIO.LOW)
                          GPIO.output(out4,GPIO.LOW)
                          time.sleep(0.03)
                          #time.sleep(1)
                      elif i==2:  
                          GPIO.output(out1,GPIO.LOW)
                          GPIO.output(out2,GPIO.HIGH)
                          GPIO.output(out3,GPIO.LOW)
                          GPIO.output(out4,GPIO.LOW)
                          time.sleep(0.03)
                          #time.sleep(1)
                      elif i==3:    
                          GPIO.output(out1,GPIO.LOW)
                          GPIO.output(out2,GPIO.HIGH)
                          GPIO.output(out3,GPIO.HIGH)
                          GPIO.output(out4,GPIO.LOW)
                          time.sleep(0.03)
                          #time.sleep(1)
                      elif i==4:  
                          GPIO.output(out1,GPIO.LOW)
                          GPIO.output(out2,GPIO.LOW)
                          GPIO.output(out3,GPIO.HIGH)
                          GPIO.output(out4,GPIO.LOW)
                          time.sleep(0.03)
                          #time.sleep(1)
                      elif i==5:
                          GPIO.output(out1,GPIO.LOW)
                          GPIO.output(out2,GPIO.LOW)
                          GPIO.output(out3,GPIO.HIGH)
                          GPIO.output(out4,GPIO.HIGH)
                          time.sleep(0.03)
                          #time.sleep(1)
                      elif i==6:    
                          GPIO.output(out1,GPIO.LOW)
                          GPIO.output(out2,GPIO.LOW)
                          GPIO.output(out3,GPIO.LOW)
                          GPIO.output(out4,GPIO.HIGH)
                          time.sleep(0.03)
                          #time.sleep(1)
                      elif i==7:    
                          GPIO.output(out1,GPIO.HIGH)
                          GPIO.output(out2,GPIO.LOW)
                          GPIO.output(out3,GPIO.LOW)
                          GPIO.output(out4,GPIO.HIGH)
                          time.sleep(0.03)
                          #time.sleep(1)
                      if i==7:
                          i=0
                          continue
                      i=i+1
      
      
          elif x<0 and x>=-400:
              x=x*-1
              for y in range(x,0,-1):
                  if positive==1:
                      if i==0:
                          i=7
                      else:
                          i=i-1
                      y=y+3
                      positive=0
                  negative=1
                  #print((x+1)-y) 
                  if i==0:
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==1:
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==2:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==3:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==4:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==5:
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==6:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==7:    
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  if i==0:
                      i=7
                      continue
                  i=i-1 
    
              
    except KeyboardInterrupt:
        print("Saliendo del control del motor")
        
def motor(pasos_motor):
    setup()
    move(pasos_motor, out1,out2,out3,out4,i,positive,negative,y, buttonIn, alto)
        



