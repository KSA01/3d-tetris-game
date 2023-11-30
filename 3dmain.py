# 3dmain.py

import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
#from SlowCube import SlowCube
from SlowTriangle import SlowTriangle
import Cube
import Pieces
import Border
import GamePlay

#Need to install for UI
from freetype import *
import pygame.freetype

pygame.init()
size = width, height = 640, 750
screen = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width/height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

#NEW
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

glTranslate(1.0, 0.0, -30.0)     #translates the camera
glRotate(-15, 0, 1, 0)           #rotate -15 degrees around y
glRotate(30, 1, 0, 0)            #rotate 30 degrees around x

Cube.Init()
#cube = Cube.Cube()
#cube = SlowCube()
GamePlay.Init()
_isPaused = False  

#UI
triangle = SlowTriangle()
#UI

tetrisPieces = Pieces.createTetrisPieces()
#print("NUM TETRIS PIECES: " + str(len(tetrisPieces)))

tetrisCubes = 0
for piece in tetrisPieces:
    tetrisCubes += len(piece.cubes)

#print("NUMBER OF CUBES: " + str(tetrisCubes))



#UI

# Font settings for rendering text
font_path = "font/Freedom-10eM.ttf"  # Replace with your font file path

def render_text(text, x, y, font_size):
    """ Renders text onto the screen """
    font = pygame.freetype.Font(font_path, font_size)
    text_surface, _ = font.render(text, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)

    text_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, text_texture)
    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # Create texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_surface.get_width(), text_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    # Render the text as a texture
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, text_texture)
    glBegin(GL_QUADS)
    # Map the text texture onto a quad
    glTexCoord2f(0, 1); glVertex2f(x, y)
    glTexCoord2f(1, 1); glVertex2f(x + text_surface.get_width(), y)
    glTexCoord2f(1, 0); glVertex2f(x + text_surface.get_width(), y + text_surface.get_height())
    glTexCoord2f(0, 0); glVertex2f(x, y + text_surface.get_height())
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # Clean up the texture
    #glDeleteTextures(text_texture)

#UI








def Update(deltaTime):
    global _isPaused  # Access the global pause variable

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Check if ESC key is pressed
                _isPaused = not _isPaused  # Toggle the pause state
                if _isPaused:
                    GamePlay.Pause()  # Call a new function to handle pause in GamePlay
                else:
                    GamePlay.Resume()  # Call a new function to handle resume in GamePlay
                continue
        if _isPaused:
            continue  # Skip the rest of the loop if the game is paused
        if GamePlay.ProcessEvent(event):
            continue

    if not _isPaused:  # Only update game state if not paused
        GamePlay.Update(deltaTime, tetrisPieces)

    #GamePlay.Update(deltaTime)

    #cube.Update(deltaTime)
    #for piece in tetrisPieces:
        #piece.Update(deltaTime)
    # GamePlay.Update(deltaTime, tetrisPieces)

    #UI
    triangle.Update(deltaTime)
    #UI

    return True

def Render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    #NEW
    #Render Border first so transparency works correctly
    Border.Render()

    #cube.Render()
    for piece in tetrisPieces:
        #piece.Render()
        GamePlay.Render(piece)
    
    #GamePlay.Render()
    
    # Setting up orthographic projection for text rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, height, 0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Render the text
    render_text("     next", 10, 10, 48)

    # Restore the previous projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    # Render the cube and triangle
    # cube.Render() 
    # triangle.Render()
    GamePlay.Render()
    Border.Render()

    # Update the display
    pygame.display.flip()

_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
while Update(_gDeltaTime):
    Render()
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTickLastFrame) / 1000.0
    _gTickLastFrame = t
