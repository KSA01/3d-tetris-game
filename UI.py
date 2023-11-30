

import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def render_image(x, y, width, height, image_path):
    """ Renders an image onto the screen with specified width and height """
    image_surface = pygame.image.load(image_path)
    image_surface = pygame.transform.scale(image_surface, (width, height))
    image_data = pygame.image.tostring(image_surface, "RGBA", True)

    image_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, image_texture)
    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # Create texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    # Render the image as a texture
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, image_texture)
    glBegin(GL_QUADS)
    # Map the image texture onto a quad
    glTexCoord2f(0, 1); glVertex2f(x, y)
    glTexCoord2f(1, 1); glVertex2f(x + width, y)
    glTexCoord2f(1, 0); glVertex2f(x + width, y + height)
    glTexCoord2f(0, 0); glVertex2f(x, y + height)
    glEnd()
    glDisable(GL_TEXTURE_2D)