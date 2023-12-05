import camera
import base64
import ledcontroller as led
from machine import Pin, PWM
from time import sleep
import api
import network
import requests
import gc

floodlight = Pin(4, Pin.OUT)
shutterbutton = Pin(13, Pin.IN, Pin.PULL_UP)

takepic = False

def beep(times, duration=0.1):
    for _ in range(times):
        print("beep")
        buzzer.duty(512)  # Activate the buzzer at half power
        sleep(duration)   # Keep the buzzer on for the specified duration
        buzzer.duty(0)    # Turn off the buzzer
        sleep(0.1)        # Short pause between beeps
    
def ErrorBeep():
    beep(3,1)
    
def ServerErrorIndicator():
    for _ in range(10):
        led.ControlLed("red","on")
        sleep(0.15)
        led.ControlLed("red","off")

def PlayShutterSound():
    buzzer.duty(512)  # Set volume (duty cycle)
    buzzer.freq(2000)  # Higher pitch
    sleep(0.10)       # Short beep
    buzzer.freq(1000)  # Lower pitch
    sleep(0.10)       # Short beep
    buzzer.duty(0)    # Turn off buzzer

def CheckPressed(pin):
  global takepic
  takepic = True
  global interrupt_pin
  interrupt_pin = pin
  
def InitializeCamera():
    print("Initializing Camera")
    try:
        camera.init(0, format=camera.JPEG)
        camera.framesize(camera.FRAME_96X96)
        camera.quality(63)
        print("Initializing Camera SUCCESS")
    except Exception as e:
        ErrorBeep()
        print("Reached Exception InitializeCamera()")
        print("Exception:", str(e))

def DeinitCamera():
    print("Deinitializing Camera")
    try:
        camera.deinit()
        print("Deinitializing Camera SUCCESS")
    except Exception as e:
        ErrorBeep()
        print("Reached Exception DeinitCamera()")
        print("Exception:", str(e))
    
def GetEncodedImage(image):
    encodedImage = base64.b64encode(image)
    return encodedImage

def GetDecodedImage(encoded_image):
    decodedImage = encoded_image.decode('utf-8')
    return decodedImage

def TakePicture():
    print("Taking Photo")
    try:
        floodlight.value(1)
        buf = camera.capture()
        PlayShutterSound()
        print("Type of captured data:", type(buf))  # Check the type of buf
        floodlight.value(0)
        print("Done")
    except Exception as e:
        ErrorBeep()
        print("Reached Exception TakePicture()")
        print("Exception:", str(e))
    return buf

def ConnectWifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('The Golden Apple', 'brendanlovesfood')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
def CheckTrimmedResponse(tr):
    if tr == "recyclable" or tr == "Recyclable":
        print("CTR: green")
        beep(1)
        led.ControlLed("green","on")
        sleep(3)
        led.ControlLed("green","off")
        
    elif tr == "landfill" or tr == "Landfill":
        print("CTR: red")
        beep(1)
        led.ControlLed("red","on")
        sleep(3)
        led.ControlLed("red","off")
        
    elif tr == "compostable" or tr == "Compostable":
        print("CTR: blue")
        beep(1)
        led.ControlLed("blue","on")
        sleep(3)
        led.ControlLed("blue","off")
        
    else:
        ErrorBeep()
        for _ in range(10):
            led.ControlLed("red","on")
            sleep(0.15)
            led.ControlLed("red","off")

# Attach interrupt
shutterbutton.irq(trigger=Pin.IRQ_FALLING, handler=CheckPressed)

# If "Device is busy", replug and hit STOP immediately.
# This sleep is to prevent the program become "unstoppable"
sleep(3)

# Connect to WiFi
ConnectWifi()
    
# Initialize Buzzer later to prevent unwanted noise.
buzzer = PWM(Pin(12))
buzzer.duty(0)
buzzer.freq(1000)

# If hear three beep then good to go.
beep(3)

# InitializeCamera()
# image = TakePicture()
# DeinitCamera()
# 
# encodedImage = GetEncodedImage(image)
# decodedImage = GetDecodedImage(encodedImage)
# 
# try:
#     response = api.CallApi(decodedImage)
#     trimmedResponse = api.TrimResponse(response)
#     print(trimmedResponse)
#     CheckTrimmedResponse(trimmedResponse)
# except Exception as e:
#     ServerErrorBeep()
#     print(str(e))
# 
# led.AllOff()
# gc.collect()

led.AllOff()

while True:
    if takepic:
        
        InitializeCamera()
        image = TakePicture()
        DeinitCamera()

        encodedImage = GetEncodedImage(image)
        decodedImage = GetDecodedImage(encodedImage)

        try:
            response = api.CallApi(decodedImage)
            trimmedResponse = api.TrimResponse(response)
            print(trimmedResponse)
            CheckTrimmedResponse(trimmedResponse)
        except Exception as e:
            ServerErrorIndicator()
            print(str(e))

        led.AllOff()
        gc.collect()

        takepic = False #reset

