import pygame
import sys
import time
from src.model.ijoypadobserver import *


class JoypadReader:
    def __init__(self, observer):

        self.numbytes = 64
        self.startpadding = (2 ** (self.numbytes + 8 - 1))
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        self.joystick = joysticks[0]
        self.joystick.init()

        self.stop = True

        self.current_data = None
        self.observer = []
        self.observer.append(observer)


    def axis2fixedPoint(self, value):
        if abs(value) > 0.15:
            BITS = 8
            return int((value + 1) * (2 ** (BITS) - 1) / 2)
        else:
            return 127


    def start(self):
        joy = self.joystick

        pygame.init()

        NUMBYTES = self.numbytes

        STARTPADDING = self.startpadding
        self.stop = False

        pow2dict = {}
        for i in range (NUMBYTES):
            pow2dict.update({i,2**i})

        while not self.stop:
            pygame.event.pump()
            inttobites = STARTPADDING

            axis = 0
            axis = axis + self.axis2fixedPoint(joy.get_axis(0)) * pow2dict.get(24)
            axis = axis + self.axis2fixedPoint(joy.get_axis(1)) * pow2dict.get(16)
            axis = axis + self.axis2fixedPoint(joy.get_axis(2)) * pow2dict.get(40)
            axis = axis + self.axis2fixedPoint(joy.get_axis(3)) * pow2dict.get(0)
            axis = axis + self.axis2fixedPoint(joy.get_axis(4)) * pow2dict.get(8)
            axis = axis + self.axis2fixedPoint(joy.get_axis(5)) * pow2dict.get(32)
    
            buttons = 0
            for i in range(8):
                if joy.get_button(i):
                    buttons = buttons + pow2dict.get(NUMBYTES - i - 1)

            hat = 0

            h = joy.get_hat(0)
            if h == (1, 0):
                hat = pow2dict.get(NUMBYTES - 9)
            elif h == (1, 1):
                hat = pow2dict.get(NUMBYTES - 10)
            elif h == (0, 1):
                hat = pow2dict.get(NUMBYTES - 11)
            elif h == (-1, 1):
                hat = pow2dict.get(NUMBYTES - 12)
            elif h == (-1, 0):
                hat = pow2dict.get(NUMBYTES - 13)
            elif h == (-1, -1):
                hat = pow2dict.get(NUMBYTES - 14)
            elif h == (0, -1):
                hat = pow2dict.get(NUMBYTES - 15)
            elif h == (1, -1):
                hat = pow2dict.get(NUMBYTES - 16)

            inttobites = inttobites + axis + buttons + hat


            for ob in self.observer:
                ob.update(inttobites)

            print(bin(int(inttobites)))
            pygame.time.Clock().tick(100)

        pygame.quit()


    def stopRead(self):
        self.stop = True


