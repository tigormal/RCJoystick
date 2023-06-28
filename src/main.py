from socket import *
import struct
import uinput

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('', 1234))

JS_MIN_VAL = 0
JS_MID_VAL = 1650
JS_MAX_VAL = 3300

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
    uinput.ABS_X + (0, 255, 0, 0),
    uinput.ABS_Y + (0, 255, 0, 0),
)
device = uinput.Device(
    events,
    vendor=0x045e,
    product=0x028e,
    version=0x110,
    name="Microsoft X-Box 360 pad",
)

device.emit(uinput.ABS_X, 128, syn=False)
device.emit(uinput.ABS_Y, 128)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

while True:

    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)

    j0x, j0y, j1x, j1y, j0sw, j1sw, onoff = struct.unpack('>HHHH???', message)
    j_raw = [j0x, j0y, j1x, j1y]
    j_calib = [leftJoystickX, leftJoystickY, rightJoystickX, rightJoystickY]

    for i, val in enumerate(j_raw):
        j_calib[i] = translate(val, JS_MIN_VAL, JS_MAX_VAL, -1.0, 1.0)

    # # Otherwise, the server responds
    # serverSocket.sendto(message, address) 

    if j0sw:
        ...
    else:
        ...

    if j1sw:
        ...
    else:
        ...

    # Emit axes
    ...

