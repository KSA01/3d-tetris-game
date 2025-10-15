# Pieces.py

from OpenGL.GL import *
import numpy as np
import math
from Cube import *
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

borders = (
    (-8, 8),
    (-5, 30),
    (-8, 8)
)

pieceNames = ["I", "J", "L", "O", "S", "T", "Z"]  # List of pieces by name
cubeCount = 4 # Amount of cubes per piece

tetrisPieces = []

CubeList = []

# A function to create Tetris pieces
def createTetrisPieces():

    for i in range(len(pieceNames)):
        piece = Piece(position=(0, 18, 0), color=colors[i], name=pieceNames[i], filepath=filepaths[i]) 
        tetrisPieces.append(piece)

    return tetrisPieces

def checkCubeCol(piece):
    # Collect position of all cubes in the piece
    for cube in piece.cubes:
        locPos = np.round(cube.GetCubePos()) + np.round(piece.GetPos())
        
        # Check if any cube in CubeList is within a distance of 2 in all three axes
        if any(all(np.abs(locPos - np.round(pos.GetCubePos())) < 2) for pos in CubeList):
            #print("Overlaps")
            return False  # overlaps

    return True # no overlaps

def freezeCubes(cube):
    CubeList.append(cube)

# function for ending the game once the player has lost
def CheckForCeil():
    if CubeList:
        for cube in CubeList:
            if np.rint(cube.GetCubePos()[1]) >= 8:
                return False
    
    return True

#Alfredo
#checks if bottom row is filled
def CheckForPoint():
    count = 0   # counter for cubes at bottom
    for cube in CubeList:
        if cube.GetCubePos()[1] <= -4.9:  # bottom y coord is -5
            count += 1
    if count >= 64:  # if there are this many cubes at bottom (8x8 layer)
        count = 0
        return False

    return True
#Alfredo

class Piece:
    def __init__(self, position, color, name, filepath):
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


    #Smooth Rotations
    #Takes a direction (left, right, down) and toggles the piece to rotate that way over 1/6s
    def ToggleRotate(self, dir):
        #If the piece is not currently rotating, toggle it to rotate in the given direction
        if self.rotateDir == None:
            self.rotateDir = dir

            #Reset rads rotated counter (for new rotation)
            self.radRotated = 0

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


    def RotateSmooth(self, deltaTime):
        # defines cur/prev pos in case to revert
        curLocalPositions = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        for i, cube in enumerate(self.cubes):
            curPos = cube.GetCubePos()
            curLocalPositions[i] = np.rint(curPos)

        #Tracks the rotation direction for this frame (for edge case)
        #This is needed in case rotation gets cancelled on the last frame of rotation (and self.rotateDir is None when reverting rotation)
        rotateDirThisFrame = self.rotateDir

        #Tracks if the rotation has failed
        failed = False

        center = np.asfarray(self.cubes[0].localPos)

        #The magnitude of the angle of rotation (in radians)
        mag = math.radians(90 * 6 * deltaTime)

        if self.rotateDir == "left":
            #If the rotation is almost complete, rotate the rest of the way
            if (self.radRotated + mag) >= math.radians(90):
                mag = math.radians(90) - self.radRotated
                #Reset rotation counter and rotation status
                #self.radRotated = math.radians(0)
                self.rotateDir = None
            else:
                #self.radRotated += mag
                pass

            self.radRotated += mag

            angle = mag
            axis = self.rotateAxis

        elif self.rotateDir == "right":
            #If the rotation is almost complete, rotate the rest of the way
            if (self.radRotated + mag) >= math.radians(90):
                mag = math.radians(90) - self.radRotated
                #Reset rotation counter and rotation status
                #self.radRotated = math.radians(0)
                self.rotateDir = None
            else:
                #self.radRotated += mag
                pass

            self.radRotated += mag

            angle = mag
            axis = self.rotateAxis

        elif self.rotateDir == "down":
            #If the rotation is almost complete, rotate the rest of the way
            if (self.radRotated + mag) >= math.radians(90):
                mag = math.radians(90) - self.radRotated
                #Reset rotation counter and rotation status
                #self.radRotated = math.radians(0)
                self.rotateDir = None
            else:
                #self.radRotated += mag
                pass

            self.radRotated += mag

            angle = -mag
            axis = self.rotateAxis

        rotation_matrix = axis_rotation_matrix(angle, axis)

        #Perform the rotation
        for cube in self.cubes:
            cube.localPos = np.dot(cube.localPos - center, rotation_matrix) + center
            
            # checks if in bounds or colliding and if so reverts cube positions 
            if not self.CheckInBounds() or not checkCubeCol(self):
                #print("collision detected, reverting rotation")
                failed = True


        if failed:
                #print("collision detected, reverting rotation")

                #self.RevertCubePos(curLocalPositions)

                #Revert piece back to its original orientation by reversing the current rotation
                if rotateDirThisFrame == "down":
                    self.Rotate(self.radRotated, self.rotateAxis)
                else:
                    #print("reverting horiz rotation")
                    self.Rotate(self.radRotated, (self.rotateAxis[0], -self.rotateAxis[1], self.rotateAxis[2]))

                #Toggle the piece to stop rotating
                self.rotateDir = None


    #Smooth Rotations


    # Rotates a piece in one frame
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
            if not self.CheckInBounds() or not checkCubeCol(self):
                self.RevertCubePos(curLocalPositions)
                break

    # Check if all cubes of a piece are in bounds
    def CheckInBounds(self):
        for cube in self.cubes:
            for i in range(3): # for each axis (x,y,z)
                pos = cube.GetCubePos() + np.rint(self.position)
                # checks if each axis value is between border limits for that axis
                if pos[i] <= borders[i][0] or pos[i] >= borders[i][1]:
                    return False  # Cube is out of bounds for at least one dimension

        return True  # All cubes are within bounds for all dimensions

    #NOTE: Fading in/out can no longer be paused (because this update is no longer locked behind pause status)
    def Update(self, deltaTime, move, paused): #Takes pause status to gatekeep all update actions except ongoing fade and rotate
        #If the game is paused, don't update position
        if not paused:
            self.ang += 50.0 * deltaTime
            self.position += move

            if not self.CheckInBounds():
                self.position[0] = self.lastPosition[0]
                self.position[2] = self.lastPosition[2]
                
            # Save last position
            self.lastPosition = np.copy(self.position)

        #TEST: Update Cubes within piece regardless of pause status
        for cube in self.cubes:
            cube.Update(deltaTime)

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
