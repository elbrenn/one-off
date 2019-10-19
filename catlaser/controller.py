import init_laser as laser
from evdev import InputDevice, categorize, ecodes

XPins = [12, 25, 24, 23]
YPins = [4, 17, 27, 22]

Laser_Pin = 16
testlaser = laser.Laser(XPins, YPins, Laser_Pin, 0.01)


testlaser.Laser_On()
testlaser.Laser_Off()

gamepad = InputDevice('/dev/input/event0')
print(gamepad)


up = False
down = False
left = False
right = False
to_break = False
speed = 1
while True:
    if to_break:
        testlaser.TurnOff()
        break
    x = 0
    y = 0
    if up:
        y = 10
    elif down:
        y = -10
    if left:
        x = -10
    elif right:
        x = 10
    x *= speed
    y *= speed
    if (x != 0) or (y != 0):
        testlaser._MoveRelSteps(x, y)

    try:
        events = gamepad.read()
        for event in events:
            if event.type == ecodes.EV_KEY:
                if event.code == 296: # SELECT
                    if event.value == 1:
                        if testlaser.Is_Laser_On:
                            testlaser.Laser_Off()
                        else:
                            testlaser.Laser_On()
                elif event.code == 297: #START
                    if event.value == 1:
                        to_break = True
                elif event.code == 291: # Y button
                    print("Y")
                elif event.code == 288: # X button
                    print("X")
                elif event.code == 290: # B button
                    if event.value == 1:
                        if testlaser.Is_Laser_On:
                            testlaser.Laser_Off()
                        else:
                            testlaser.Laser_On()                    
                elif event.code == 289: # A button
                    print("A")
                elif event.code == 293: # Right Trigger
                    print("R Trig")
                elif event.code == 292: # Left trigger
                    if event.value == 1:
                        speed = 5
                    elif event.value == 0:
                        speed = 1
                else:
                    print("unknown button")
            elif event.type == ecodes.EV_ABS:
                if event.code == 0: # X direction
                    if event.value == 0: #Left down
                        left = True
                        right = False
                    if event.value == 127:
                        left = False
                        right = False
                    elif event.value == 255: #Right down
                        right = True
                        left = False
                elif event.code == 1: #Y direction
                    if event.value == 0: #up direction
                        down = True
                        up = False
                    elif event.value == 127:
                        up = False
                        down = False
                    elif event.value == 255: #down direction
                        down = False
                        up = True
                else:
                    print("Unknown direction")
    except BlockingIOError:
        #do nothing
        pass