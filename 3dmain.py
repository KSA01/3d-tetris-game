import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from freetype import *
import pygame.freetype
from SlowCube import SlowCube 
from SlowTriangle import SlowTriangle 
import Cube
import Triangle
import Border
import GamePlay 

# Initialize the objects
cube = SlowCube()
triangle = SlowTriangle()
_isPaused = False  
# _nextPiece = triangle  

# Initialize Pygame and OpenGL
pygame.init()
size = width, height = 840, 680
screen = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

# Set up the OpenGL context
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width/height), 0.1, 50.0)  # Set the perspective projection
glMatrixMode(GL_MODELVIEW)
glTranslate(1.0, 0.0, -20)  # Move the viewpoint backwards to view the objects
glRotate(-15, 0, 1, 0)
glRotate(30, 1, 0, 0) 

Cube.Init()
Triangle.Init()
GamePlay.Init()


# Enable depth testing for 3D rendering
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

# Font settings for rendering text
font_path = "font/Freedom-10eM.ttf"  # Replace with your font file path
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# score_value = 0

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
    glDeleteTextures(text_texture)

# def draw_score(screen, score, x, y):
#     """Draw the score on the screen"""
#     score = font_path.render("Score: " + str(score_value), True, (255, 255, 255))
#     screen.blit(score, (x, y))


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
        GamePlay.Update(deltaTime)

    return True

# def drawNextPiece():
#     global _nextPiece

#     # Assuming _nextPiece contains information about the piece type
#     # Load the corresponding image. For simplicity, let's assume an image loading function `loadImage(pieceType)`
#     pieceImage = loadImage(_nextPiece)

#     # Position for the top left corner
#     x, y = 10, 10  # You can adjust these values as needed

#     # Draw the image at (x, y)
#     glBindTexture(GL_TEXTURE_2D, pieceImage)
#     glBegin(GL_QUADS)
#     glTexCoord2f(0, 0); glVertex2f(x, y)
#     glTexCoord2f(1, 0); glVertex2f(x + pieceImageWidth, y)
#     glTexCoord2f(1, 1); glVertex2f(x + pieceImageWidth, y + pieceImageHeight)
#     glTexCoord2f(0, 1); glVertex2f(x, y + pieceImageHeight)
#     glEnd()
#     glBindTexture(GL_TEXTURE_2D, 0)


def Render(score):
    """ Handles the rendering of objects and text """
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    # Setting up orthographic projection for text rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, height, 0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Render the text
    render_text(f"Score: {score}", 10, 10, 36)

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

# Main loop
score = 0 
_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
while Update(_gDeltaTime):
    Render(score)
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTickLastFrame) / 1000.0  # Calculate the time since last frame
    _gTickLastFrame = t

pygame.quit()
