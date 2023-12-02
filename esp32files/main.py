import camera
import base64
from machine import Pin
from time import sleep

floodlight = Pin(4, Pin.OUT)
pushbutton = Pin(1, Pin.IN, Pin.PULL_UP)
builtinled = Pin(33, Pin.OUT)

takepic = False

def CheckPressed(pin):
  global takepic
  takepic = True
  global interrupt_pin
  interrupt_pin = pin
  
pushbutton.irq(trigger=Pin.IRQ_FALLING, handler=CheckPressed)

while True:
    if takepic:
        try:
            camera.init(0, format=camera.JPEG)
            camera.framesize(camera.FRAME_96X96)
            camera.quality(63)
            floodlight.value(1)
            buf = camera.capture()
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
            takepic = False
