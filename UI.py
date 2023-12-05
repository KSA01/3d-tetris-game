# UI.py

import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

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
    
#UI