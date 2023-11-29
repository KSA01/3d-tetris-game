# Pieces.py

from OpenGL.GL import *
import numpy as np
import math
import random
import quaternion

from Cube import * #Cube, Init, axis_rotation_matrix
#import GamePlay

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

        self.cubes = [Cube(localPos, color, filepath) for localPos in localPositions]
        self.position = position        #takes position of each piece
        self.ang = 0
        self.axis = (3,1,1)             
        self.color = np.asfarray(color)  #takes a different color for each piece
        self.vel = random.randrange(1, 3)
        self.rotation_quat = (1, 0, 0, 0)  # Initialize rotation quaternion

        self.transforms = [np.eye(4) for _ in range(cubeCount)]

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
        '''rotation_quat = axis_rotation_quaternion(angle, axis)
        self.rotation_quat = q_mult(self.rotation_quat, rotation_quat)

        for cube in self.cubes:
            # Rotate each cube using the quaternion
            rotated_position = qv_mult(rotation_quat, cube.localPos)
            cube.localPos = rotated_position'''
        
        axis_quaternion = quaternion.from_rotation_vector(np.radians(angle) * np.array(axis) / np.linalg.norm(axis))

        for cube in self.cubes:
            local_pos_quaternion = quaternion.quaternion(0, *map(float, cube.localPos))
            rotated_pos_quaternion = axis_quaternion * local_pos_quaternion * axis_quaternion.conj()
            cube.localPos = np.imag(rotated_pos_quaternion)[1:]
        
        self.rotation_quat = quaternion.multiply(axis_quaternion, self.rotation_quat)

        '''rotation_matrix = axis_rotation_matrix(angle, axis)
        for cube in self.cubes:
            newPos = np.dot(cube.localPos, rotation_matrix)
            print(newPos)
            for i in range(3):
                newPos[i] = round(newPos[i])
            cube.localPos = newPos
            print(cube.localPos)'''

    def Update(self, deltaTime, move):
        self.ang += 50.0 * deltaTime
        self.position += move

    def Render(self):
        #m = glGetDouble(GL_MODELVIEW_MATRIX)
        #center = self.cubes[0].localPos

        glPushMatrix()
        # Apply rotation to the cube
        #glMultMatrixf(q_to_mat4(self.rotation_quat))
        glTranslatef(*self.position)
        #glRotatef(self.ang, *center)
        for cube in self.cubes:
            cube.Render()
        glPopMatrix()
        
        #glLoadMatrixf(m)