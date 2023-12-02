import camera
import base64
from machine import Pin, PWM
from time import sleep

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

def TakePicture():
    try:
        camera.init(0, format=camera.JPEG)
        camera.framesize(camera.FRAME_96X96)
        camera.quality(63)
        floodlight.value(1)
        buf = camera.capture()
        PlayShutterSound()
        floodlight.value(0)
        encoded_image = base64.b64encode(buf)
        print(encoded_image.decode('utf-8')[:100])
        print(len(buf))
    except Exception as e:
        builtinled.value(0)
        sleep(3)
        print("reached exception")
        print("Exception:", str(e))
    finally:
        camera.deinit()
        takepic = False #reset

# Attach interrupt
shutterbutton.irq(trigger=Pin.IRQ_FALLING, handler=CheckPressed)

# If "Device is busy", replug and hit STOP immediately.
# This sleep is to prevent the program become "unstoppable"
sleep(3)

# Initialize Buzzer later to prevent unwanted noise.
buzzer = PWM(Pin(12))
buzzer.duty(0)
buzzer.freq(1000)

# If hear three beep then good to go.
for _ in range(3):
    beep()

print("loop we go!") #dev purposes

while True:
    if takepic:
        try:
            camera.init(0, format=camera.JPEG)
            camera.framesize(camera.FRAME_96X96)
            camera.quality(63)
            floodlight.value(1)
            buf = camera.capture()
            PlayShutterSound()
            floodlight.value(0)
            encoded_image = base64.b64encode(buf)
            print(encoded_image.decode('utf-8')[:100])
            print(len(buf))
        except Exception as e:
            for _ in range(3): #beep three times each 1 second if reach exception
                beep(1)
            print("reached exception")
            print("Exception:", str(e))
        finally:
            camera.deinit()
            takepic = False #reset

