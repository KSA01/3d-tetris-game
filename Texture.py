from OpenGL.GL import *
import numpy as np
import math

from OpenGL.arrays import vbo
from OpenGL.GL import shaders
import pygame

#NEW
class Texture:
    def __init__(self, filepath):

        #Allocate space in memory for texture
        self.texture = glGenTextures(1) #Need &textureId ?
        #Bind as the current texture to work with
        glBindTexture(GL_TEXTURE_2D, self.texture)
        #Set parameters for texture behavior
        #Texture Wrap options determine behavior for when s and t coordinates fall outside of range 0-1
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        #Min/Mag filter sets behavior for when image dimensions differ from expected values
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        #Load in image via pygame, convert to device-friendly pixel format
        img = pygame.image.load(filepath).convert()
        #Get width/height of image
        img_width, img_height = img.get_rect().size
        #Convert pygame image to RGBA (red green blue alpha) string format so it can be read by OpenGL
        img_str = pygame.image.tostring(img, "RGBA")
        #Load the image into OpenGL. Arguments: (texture location to upload to, mipmap level, internal format, w, h, border color, format of data loading in, data format, image data)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_str)
        #Generate mipmap based on the image loaded in (downscales image as it gets further away)
        #Don't need this, it will make things more complicated
        #glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    #Free from memory (probably don't need yet)
    def destroy(self):
        glDeleteTextures(1, (self.texture,))