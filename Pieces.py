# Pieces.py

from OpenGL.GL import *
import numpy as np
import math
import random

from Cube import Cube, Init

colors = (
        [1,0,0], # Red 0
        [0,1,0], # Green 1
        [0,0,1], # Blue 2
        [1,1,0], # Yellow 3
        [0,1,1], # Cyan 4
        [1,0.5,0], # Orange 5
        [1,0,1]) # Purple 6

axis = (
    [3,1,1], 
    [0,1,1], 
    [6,1,1], 
    [3,1,4], 
    [0,1,4], 
    [6,1,4], 
    [3,5,4]
)

pieceNames = ["I", "J", "L", "O", "S", "T", "Z"]  # List of pieces by name
cubeCount = 4 # Amount of cubes per piece

# A function to create Tetris pieces
def createTetrisPieces():

    tetrisPieces = []

    def J():
        for i in range(cubeCount):
            if i >= 3:
                piece = Piece(position=((i - 2) * -2, 0, 0), color=colors[0], axis=axis[0]) 
            else:
                piece = Piece(position=(0, i * -2, 0), color=colors[0], axis=axis[0])  
            tetrisPieces.append(piece)

    def L():
        for i in range(cubeCount):
            i -= 2
            if i >= 1:
                piece = Piece(position=((i - 2) * 2, 0, 0), color=colors[1], axis=axis[1]) 
            else:
                piece = Piece(position=(0, i * -2, 0), color=colors[1], axis=axis[1])  
            tetrisPieces.append(piece)

    def T():
        for i in range(cubeCount):
            i += 2
            if i >= 5:
                piece = Piece(position=((i - 2) * 2, (i - 4) * -2, 0), color=colors[2], axis=axis[2])
            else:
                piece = Piece(position=(i * 2, 0, 0), color=colors[2], axis=axis[2]) 
            tetrisPieces.append(piece)

    def O():
        piece0 = Piece(position=(2, 2, 2), color=colors[3], axis=axis[3])  
        tetrisPieces.append(piece0)
        piece1 = Piece(position=(4, 4, 2), color=colors[3], axis=axis[3])  
        tetrisPieces.append(piece1)
        piece2 = Piece(position=(2, 4, 2), color=colors[3], axis=axis[3])  
        tetrisPieces.append(piece2)
        piece3 = Piece(position=(4, 2, 2), color=colors[3], axis=axis[3])  
        tetrisPieces.append(piece3)

    def I():
        for i in range(cubeCount):
            piece = Piece(position=(i * -2, -2, 0), color=colors[4], axis=axis[4])  
            tetrisPieces.append(piece)

    def Z():
        counter = 0
        y = 0
        # Create instances of pieces and store them in a list
        for i in range(cubeCount):
            i = i + 4
            if i >= 6:
                i -= 1
            piece = Piece(position=(i * 2, y, 0), color=colors[5], axis=axis[5])  
            tetrisPieces.append(piece)
            counter += 1
            if counter >= 2:
                y += 2
                counter = 0

    def S():
        counter = 0
        y = 0
        # Create instances of pieces and store them in a list
        for i in range(cubeCount):
            i = i + 4
            if i >= 6:
                i -= 1
            piece = Piece(position=(i * -2, y, 0), color=colors[6], axis=axis[6]) 
            tetrisPieces.append(piece)
            counter += 1
            if counter >= 2:
                y += 2
                counter = 0

    for name in pieceNames:
        if name == "I":
            I()
        elif name == "J":
            J()
        elif name == "L":
            L()
        elif name == "O":
            O()
        elif name == "S":
            S()
        elif name == "T":
            T()
        elif name == "Z":
            Z()

    return tetrisPieces

class Piece:
    def __init__(self, position, color, axis):
        Init()
        self.cubes = [Cube(color, axis) for _ in range(cubeCount)]
        self.position = position  #takes position of each piece and cubes
        self.ang = 0
        self.axis = axis  #takes a different axis for each piece so they rotate differently
        self.color = np.asfarray(color)  #takes a different color for each piece
        self.vel = random.randrange(1, 3)

    def Update(self, deltaTime):
        self.ang += 50.0 * deltaTime

    def Render(self):
        m = glGetDouble(GL_MODELVIEW_MATRIX)
        glRotatef(self.ang, *self.axis)
        glTranslatef(*self.position)
        for cube in self.cubes:
            cube.Render()
        
        glLoadMatrixf(m)