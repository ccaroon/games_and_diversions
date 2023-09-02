import pygame

from color import Color

class Mandlebrot:

    def __init__(self, xn, xx, yn, yx):
        self.xMin = xn
        self.xMax = xx
        self.yMin = yn
        self.yMax = yx

    def compute(self, iterations, screen):
        # these are used for calculating the points corresponding to the pixels
        xStep = (self.xMax - self.xMin) / (screen.get_width() * 1.0)
        yStep = (self.yMax - self.yMin) / (screen.get_height() * 1.0)

        x = self.xMin * 1.0
        y = self.yMin * 1.0

        for i in range(0, screen.get_height()):
            for j in range(0, screen.get_width()):
                z = 0.0
                zi = 0.0
                inSet = True
                for k in range(0, iterations):
                    # z^2 = (a+bi)(a+bi) = a^2 + 2abi - b^2
                    newZ = (z*z) - (zi*zi) + x
                    newZI = 2*z*zi + y
                    z = newZ
                    zi = newZI
                    if ((z*z) + (zi*zi)) > 4:
                        inSet = False
                        colour = k
                        k = iterations

                if inSet:
                    pygame.draw.line(screen, Color.BLACK, (j,i),(j,i))
                else:
                    pygame.draw.line(screen, Color.to_RGB(colour), (j,i),(j,i))

                x += xStep

            y += yStep
            x = self.xMin
