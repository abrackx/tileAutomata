import pygame
import sys
import random
from pygame.locals import *

running = True

class Tilemap:
    tilemap = []
    ht = None # ht = highlight texture

    def __init__(self, height, width, tilesize, textures):
        self.height = height # How many tiles high it is
        self.width = width # How many tiles wide it is
        self.tilesize = tilesize # How many pixels each tile is
        self.textures = textures # The textures
        self.size = (self.width*self.tilesize,self.height*self.tilesize)

    def generate_random(self):
        # Generate a random tilemap
        self.tilemap = [[random.randint(0, len(self.textures)-1) for e in range(self.width)] for e in range(self.height)]

    def draw(self, display, mouse=None):
        mouse = mouse
        # Draw the map
        for row in range(self.height):
            for column in range(self.width):
                texture = self.textures[self.tilemap[row][column]]
                if self.ht != None:
                    if mouse[0] >= (column*self.tilesize) and mouse[0] <= (column*self.tilesize)+self.tilesize:
                        if mouse[1] >= (row*self.tilesize) and mouse[1] <= (row*self.tilesize)+self.tilesize:
                            texture = self.ht
                display.blit(texture,(column*self.tilesize, row*self.tilesize))

    def drawOnOFf(self, display, mouse = None):
        mouse = mouse
        for row in range(self.height):
            for column in range(self.width):
                texture = self.tilemap[row][column]
                if mouse[0] >= (column * self.tilesize) and mouse[0] <= (column * self.tilesize) + self.tilesize:
                    if mouse[1] >= (row * self.tilesize) and mouse[1] <= (row * self.tilesize) + self.tilesize:
                        if texture == 1:
                            #display.blit(self.textures[0], (column*self.tilesize, row*self.tilesize))
                            self.tilemap[row][column] = 0
                        if texture == 0:
                            #display.blit(self.textures[1], (column*self.tilesize, row*self.tilesize))
                            self.tilemap[row][column] = 1
                display.blit(self.textures[self.tilemap[row][column]], (column*self.tilesize, row*self.tilesize))

    def automata(self, display):
        self.height = 10

        for i in range(self.height):
            self.tilemap.append([0,0,0,0,0,0,0,0,0,0])


        for row in range(self.height):
            row = row + 1
            for column in range(self.width):

                texture0 = self.tilemap[row-1][column]
                if (column - 1) < 0: #if compare first element to last in row
                    texture1 = self.tilemap[row-1][self.width-1]
                else:
                    texture1 = self.tilemap[row-1][column-1]

                if (column + 1) > self.width-1: #compare last element to first in row
                    texture2 = self.tilemap[row-1][0]
                else:
                    texture2 = self.tilemap[row-1][column+1]

                #automata bb
                if (texture0 == 1 and texture1 == 1):
                    self.tilemap[row][column] = 1
                elif (texture0 == 1 and texture2 == 1):
                    self.tilemap[row][column] = 0
                elif (texture1 == 1 and texture2 == 1):
                    self.tilemap[row][column] = 1
                elif (texture0 == 1 and texture1 == 1 and texture2 == 1):
                    self.tilemap[row][column] = 0
                else:
                    self.tilemap[row][column] = 0
                display.blit(self.textures[self.tilemap[row][column]], (column * self.tilesize, row * self.tilesize))


tilemap = Tilemap(1,10,100,
                  # Load the textures
                  {0: pygame.image.load("tile1.png"),
                   1: pygame.image.load("tile2.png")
                   }
                  )



tilemap.generate_random() # Generate a random tilemap

pygame.init()
DISPLAYSURF = pygame.display.set_mode((tilemap.size))
# Load the highlighter
tilemap.ht = pygame.image.load("highlight.png").convert(8)
tilemap.ht.set_alpha(10)


mouseClick = False

while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            mouseClick = True
        if event.type == MOUSEBUTTONDOWN:
            tilemap.drawOnOFf(DISPLAYSURF, clickPos)
            mouseClick = False
        if pygame.mouse.get_focused() == 0: #if the mouse if off screen, then do not show the highlighted tile
            tilemap.draw(DISPLAYSURF, (0,0))
        if keys[K_SPACE]:
            tilemap2 = Tilemap(10, 10, 100,
                              # Load the textures
                              {0: pygame.image.load("tile1.png"),
                               1: pygame.image.load("tile2.png")
                               }
                              )




            DISPLAYSURF = pygame.display.set_mode((tilemap2.size))



            tilemap.automata(DISPLAYSURF)

        # Draw the tilemap
        tilemap.draw(DISPLAYSURF, pygame.mouse.get_pos())

    pygame.display.update()
