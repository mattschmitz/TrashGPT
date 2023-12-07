import camera
import ubinascii
import ledcontroller as led
from machine import Pin, PWM
from time import sleep
import api
import network
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
        sleep(0.10)
        led.ControlLed("red","off")
        sleep(0.10)
        
def LoopErrorIndicator():
    for _ in range(5):
        led.ControlLed("blue","on")
        sleep(0.10)
        led.ControlLed("blue","off")
        sleep(0.10)
        
def InitCamErrorIndicator():
    for _ in range(5):
        led.ControlLed("yellow","on")
        sleep(0.10)
        led.ControlLed("yellow","off")

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
  
def InitializeCamera():
    print("Initializing Camera")
    try:
        camera.init(0, format=camera.JPEG)
        camera.framesize(camera.FRAME_240X240)
        camera.quality(10)
        print("Initializing Camera SUCCESS")
    except Exception as e:
        InitCamErrorIndicator()
        print("Reached Exception InitializeCamera()")
        print("Exception:", str(e))

def DeinitCamera():
    print("Deinitializing Camera")
    try:
        camera.deinit()
        print("Deinitializing Camera SUCCESS")
    except Exception as e:
        print("Reached Exception DeinitCamera()")
        print("Exception:", str(e))
    
def GetEncodedImage(image):
    print("Encoding Image")
    encodedImage = ubinascii.b2a_base64(image)
    print("Encoding Image DONE")
    return encodedImage

def GetDecodedImage(encoded_image):
    print("Decoding Image")
    decodedImage = encoded_image.decode('utf-8')
    print("Decoding Image DONE")
    return decodedImage

def TakePicture():
    print("Taking Photo")
    try:
        floodlight.value(1)
        buf = camera.capture()
        floodlight.value(0)
        
        if type(buf) == bool:
            return
        
        PlayShutterSound()
        print("Type of captured data:", type(buf))  # Check the type of buf
        print("Done")
    except Exception as e:
        ErrorBeep()
        print("Reached Exception TakePicture()")
        print("Exception:", str(e))
    return buf

def ConnectWifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to WiFi...')
        sta_if.active(True)
        sta_if.connect('The Golden Apple', 'brendanlovesfood')
        while not sta_if.isconnected():
            pass
    print("Connected to WiFi.")    
    print('network config:', sta_if.ifconfig())
    
def DisconnectWifi():
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        print("Disconnecting from WiFi...")
        sta_if.disconnect()
        sta_if.active(False)  # Optionally deactivate the interface
        print("Disconnected from WiFi.")
    else:
        print("WiFi is not connected.")
    
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
        ServerErrorIndicator()

# Attach interrupt
shutterbutton.irq(trigger=Pin.IRQ_FALLING, handler=CheckPressed)

# If "Device is busy", replug and hit STOP immediately.
# This sleep is to prevent the program become "unstoppable"
sleep(1)
    
# Initialize Buzzer later to prevent unwanted noise.
buzzer = PWM(Pin(12))
buzzer.duty(0)
buzzer.freq(1000)

# If hear three beep then good to go.
beep(3)

led.AllOff()

# while True:
#     user_input = input("Enter 1 to take a picture, or press Enter to do nothing: ")
#     try:
#         if user_input == "1":
#             gc.collect()
#             
#             InitializeCamera()
#             image = TakePicture()
#             DeinitCamera()
#             
#             decodedImage = GetDecodedImage(GetEncodedImage(image))
# 
#             try:
#                 ConnectWifi()
#                 
#                 response = api.CallApi(decodedImage)
#                 trimmedResponse = api.TrimResponse(response)
#                 print(trimmedResponse)
#                 CheckTrimmedResponse(trimmedResponse)
#                 
#                 DisconnectWifi()
#             except Exception as e:
#                 ServerErrorIndicator()
#                 print(str(e))
# 
#             led.AllOff()
#             gc.collect()
#         else:
#             print("No action taken. Waiting for next command.")
#         
#     except Exception as e:
#         LoopErrorIndicator()
#         print("Exception in Loop")
#         print(str(e))
#         gc.collect()
#         takepic = False #reset
#         continue
        
while True:
    try: 
        if takepic:
            
            InitializeCamera()
            image = TakePicture()
            DeinitCamera()
            
            decodedImage = GetDecodedImage(GetEncodedImage(image))

            try:
                ConnectWifi()
                
                response = api.CallApi(decodedImage)
                trimmedResponse = api.TrimResponse(response)
                print(trimmedResponse)
                CheckTrimmedResponse(trimmedResponse)
                
                DisconnectWifi()
                
            except Exception as e:
                ServerErrorIndicator()
                takepic = False
                print(str(e))

            led.AllOff()
            gc.collect()

            takepic = False #reset
            
    except Exception as e:
        LoopErrorIndicator()
        print("Exception in Loop")
        print(str(e))
        gc.collect()
        takepic = False #reset
        continue

