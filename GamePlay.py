# GamePlay.py

import pygame
from OpenGL.GL import *
import numpy as np
import math
import random
import Cube
import Pieces

def Init():
    #global _pieces
    global _piece
    global OnStart
    global moveUp, moveDown, moveLeft, moveRight, rotateLeft, rotateRight, rotateDown

    #Cube.Init()
    Pieces.Init()
    #_pieces = Pieces.tetrisPieces
    #_cube = Cube.Cube(np.asfarray([-1,7,-1]))
    OnStart = True
    moveUp, moveDown, moveLeft, moveRight, rotateLeft, rotateRight, rotateDown = False, False, False, False, False, False, False

def ProcessEvent(event):
    global moveUp, moveDown, moveLeft, moveRight, rotateLeft, rotateRight, rotateDown
    #add player key shift movements using arrow keys
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            moveLeft = True
            #piece.Move((-2, 0, 0))
        elif event.key == pygame.K_RIGHT:
            moveRight = True
            #piece.Move((2, 0, 0))
        elif event.key == pygame.K_DOWN:
            moveDown = True
            #piece.Move((0, 0, 2))
        elif event.key == pygame.K_UP:
            moveUp = True
            #piece.Rotate(90, (0, 0, -2))
        elif event.key == pygame.K_a:
            rotateLeft = True
        elif event.key == pygame.K_d:
            rotateRight = True
        elif event.key == pygame.K_s:
            rotateDown = True

    return False

index = random.randint(0, 6)

#ALFREDO
_isGamePaused = False  # A new global variable to track the pause state

def Pause():
    global _isGamePaused
    _isGamePaused = True

def Resume():
    global _isGamePaused
    _isGamePaused = False
#ALFREDO

def Update(deltaTime, pieces):
    global _piece
    global index
    global OnStart
    global moveUp, moveDown, moveLeft, moveRight, rotateLeft, rotateRight, rotateDown

    _piece = pieces[index]

    if OnStart:
        updatePos = (0, 6, -2)
        _piece.SetPos(updatePos)
        OnStart = False

        #NEW
        #Toggle cubes of piece to fade in
        _piece.ToggleCubes(True, False)


    #move = np.asfarray([-4, 12, 0])

    # Check if piece hits the bottom
    move = np.asfarray([0, -2*deltaTime, 0])
    if move[1] + _piece.GetPos()[1] <= -5:
        index = random.randint(0, 6)
        OnStart = True
        move[1] += 24

    #NEW
    #Check if piece is close to bottom
    if move[1] + _piece.GetPos()[1] <= -4:
        #Toggle cubes of piece to fade out
        _piece.ToggleCubes(False, True)

    # Check if piece is not at z limit then move
    if _piece.GetPos()[2] >= -4:
        if moveUp:
            move[2] += -2
            moveUp = False
    if _piece.GetPos()[2] <= 1.5:
        if moveDown:
            move[2] += 2
            moveDown = False

    # Check if piece is not at x limit then move
    if _piece.GetPos()[0] >= -3:
        if moveLeft:
            move[0] += -2
            moveLeft = False
    if _piece.GetPos()[0] <= 3:
        if moveRight:
            move[0] += 2
            moveRight = False

    # Rotate piece
    if rotateLeft:
        _piece.Rotate(90, (0, 0, -2))
        rotateLeft = False
    elif rotateRight:
        _piece.Rotate(-90, (0, 0, -2))
        rotateRight = False
    elif rotateDown:
        _piece.Rotate(90, (0, -2, 0))
        rotateDown = False

    _piece.Update(deltaTime, move)

def Render(piece):
    global _piece

    _piece = piece

    _piece.Render()