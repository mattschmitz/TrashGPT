from machine import Pin

redLed = Pin(2, Pin.OUT)
greenLed = Pin(15, Pin.OUT)
blueLed = Pin(14, Pin.OUT)

def GetState(s):
    if s == "on":
        return 0
    elif s == "off":
        return 1

def ControlLed(color, state):
    if color == "red":
        print("ControlLed: red")
        redLed.value(GetState(state))
    elif color == "green":
        print("ControlLed: green")
        greenLed.value(GetState(state))
    elif color == "blue":
        print("ControlLed: blue")
        blueLed.value(GetState(state))
        
def AllOff():
    print("AllOff() called")
    redLed.value(1)
    greenLed.value(1)
    blueLed.value(1)
