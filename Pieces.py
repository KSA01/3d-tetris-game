# Pieces.py

from OpenGL.GL import *
import numpy as np
import math
import random
import quaternion

from Cube import * #Cube, Init, axis_rotation_matrix
#import GamePlay

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
        #print(i)
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
        #print(filepath)

        self.cubes = [Cube(localPos, color, self.filepath) for localPos in localPositions]
        self.position = position        #takes position of each piece
        self.ang = 0
        self.axis = (3,1,1)             
        self.color = np.asfarray(color)  #takes a different color for each piece
        self.vel = random.randrange(1, 3)
        self.rotation_quat = (1, 0, 0, 0)  # Initialize rotation quaternion

        self.transforms = [np.eye(4) for _ in range(cubeCount)]


        #TEST
        #Set cubes within piece to be fully transparent on init
        for cube in self.cubes:
            cube.color[3] = 0

        #Toggle cubes to appear
        self.ToggleCubes(True, False)

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
        
    #NEW
    #Change the value of appearing and disappearing for all cubes within piece (pass in a boolean for appear and disappear)
    def ToggleCubes(self, appear, disappear):
        for cube in self.cubes:
            cube.appearing = appear
            cube.disappearing = disappear

        
    # Rotation function for piece
    def Rotate(self, angle, axis):
        # Convert angle to radians
        angle = math.radians(angle)
        center = np.asfarray(self.cubes[0].localPos)
        rotation_matrix = axis_rotation_matrix(angle, axis)

        for cube in self.cubes:
            cube.localPos = np.rint(np.dot(cube.localPos - center, rotation_matrix)) + center

    #NOTE: Fading in/out can no longer be paused (because this update is no longer locked behind pause status)
    def Update(self, deltaTime, move, paused): #NEW: Takes pause status to gatekeep all update actions except fade
        #NEW
        #If the game is paused, don't update position
        if not paused:
        #NEW
            self.ang += 50.0 * deltaTime
            self.position += move

        #TEST: Update Cubes within piece regardless of pause status
        for cube in self.cubes:
            cube.Update(deltaTime, move)




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