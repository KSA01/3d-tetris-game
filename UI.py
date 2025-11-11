# UI.py

import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

#UI

# Font settings for rendering text
font_path = "font/Beyonders.ttf"  # Replace with your font file path

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
    glColor3f(1.0, 1.0, 0.0) # sets the color of the text - yellow
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
    if image_path == "Icons/IIcon.png":
        width /= 2.5
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
    glColor3f(1.0, 1.0, 1.0) # Sets the color of the next piece icon - keep white
    glBegin(GL_QUADS)
    # Map the image texture onto a quad
    glTexCoord2f(0, 1); glVertex2f(x, y)
    glTexCoord2f(1, 1); glVertex2f(x + width, y)
    glTexCoord2f(1, 0); glVertex2f(x + width, y + height)
    glTexCoord2f(0, 0); glVertex2f(x, y + height)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def get_text_size(text, font_size):
    """ Get the width and height of text """
    font = pygame.freetype.Font(font_path, font_size)
    text_surface, _ = font.render(text, (255, 255, 255))
    return text_surface.get_width(), text_surface.get_height()

def render_button(x, y, width, height, text, font_size=24, hover=False):
    """ Renders a button with text. Returns the button's bounding box for click detection """
    # Assume depth test is already disabled by the caller for UI rendering
    # Just ensure blending is enabled
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Draw button background
    glDisable(GL_TEXTURE_2D)
    if hover:
        glColor4f(0.4, 0.4, 0.4, 0.95)  # Darker when hovering
    else:
        glColor4f(0.25, 0.25, 0.25, 0.95)  # Normal color - slightly lighter for better visibility
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()
    
    # Draw button border
    glColor4f(1.0, 1.0, 1.0, 1.0)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()
    
    # Render button text (centered) - use white color for visibility
    # Get text size for centering
    font = pygame.freetype.Font(font_path, font_size)
    text_surface, _ = font.render(text, (255, 255, 255))
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    text_x = x + (width - text_width) // 2
    text_y = y + (height - text_height) // 2
    
    # Use render_text_color which we know works correctly
    # This ensures consistent text rendering and proper visibility
    render_text_color(text, text_x, text_y, font_size, (1.0, 1.0, 1.0))
    
    return (x, y, x + width, y + height)

def is_point_in_button(mouse_x, mouse_y, button_bounds):
    """ Check if a point is within a button's bounds """
    x1, y1, x2, y2 = button_bounds
    return x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2

def render_text_color(text, x, y, font_size, color=(1.0, 1.0, 0.0)):
    """ Renders text with a custom color (RGB tuple, values 0-1) """
    font = pygame.freetype.Font(font_path, font_size)
    text_surface, _ = font.render(text, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)

    text_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, text_texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_surface.get_width(), text_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, text_texture)
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(x, y)
    glTexCoord2f(1, 1); glVertex2f(x + text_surface.get_width(), y)
    glTexCoord2f(1, 0); glVertex2f(x + text_surface.get_width(), y + text_surface.get_height())
    glTexCoord2f(0, 0); glVertex2f(x, y + text_surface.get_height())
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
#UI