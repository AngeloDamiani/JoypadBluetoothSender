import pygame, sys, time


pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

joy = joysticks[0]
joy.init()

pygame.init()

NUMBYTES = 64
STARTPADDING = (2 ** (NUMBYTES + 8 - 1))


def axis2fixedPoint(value):
    if abs(value) > 0.15:
        BITS = 8
        return int((value+1)*(2**(BITS)-1)/2)
    else:
        return 127

while True:
    inttobites = STARTPADDING

    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN and event.button >= 8:
            pygame.quit()
            sys.exit()
    
    axis = 0
    axis = axis + axis2fixedPoint(joy.get_axis(0))*(2**24)
    axis = axis + axis2fixedPoint(joy.get_axis(1))*(2**16)
    axis = axis + axis2fixedPoint(joy.get_axis(2))*(2**40)
    axis = axis + axis2fixedPoint(joy.get_axis(3))*(2**0)
    axis = axis + axis2fixedPoint(joy.get_axis(4))*(2**8)
    axis = axis + axis2fixedPoint(joy.get_axis(5))*(2**32)

    buttons = 0
    for i in range (8):
        if joy.get_button(i):
            buttons = buttons + 2 ** (NUMBYTES - i - 1)

    hat = 0

    h = joy.get_hat(0)
    if h == (1, 0):
        hat = 2 ** (NUMBYTES - 9)
    elif h == (1, 1):
        hat = 2 ** (NUMBYTES - 10)
    elif h == (0, 1):
        hat = 2 ** (NUMBYTES - 11)
    elif h == (-1, 1):
        hat = 2 ** (NUMBYTES - 12)
    elif h == (-1, 0):
        hat = 2 ** (NUMBYTES - 13)
    elif h == (-1, -1):
        hat = 2 ** (NUMBYTES - 14)
    elif h == (0, -1):
        hat = 2 ** (NUMBYTES - 15)
    elif h == (1, -1):
        hat = 2 ** (NUMBYTES - 16)


    inttobites = inttobites + axis + buttons + hat

    print(bin(int(inttobites)))

    pygame.time.Clock().tick(30)
