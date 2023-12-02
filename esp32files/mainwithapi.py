import camera
import base64
from machine import Pin, PWM
from time import sleep
import api
import network
import requests

floodlight = Pin(4, Pin.OUT)
shutterbutton = Pin(13, Pin.IN, Pin.PULL_UP)
builtinled = Pin(33, Pin.OUT)

takepic = False

def beep(duration=0.1):
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
    try:
        camera.init(0, format=camera.JPEG)
        camera.framesize(camera.FRAME_96X96)
        camera.quality(63)
    except Exception as e:
        for _ in range(3):
            beep(1)
        print("reached exception")
        print("Exception:", str(e))

def DeinitCamera():
    camera.deinit()

def GetDecodedImage():
    print("Taking Photo")
    try:
        floodlight.value(1)
        buf = camera.capture()
        PlayShutterSound()
        floodlight.value(0)
        encoded_image = base64.b64encode(buf)
        decoded_image = encoded_image.decode('utf-8')
        print(decoded_image)
        print(len(buf))
    except Exception as e:
        for _ in range(3):
            beep(1)
        print("reached exception")
        print("Exception:", str(e))
    return decoded_image

def ConnectWifi():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('The Golden Apple', 'brendanlovesfood')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

# Attach interrupt
shutterbutton.irq(trigger=Pin.IRQ_FALLING, handler=CheckPressed)

# If "Device is busy", replug and hit STOP immediately.
# This sleep is to prevent the program become "unstoppable"
sleep(3)

# Initialize Buzzer later to prevent unwanted noise.
buzzer = PWM(Pin(12))
buzzer.duty(0)
buzzer.freq(1000)

# Initialize Cam
InitializeCamera()

# If hear three beep then good to go.
for _ in range(3):
    beep()

ConnectWifi()
decodedImage = GetDecodedImage()
DeinitCamera()

response = api.CallApi(decodedImage)
print(response)
takepic = False #reset

# print("loop we go!") #dev purposes
# 
# while True:
#     if takepic:
#         encodedImage = TakePicture()
#         response = api.CallApi(encodedImage)
#         print(response)
#         takepic = False #reset
