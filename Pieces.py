# Pieces.py

from OpenGL.GL import *
import numpy as np
import math
import random
#import quaternion

from Cube import * #Cube, Init, axis_rotation_matrix
#import GamePlay

from Texture import Texture
import Camera

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

        #Smooth rotations
        #Tracks which direction the piece is currently rotating (left, right, down)
        self.rotateDir = None
        #Tracks how many degrees have been rotated in current rotation
        self.radRotated = math.radians(0)

        #Relative rotations
        #The axis to rotate the pieces on (horizontal by default, changes when rotation is toggled)
        self.rotateAxis = (0, -2, 0)

        self.name = name
        if self.name == "I":
            self.localPositions = [(0, 0, 0), (0, 0, -2), (0, 0, -4), (0, 0, 2)]
        elif self.name == "J":
            self.localPositions = [(0, 0, 0), (0, 2, 0), (-2, 2, 0), (0, -2, 0)]
        elif self.name == "L":
            self.localPositions = [(0, 0, 0), (0, 2, 0), (-2, -2, 0), (0, -2, 0)]
        elif self.name == "O":
            self.localPositions = [(0, 0, 0), (-2, 0, 0), (0, -2, 0), (-2, -2, 0)]
        elif self.name == "S":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (2, 0, 0), (-2, -2, 0)]
        elif self.name == "T":
            self.localPositions = [(0, 0, 0), (-2, 0, 0), (2, 0, 0), (0, -2, 0)]
        elif self.name == "Z":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (-2, 0, 0), (2, -2, 0)]


        self.filepath = filepath


        self.cubes = [Cube(localPos, color, self.filepath) for localPos in self.localPositions]
        self.position = position        #takes position of each piece
        self.ang = 0
        self.axis = (3,1,1)             
        self.color = np.asfarray(color)  #takes a different color for each piece
        self.vel = random.randrange(1, 3)
        self.rotation_quat = (1, 0, 0, 0)  # Initialize rotation quaternion

        self.transforms = [np.eye(4) for _ in range(cubeCount)]


        #Set cubes within piece to be fully transparent on init
        for cube in self.cubes:
            cube.color[3] = 0

        #Toggle cubes to appear
        self.ToggleCubes(True, False)

    def GetPos(self):
        return self.position

    def SetPos(self, position):
        self.position = position

    def ResetCubePos(self):
        for i, cube in enumerate(self.cubes):
            #reset each localPos
            cube.SetCubePos(self.localPositions[i])

        
    #Change the value of appearing and disappearing for all cubes within piece (pass in a boolean for appear and disappear)
    def ToggleCubes(self, appear, disappear):
        for cube in self.cubes:
            cube.appearing = appear
            cube.disappearing = disappear


    #Smooth Rotations
    #Takes a direction (left, right, down) and toggles the piece to rotate that way over 1/6s
    def ToggleRotate(self, dir):
        #If the piece is not currently rotating, toggle it to rotate in the given direction
        if self.rotateDir == None:
            self.rotateDir = dir

            #Check axis facing the camera (for relative piece rotations)
            curSide = Camera.getCurSide()
            
            #If rotating left or right, rotate around y axis
            if self.rotateDir == "left":
                self.rotateAxis = (0, -2, 0)
            elif self.rotateDir == "right":
                self.rotateAxis = (0, 2, 0)
            #If rotating down, rotate around x or z axis
            elif self.rotateDir == "down":
                if curSide == 'z':
                    self.rotateAxis = (-2, 0, 0)
                elif curSide == '-z':
                    self.rotateAxis = (2, 0, 0)
                elif curSide == 'x':
                    self.rotateAxis = (0, 0, -2)
                elif curSide == '-x':
                    self.rotateAxis = (0, 0, 2)


    #Rotates a piece by a fraction of a 90 degree angle (for smooth rotations)
    def RotateSmooth(self, deltaTime):
        center = np.asfarray(self.cubes[0].localPos)

        #The magnitude of the angle of rotation (in radians)
        mag = math.radians(90 * 6 * deltaTime)

        if self.rotateDir == "left":
            #If the rotation is almost complete, rotate the rest of the way
            if (self.radRotated + mag) >= math.radians(90):
                mag = math.radians(90) - self.radRotated
                #Reset rotation counter and rotation status
                self.radRotated = math.radians(0)
                self.rotateDir = None
            else:
                self.radRotated += mag

            angle = mag
            
            axis = self.rotateAxis

        elif self.rotateDir == "right":
            #If the rotation is almost complete, rotate the rest of the way
            if (self.radRotated + mag) >= math.radians(90):
                mag = math.radians(90) - self.radRotated
                #Reset rotation counter and rotation status
                self.radRotated = math.radians(0)
                self.rotateDir = None
            else:
                self.radRotated += mag

            angle = mag

            axis = self.rotateAxis

        elif self.rotateDir == "down":
            #If the rotation is almost complete, rotate the rest of the way
            if (self.radRotated + mag) >= math.radians(90):
                mag = math.radians(90) - self.radRotated
                #Reset rotation counter and rotation status
                self.radRotated = math.radians(0)
                self.rotateDir = None
            else:
                self.radRotated += mag

            angle = -mag
            axis = self.rotateAxis

        rotation_matrix = axis_rotation_matrix(angle, axis)

        #Perform the rotation
        for cube in self.cubes:
            cube.localPos = np.dot(cube.localPos - center, rotation_matrix) + center


    # Rotates a piece in one frame
    def Rotate(self, angle, axis):
        # Convert angle to radians
        angle = math.radians(angle)
        center = np.asfarray(self.cubes[0].localPos)
        rotation_matrix = axis_rotation_matrix(angle, axis)

        for cube in self.cubes:
            cube.localPos = np.rint(np.dot(cube.localPos - center, rotation_matrix)) + center

    #NOTE: Fading in/out can no longer be paused (because this update is no longer locked behind pause status)
    def Update(self, deltaTime, move, paused): #Takes pause status to gatekeep all update actions except ongoing fade and rotate
        #If the game is paused, don't update position
        if not paused:
            self.ang += 50.0 * deltaTime
            self.position += move

        #TEST: Update Cubes within piece regardless of pause status
        for cube in self.cubes:
            cube.Update(deltaTime, move)

        #Smooth Rotations
        if self.rotateDir != None:
            self.RotateSmooth(deltaTime)




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