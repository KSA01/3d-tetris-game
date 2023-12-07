
import pygame
from OpenGL.GL import *
import numpy as np
import math
import Cube
import Triangle

# Initialize the game board grid representing a 10x20 grid (rows x columns)

_isPaused = False
score = 0 

def Init():
    global _cube

    Cube.Init()
    _cube = Cube.Cube(np.asfarray([-1,7,-1]))

    global _triangle

    Triangle.Init()
    _triangle = Triangle.Triangle(np.asfarray([-1,7,1]))

def ProcessEvent(event):
    return False


# def Update(deltaTime):
#     global _cube

#     move = np.asfarray([0, -1*deltaTime, 0]) 
#     if move[1] + _cube.GetPos()[1] <= -5:
#         move[1] += 12

#     global _triangle

#     _cube.Update(deltaTime, move) 
#     _triangle.Update(deltaTime, move)

# Function to update and display the score
def update_score(points):
    global score
    score += points
    print(f"Score: {score}")  # Display the score 

# Global variables to track the state
_currentObject = "cube"  # Start with the cube falling first
_switchHeight = -5  # Height at which we switch objects

_isGamePaused = False  # A new global variable to track the pause state

def Pause():
    global _isGamePaused
    _isGamePaused = True

def Resume():
    global _isGamePaused
    _isGamePaused = False

def Update(deltaTime):
    global _cube
    global _triangle
    global _currentObject
    global _isPaused
    global score

    move = np.asfarray([0, -1 * deltaTime, 0])

    if _currentObject == "cube":
        # Update cube position
        if _cube.GetPos()[1] + move[1] <= _switchHeight:
            # If the cube reaches the switch height, reset its position and switch to the triangle
            _cube.SetPos(np.asfarray([-1, 7, -1]))
            _currentObject = "triangle"
            update_score(100)
        else:
            # Otherwise, just update the cube's position
            _cube.Update(deltaTime, move)

    elif _currentObject == "triangle":
        # Update triangle position
        if _triangle.GetPos()[1] + move[1] <= _switchHeight:
            # If the triangle reaches the switch height, reset its position and switch to the cube
            _triangle.SetPos(np.asfarray([-1, 7, 1]))
            _currentObject = "cube"
            update_score(100)
        else:
            # Otherwise, just update the triangle's position
            _triangle.Update(deltaTime, move)


# def Render():
#     global _cube
#     _cube.Render() 

#     global _triangle
#     _triangle.Render()

def Render():
    global _cube
    global _triangle
    global _isGamePaused

    if not _isGamePaused:
        _cube.Render() 
        _triangle.Render()

