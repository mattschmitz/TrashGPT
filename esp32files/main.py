import camera
import base64
from machine import Pin, PWM
from time import sleep
import api
import network
import requests
import gc

floodlight = Pin(4, Pin.OUT)
shutterbutton = Pin(13, Pin.IN, Pin.PULL_UP)
builtinled = Pin(33, Pin.OUT)

takepic = False

def beep(times, duration=0.1):
    for _ in range(times):
        print("beep")
        buzzer.duty(512)  # Activate the buzzer at half power
        sleep(duration)   # Keep the buzzer on for the specified duration
        buzzer.duty(0)    # Turn off the buzzer
        sleep(0.1)        # Short pause between beeps

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
        beep(3,1)
        print("Reached Exception InitializeCamera()")
        print("Exception:", str(e))

def DeinitCamera():
    print("Deinitializing Camera")
    try:
        camera.deinit()
        print("Deinitializing Camera SUCCESS")
    except Exception as e:
        beep(3,1)
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
        beep(3,1)
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
        print("CTR got RECYCLABLE")
        beep(1,0.5)
    elif tr == "landfill" or tr == "Landfill":
        print("CTR got LANDFILL")
        beep(2,0.5)
    elif tr == "compostable" or tr == "Compostable":
        print("CTR got COMPOSTABLE")
        beep(3,0.5)
    else:
        print("CTR got ELSE")
        beep(3,1)

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
# encodedImage = GetEncodedImage(image)
# decodedImage = GetDecodedImage(encodedImage)
# response = api.CallApi(decodedImage)
# trimmedResponse = api.TrimResponse(response)
# print(trimmedResponse)
# CheckTrimmedResponse(trimmedResponse)
# gc.collect()


while True:
    if takepic:
        InitializeCamera()
        image = TakePicture()
        DeinitCamera()
        
        encodedImage = GetEncodedImage(image)
        decodedImage = GetDecodedImage(encodedImage)
        
        response = api.CallApi(decodedImage)
        trimmedResponse = api.TrimResponse(response)
        print(trimmedResponse)
        CheckTrimmedResponse(trimmedResponse)
        
        gc.collect()

        takepic = False #reset

