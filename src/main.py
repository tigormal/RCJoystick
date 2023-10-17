#!/usr/bin/python
from socket import socket, AF_INET, SOCK_DGRAM
import struct
import uinput
import logging
import time

logging.basicConfig(level=logging.DEBUG)

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
logging.info("Starting server")
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('', 1234))

JS_MIN_VAL = 142
JS_MID_VAL = 1650
JS_MAX_VAL = 3165

leftJoystickX = 0
leftJoystickY = 0
rightJoystickX = 0
rightJoystickY = 0

events = (
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_TL,
    uinput.BTN_TR,
    uinput.BTN_THUMBL,
    uinput.BTN_THUMBR,
    uinput.ABS_X + (0, 1024, 0, 0),
    uinput.ABS_Y + (0, 1024, 0, 0),
)

logging.info("Creating device")

device = uinput.Device(
    events,
    vendor=0x045e,
    product=0x028e,
    version=0x110,
    # name="Microsoft X-Box 360 pad",
    name="Generic Remote Joystick",
)

logging.debug("Created device")

device.emit(uinput.ABS_X, 512, syn=False)
device.emit(uinput.ABS_Y, 512)
# device.emit(uinput.ABS_HAT1X, 128, syn=False)
# device.emit(uinput.ABS_HAT1Y, 128)

j0x, j0y, j1x, j1y, j0sw, j1sw, onoff, bt1, bt2, bt3, bt4 = tuple([None]*11)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

if __name__ == '__main__':
    try:
        logging.debug("Entering cycle")
        # time.sleep(5)
        while True:
            message, address = serverSocket.recvfrom(1024)
            # print("Got message", str(message))
    
            try:
                j0x, j0y, j1x, j1y, j0sw, j1sw, onoff, bt1, bt2, bt3, bt4 = struct.unpack('<HHHH???????', message)
                # print(j0x, j0y, j1x, j1y, j0sw, j1sw, onoff, bt1, bt2, bt3, bt4)
            except:
                logging.warning("Could not read data from bytes: " + str(message))
                continue
    
    
            leftJoystickX = int(translate(j0x, JS_MIN_VAL, JS_MAX_VAL, 0, 1024))
            leftJoystickY = int(translate(j0y, JS_MIN_VAL, JS_MAX_VAL, 0, 1024))
            rightJoystickX = int(translate(j1x, JS_MIN_VAL, JS_MAX_VAL, 0, 1024))
            rightJoystickY = int(translate(j1y, JS_MIN_VAL, JS_MAX_VAL, 0, 1024))
            # print(leftJoystickX, leftJoystickY, rightJoystickX, rightJoystickY)
    
    
            if j0sw is not None:
                device.emit(uinput.BTN_THUMBL, j0sw)
    
            if j1sw is not None:
                device.emit(uinput.BTN_THUMBR, j1sw)
    
            if onoff is not None:
                device.emit(uinput.BTN_TR, onoff)
    
            if bt1 is not None:
                device.emit(uinput.BTN_A, bt1)
    
            if bt2 is not None:
                device.emit(uinput.BTN_B, bt2)
    
            if bt3 is not None:
                device.emit(uinput.BTN_X, bt3)
    
            if bt4 is not None:
                device.emit(uinput.BTN_Y, bt4)
    
            # Emit axes
            device.emit(uinput.ABS_X, rightJoystickX, syn=False)
            device.emit(uinput.ABS_Y, leftJoystickY)
        logging.debug("Exiting cycle")
    
    except KeyboardInterrupt:
        pass
    finally:
        logging.debug("Closing socket")
        serverSocket.close()


