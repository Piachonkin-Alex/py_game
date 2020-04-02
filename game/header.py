import pygame
import random


class Barrier:
    def __init__(self, x, y, width, height, movement):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.movement = movement

    def move(self, our_display, display_width):
        if self.x >= -self.width:
            pygame.draw.rect(our_display, (85, 107, 47), (self.x, self.y, self.width, self.height))
            self.x -= self.movement
            return True
        else:
            self.x = display_width + 120 + random.randrange(-100, 70)
            return False
