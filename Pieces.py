# Pieces.py

from OpenGL.GL import *
import numpy as np
import math
import random
from Cube import *
from Texture import Texture

#[r,g,b,a]
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

borders = (
    (-5, 5),
    (-12, 30),
    (-6, 4)
)

pieceNames = ["I", "J", "L", "O", "S", "T", "Z"]  # List of pieces by name
cubeCount = 4 # Amount of cubes per piece

tetrisPieces = []

CubeList = []

# A function to create Tetris pieces
def createTetrisPieces():

    for i in range(len(pieceNames)):
        piece = Piece(position=(i*3, 18, i*-2), color=colors[i], name=pieceNames[i], filepath=filepaths[i]) 
        tetrisPieces.append(piece)

    return tetrisPieces

def checkCubeCol(piece):
    # Collect position of all cubes in the piece
    for cube in piece.cubes:
        locPos = np.round(cube.GetCubePos()) + np.round(piece.GetPos())

        if any(np.array_equal(locPos, pos.GetCubePos()) for pos in CubeList):
            print("overlaps")
            return False # overlaps

    return True # no overlaps

def freezeCubes(cube):
    CubeList.append(cube)

class Piece:
    def __init__(self, position, color, name, filepath):
        #Init()

        self.name = name
        if self.name == "I":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (0, 2, 0), (0, 4, 0)]
        elif self.name == "J":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (0, 2, 0), (-2, 2, 0)]
        elif self.name == "L":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (-2, -2, 0), (0, 2, 0)]
        elif self.name == "O":
            self.localPositions = [(0, 0, 0), (-2, -2, 0), (0, -2, 0), (-2, 0, 0)]
        elif self.name == "S":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (-2, -2, 0), (2, 0, 0)]
        elif self.name == "T":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (-2, 0, 0), (2, 0, 0)]
        elif self.name == "Z":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (2, -2, 0), (-2, 0, 0)]


        self.filepath = filepath


        self.cubes = [Cube(localPos, color, self.filepath) for localPos in self.localPositions]
        self.position = position        #takes position of each piece
        self.lastPosition = self.position #sets last position
        self.ang = 0
        self.axis = (3,1,1)             
        self.color = np.asfarray(color)  #takes a different color for each piece

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

    # Reset Cube Orientation for in gameplay
    def ResetCubePos(self):
        for i, cube in enumerate(self.cubes):
            #reset each localPos
            cube.SetCubePos(self.localPositions[i])

    # Revert Cube Positions for rotation function
    def RevertCubePos(self, lastPos):
        for i, cube in enumerate(self.cubes):
            #revert each localPos
            cube.SetCubePos(lastPos[i])

    #Change the value of appearing and disappearing for all cubes within piece (pass in a boolean for appear and disappear)
    def ToggleCubes(self, appear, disappear):
        for cube in self.cubes:
            cube.appearing = appear
            cube.disappearing = disappear
  
    # Rotation function for piece
    def Rotate(self, angle, axis):
        curLocalPositions = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        for i, cube in enumerate(self.cubes):
            curPos = cube.GetCubePos()
            curLocalPositions[i] = curPos

        # Convert angle to radians
        angle = math.radians(angle)
        center = np.asfarray(self.cubes[0].localPos)
        rotation_matrix = axis_rotation_matrix(angle, axis)

        # checks if cubes are in bounds before completing rotation
        for cube in self.cubes:
            cube.localPos = np.rint(np.dot(cube.localPos - center, rotation_matrix)) + center
            if not cube.CheckInBounds(piece=self):
                self.RevertCubePos(curLocalPositions)
                break

    # Check if all cubes of a piece are in bounds
    def CheckInBounds(self):
        for cube in self.cubes:
            for i in range(3): # for each axis (x,y,z)
                pos = np.round(cube.GetCubePos()) + np.round(self.position)
                # checks if each axis value is between border limits for that axis
                if pos[i] <= borders[i][0] or pos[i] >= borders[i][1]:
                    return False  # Cube is out of bounds for at least one dimension

        return True  # All cubes are within bounds for all dimensions

    #NOTE: Fading in/out can no longer be paused (because this update is no longer locked behind pause status)
    def Update(self, deltaTime, move, paused): #NEW: Takes pause status to gatekeep all update actions except fade
        #NEW
        #If the game is paused, don't update position
        if not paused:
        #NEW
            self.ang += 50.0 * deltaTime
            self.position += move

            if not self.CheckInBounds():
                self.position[0] = self.lastPosition[0]
                self.position[2] = self.lastPosition[2]
                
            # Save last position
            self.lastPosition = np.copy(self.position)

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

# quaternians rotation matrix 
def axis_rotation_matrix(angle, axis):
    axis = np.asarray(axis)
    axis = axis / np.sqrt(np.dot(axis, axis))
    q = np.array([np.cos(angle / 2.0), *(-axis * np.sin(angle / 2.0))])
    rotation_matrix = np.array([
        [1 - 2 * (q[2]**2 + q[3]**2), 2 * (q[1] * q[2] - q[0] * q[3]), 2 * (q[1] * q[3] + q[0] * q[2])],
        [2 * (q[1] * q[2] + q[0] * q[3]), 1 - 2 * (q[1]**2 + q[3]**2), 2 * (q[2] * q[3] - q[0] * q[1])],
        [2 * (q[1] * q[3] - q[0] * q[2]), 2 * (q[2] * q[3] + q[0] * q[1]), 1 - 2 * (q[1]**2 + q[2]**2)],
    ])
    return rotation_matrix