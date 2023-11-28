# Pieces.py

from OpenGL.GL import *
import numpy as np
import math
import random

from Cube import Cube, Init, axis_rotation_matrix
import GamePlay

from Texture import Texture

#CHANGED
#Added transparency (color[3])
colors = (
        [0,1,1,1], # Cyan 0
        [0,0,1,1], # Blue 1
        [1,0.5,0,1], # Orange 2
        [1,1,0,1], # Yellow 3
        [0,1,0,1], # Green 4
        [1,0,1,1], # Purple 5
        [1,0,0,1] # Red 6
)

filepaths = (
    "Textures/blueberryI.png",
    "Textures/blackberriesJ.png",
    "Textures/orangeL.png",
    "Textures/bananaO.png",
    "Textures/pearZ.png",
    "Textures/grapesT.png",
    "Textures/strawberryS.png"
)



pieceNames = ["I", "J", "L", "O", "S", "T", "Z"]  # List of pieces by name
cubeCount = 4 # Amount of cubes per piece

# A function to create Tetris pieces
def createTetrisPieces():

    tetrisPieces = []

    for i in range(len(pieceNames)):
        print(i)
        piece = Piece(position=(0, 18, -2), color=colors[i], name=pieceNames[i], filepath=filepaths[i]) 
        tetrisPieces.append(piece)

    return tetrisPieces

class Piece:
    def __init__(self, position, color, name, filepath):
        #Init()

        self.name = name
        if self.name == "I":
            localPositions = [(0, 0, 0), (0, 0, -2), (0, 0, -4), (0, 0, 2)]
        elif self.name == "J":
            localPositions = [(0, 0, 0), (0, 2, 0), (-2, 2, 0), (0, -2, 0)]
        elif self.name == "L":
            localPositions = [(0, 0, 0), (0, 2, 0), (-2, -2, 0), (0, -2, 0)]
        elif self.name == "O":
            localPositions = [(0, 0, 0), (-2, 0, 0), (0, -2, 0), (-2, -2, 0)]
        elif self.name == "S":
            localPositions = [(0, 0, 0), (0, -2, 0), (2, 0, 0), (-2, -2, 0)]
        elif self.name == "T":
            localPositions = [(0, 0, 0), (-2, 0, 0), (2, 0, 0), (0, -2, 0)]
        elif self.name == "Z":
            localPositions = [(0, 0, 0), (0, -2, 0), (-2, 0, 0), (2, -2, 0)]


        self.filepath = filepath
        print(filepath)

        self.cubes = [Cube(localPos, color, self.filepath) for localPos in localPositions]
        self.position = position        #takes position of each piece
        self.ang = 0
        self.axis = (3,1,1)             
        self.color = np.asfarray(color)  #takes a different color for each piece
        self.vel = random.randrange(1, 3)

        self.transforms = [np.eye(4) for _ in range(cubeCount)]

        #NEW
        #Tracks the time since fade animation started (might not need)
        self.animTime = 0
        #Tracks if the fade in animation is ongoing
        self.appearing = True
        #Tracks if the fade out animation is ongoing
        self.disappearing = False
        #TEST
        #Set cubes within piece to be fully transparent
        for cube in self.cubes:
            cube.color[3] = 0

    def GetPos(self):
        return self.position

    def SetPos(self, position):
        self.position = position
        #for i in range(len(self.cubes)):
        '''for cube in self.cubes:
            #change each localPos
            localPos = cube.GetCubePos()
            newPosition = np.add(position, localPos)
            cube.SetCubePos(newPosition)'''
        
    # Rotation function for piece
    def Rotate(self, angle, axis):
        rotation_matrix = axis_rotation_matrix(angle, axis)
        for cube in self.cubes:
            cube.localPos = np.dot(cube.localPos, rotation_matrix)

    def Update(self, deltaTime, move):
        self.ang += 50.0 * deltaTime
        self.position += move

        #NEW
        #If piece is appearing, call fade in function for all of its cubes
        if self.appearing == True:
            for cube in self.cubes:
                cube.FadeIn(deltaTime)
        #Otherwise, if piece is disappearing, call fade out function for all of its cubes
        elif self.disappearing == True:
            for cube in self.cubes:
                cube.FadeOut(deltaTime)



    def Render(self):
        #m = glGetDouble(GL_MODELVIEW_MATRIX)
        #center = self.cubes[0].localPos

        glPushMatrix()
        glTranslatef(*self.position)
        #glRotatef(self.ang, *center)
        for cube in self.cubes:
            cube.Render()
        glPopMatrix()
        
        #glLoadMatrixf(m)