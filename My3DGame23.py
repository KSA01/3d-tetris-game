import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from freetype import *
import pygame.freetype
from SlowCube import SlowCube 
from SlowTriangle import SlowTriangle 
import Border

# Initialize the objects
cube = SlowCube()
triangle = SlowTriangle()

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

# Enable depth testing for 3D rendering
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

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
    glDeleteTextures(text_texture)

def Update(deltaTime):
    """ Handles updating the state of objects and checking for quit event """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    cube.Update(deltaTime)
    triangle.Update(deltaTime)

    return True

def Render():
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
    render_text("Hello World", 10, 10, 48)

    # Restore the previous projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    # Render the cube and triangle
    cube.Render() 
    triangle.Render()
    Border.Render()

    # Update the display
    pygame.display.flip()

# Main loop
_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
while Update(_gDeltaTime):
    Render()
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTickLastFrame) / 1000.0  # Calculate the time since last frame
    _gTickLastFrame = t

pygame.quit()
