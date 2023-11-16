# Pieces.py

from OpenGL.GL import *
import numpy as np
import math
import random

from Cube import Cube, Init

from Texture import Texture

colors = (
        [0,1,1], # Cyan 0
        [0,0,1], # Blue 1
        [1,0.5,0], # Orange 2
        [1,1,0], # Yellow 3
        [0,1,0], # Green 4
        [1,0,1], # Purple 5
        [1,0,0] # Red 6
)

filepaths = (
    "blueberryI.png",
    "blackberriesJ.png",
    "orangeL.png",
    "bananaO.png",
    "pearZ.png",
    "grapesT.png",
    "strawberryS.png"
)

#BUG: Only the texture for Z is being used, because it is the last on this list
#This could be a problem with texture coordinates, is the last image defining the coordinates to be on the pear image?
#So it would be a problem in Texture.py?
#Do I need to unbind the texture each time?
pieceNames = ["I", "J", "L", "O", "S", "T", "Z"]  # List of pieces by name
cubeCount = 4 # Amount of cubes per piece

# A function to create Tetris pieces
def createTetrisPieces():

    tetrisPieces = []

    for i in range(len(pieceNames)):
        print(i)
        piece = Piece(position=(0, 0, 0), color=colors[i], name=pieceNames[i], filepath=filepaths[i]) 
        tetrisPieces.append(piece)

    return tetrisPieces

class Piece:
    def __init__(self, position, color, name, filepath):
        #Init()

        self.name = name
        if self.name == "I":
            localPositions = [(-6, 6, 0), (-6, 6, -2), (-6, 6, -4), (-6, 6, 2)]
        elif self.name == "J":
            localPositions = [(0, 6, 0), (0, 8, 0), (-2, 8, 0), (0, 4, 0)]
        elif self.name == "L":
            localPositions = [(6, 6, 0), (6, 8, 0), (4, 8, 0), (6, 4, 0)]
        elif self.name == "O":
            localPositions = [(-6, -1, 0), (-8, -1, 0), (-6, -3, 0), (-8, -3, 0)]
        elif self.name == "S":
            localPositions = [(0, -1, 0), (-2, -1, 0), (-2, -3, 0), (-4, -3, 0)]
        elif self.name == "T":
            localPositions = [(6, -1, 0), (4, -1, 0), (8, -1, 0), (6, -3, 0)]
        elif self.name == "Z":
            localPositions = [(-4, -8, 0), (-2, -8, 0), (-2, -10, 0), (0, -10, 0)]


        self.filepath = filepath
        print(filepath)

        self.cubes = [Cube(color, localPos, filepath) for localPos in localPositions]
        self.position = position        #takes position of each piece
        self.ang = 0
        self.axis = (3,1,1)             
        self.color = np.asfarray(color)  #takes a different color for each piece
        self.vel = random.randrange(1, 3)

    def Update(self, deltaTime):
        self.ang += 50.0 * deltaTime

    def Render(self):
        #m = glGetDouble(GL_MODELVIEW_MATRIX)
        center = self.cubes[0].localPos

        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.ang, *center)

        for cube in self.cubes:
            cube.Render()
        
        glPopMatrix()
        
        #glLoadMatrixf(m)