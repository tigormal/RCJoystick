from socket import *
import struct
import uinput
import logging

logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)

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
    uinput.ABS_HAT0X  + (0, 255, 0, 0),
    uinput.ABS_HAT0Y  + (0, 255, 0, 0),
    uinput.ABS_HAT1X  + (0, 255, 0, 0),
    uinput.ABS_HAT1Y  + (0, 255, 0, 0),
    uinput.BTN_THUMBL,
    uinput.BTN_THUMBR,
    # uinput.ABS_X + (0, 255, 0, 0),
    # uinput.ABS_Y + (0, 255, 0, 0),
)

logging.info("Creating device")

device = uinput.Device(
    events,
    vendor=0x045e,
    product=0x028e,
    version=0x110,
    name="Microsoft X-Box 360 pad",
)

device.emit(uinput.ABS_HAT0X, 128, syn=False)
device.emit(uinput.ABS_HAT0Y, 128)
device.emit(uinput.ABS_HAT1X, 128, syn=False)
device.emit(uinput.ABS_HAT1Y, 128)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

try:
    while True:

        # Receive the client packet along with the address it is coming from
        message, address = serverSocket.recvfrom(1024)
        print("Got message", str(message))

        try:
            j0x, j0y, j1x, j1y, j0sw, j1sw, onoff = struct.unpack('<HHHH???', message)
            print(j0x, j0y, j1x, j1y, j0sw, j1sw, onoff)
        except:
            logging.warning("Could not read data from bytes: " + str(message))
        # j_raw = [j0x, j0y, j1x, j1y]
        # j_calib = [leftJoystickX, leftJoystickY, rightJoystickX, rightJoystickY]

        # for i, val in enumerate(j_raw):
        #     j_calib[i] = translate(val, JS_MIN_VAL, JS_MAX_VAL, 0, 255)
        leftJoystickX = int(translate(j0x, JS_MIN_VAL, JS_MAX_VAL, 0, 255))
        leftJoystickY = int(translate(j0y, JS_MIN_VAL, JS_MAX_VAL, 0, 255))
        rightJoystickX = int(translate(j1x, JS_MIN_VAL, JS_MAX_VAL, 0, 255))
        rightJoystickY = int(translate(j1y, JS_MIN_VAL, JS_MAX_VAL, 0, 255))
        

        print(leftJoystickX, leftJoystickY, rightJoystickX, rightJoystickY)

        # # Otherwise, the server responds
        # serverSocket.sendto(message, address) 

        if j0sw:
            device.emit(uinput.BTN_THUMBL, 1)
        else:
            device.emit(uinput.BTN_THUMBL, 0)

        if j1sw:
            device.emit(uinput.BTN_THUMBR, 1)
        else:
            device.emit(uinput.BTN_THUMBR, 0)

        # Emit axes
        device.emit(uinput.ABS_HAT0X, leftJoystickX, syn=False)
        device.emit(uinput.ABS_HAT0Y, leftJoystickY)
        device.emit(uinput.ABS_HAT1X, rightJoystickX, syn=False)
        device.emit(uinput.ABS_HAT1Y, rightJoystickY)
except KeyboardInterrupt:
    pass
finally:
    serverSocket.close()


