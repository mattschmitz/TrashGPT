from machine import Pin

redLed = Pin(3, Pin.OUT)
greenLed = Pin(0, Pin.OUT)
blueLed = Pin(1, Pin.OUT)

def GetState(s):
    if s == "on":
        return 0
    elif s == "off":
        return 1

def ControlLed(color, state):
    if color == "red":
        redLed.value(GetState(state))
    elif color == "green":
        greenLed.value(GetState(state))
    elif color == "blue":
        blueLed.value(GetState(state))
    
