# Cube.py

from OpenGL.GL import *
import numpy as np
from math import *

from OpenGL.arrays import vbo
from OpenGL.GL import shaders

import pygame
from Texture import Texture

# 3 positions, 3 normals, 2 UVs
_verts = np.float32([(1, -1, -1, 0, 0, -1, 0, 0),   # first - 8 vertices x 3
                    (1, 1, -1, 0, 0, -1, 1, 0),
                    (-1, 1, -1, 0, 0, -1, 1, 1),
                    (-1, -1, -1, 0, 0, -1, 0, 1),

                    (-1, -1, -1, -1, 0, 0, 0, 0),
                    (-1, 1, -1, -1, 0, 0, 1, 0),
                    (-1, 1, 1, -1, 0, 0, 1, 1),
                    (-1, -1, 1, -1, 0, 0, 0, 1),

                    (-1, -1, 1, 0, 0, 1, 0, 0),    # second
                    (-1, 1, 1, 0, 0, 1, 1, 0),
                    (1, 1, 1, 0, 0, 1, 1, 1),
                    (1, -1, 1, 0, 0, 1, 0, 1),
                                  
                    (1, -1, 1, 1, 0, 0, 0, 0),
                    (1, 1, 1, 1, 0, 0, 1, 0),
                    (1, 1, -1, 1, 0, 0, 1, 1),
                    (1, -1, -1, 1, 0, 0, 0, 1),
                                  
                    (1, 1, -1, 0, 1, 0, 0, 0),   # third
                    (1, 1, 1, 0, 1, 0, 1, 0),
                    (-1, 1, 1, 0, 1, 0, 1, 1),
                    (-1, 1, -1, 0, 1, 0, 0, 1),
                                  
                    (1, -1, 1, 0, -1, 0, 0, 0),
                    (1, -1, -1, 0, -1, 0, 1, 0),
                    (-1, -1, -1, 0, -1, 0, 1, 1),
                    (-1, -1, 1, 0, -1, 0, 0, 1)
                    ])

borders = (
    (-4, 4),
    (-5, 30),
    (-4, 4)
)

def Init():
    global _shader
    global _vbo
    global _verts
    global _uniformInv
    global _position
    global _color
    global _vertex_normal

    global _uv_coords


    _VERTEX_SHADER = shaders.compileShader("""
        uniform mat4 inv;
        attribute vec3 position;
                                           
        /*uniform vec3 color;*/

        /*NEW*/                          
        uniform vec4 color;

        attribute vec3 vertex_normal;
        varying vec4 vertex_color;                               
        attribute vec2 inTexCoord;
        varying vec2 vertexTexCoord;
                                           
        void main()
        {
            gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0);
            vec4 light = inv * vec4(0, 0, 1, 0);
            float dt = dot(light.xyz, vertex_normal);
            float mult = max(min(dt, 1.0), 0.0);

            /*NEW*/
            vertex_color = vec4(color.xyz * mult, color.w);

            /*CHANGED*/
            /*vertex_color = vec4(color * mult, 0.8);*/
                                           
            vertexTexCoord = inTexCoord;
        }
    """, GL_VERTEX_SHADER)

    _FRAGMENT_SHADER = shaders.compileShader("""
        varying vec4 vertex_color;           
        varying vec2 vertexTexCoord;
        uniform sampler2D myTex;
                                             
        void main()
        {
            /*NEW*/
            vec4 t = vec4(texture(myTex, vertexTexCoord).xyz, 1);
            gl_FragColor = t * vertex_color;
                                             
            /*gl_FragColor = texture(myTex, vertexTexCoord) * vertex_color;*/
        }
    """, GL_FRAGMENT_SHADER)

    _shader = shaders.compileProgram(_VERTEX_SHADER, _FRAGMENT_SHADER)
    _vbo = vbo.VBO(_verts)

    _uniformInv = glGetUniformLocation(_shader, "inv")
    _position = glGetAttribLocation(_shader, "position")
    _color = glGetUniformLocation(_shader, "color")
    _vertex_normal = glGetAttribLocation(_shader, "vertex_normal")
    _uv_coords = glGetAttribLocation(_shader, "inTexCoord")

class Cube:
    def __init__(self, localPos, color=([0,0,1,1]), filepath="blueberryI.png"):
        #super().__init__()
        self.color = np.asfarray(color)
        self.ang = 0
        self.axis = (3,1,1)
        self.localPos = localPos   # Takes local positions of the current cube from pieces

        self.filepath = filepath

        #Generate the texture
        self.fruit_texture = Texture(self.filepath)

        #NEW
        #Tracks if the fade in animation is ongoing
        self.appearing = False
        #Tracks if the fade out animation is ongoing
        self.disappearing = False


    def GetCubePos(self):
        return self.localPos

    def SetCubePos(self, newPos):
        self.localPos = newPos

    # Check if cube is in bounds
    def CheckInBounds(self, piece):
        for i in range(3): # for each axis (x,y,z)
            pos = np.round(self.GetCubePos()) + np.round(piece.GetPos())
            # checks if each axis value is between border limits for that axis
            if pos[i] <= borders[i][0] or pos[i] >= borders[i][1]:
                return False  # Cube is out of bounds for at least one dimension

        return True  # All cubes are within bounds for all dimensions

    #NEW
    #Fade in a cube over 1/6 of a second
    def FadeIn(self, deltaTime):
        #If cube is appearing, increase alpha value by 6x the time passed
        if self.appearing == True:
            self.color[3] += (deltaTime * 6)

            #If cube is now fully visible, restrain alpha to 1 and set appearing status to False
            if self.color[3] >= 1:
                self.color[3] = 1
                self.color[3] = 1
                self.appearing = False
                #print("Fully visible")
        

    #Fade out a cube over 1/6 of a second
    def FadeOut(self, deltaTime):
        #If piece is disappearing, decrease alpha value by 6x the time passed
        if self.disappearing == True:
            self.color[3] -= (deltaTime * 6)

            #If piece is now fully transparent, restrain alpha to 0 and set disappearing status to False
            if self.color[3] <= 0:
                self.color[3] = 0
                self.disappearing = False
                #print("Fully transparent")

    def Update(self, deltaTime):
        self.ang += 50.0 * deltaTime
        #self.localPos += move #This was commented out on mine #BUG

        #NEW
        #If cube is appearing, call fade in function
        if self.appearing == True:
            self.FadeIn(deltaTime)
        #Otherwise, if cube is disappearing, call fade out function
        elif self.disappearing == True:
            self.FadeOut(deltaTime)

    def _DrawBlock(self):
        global _shader
        global _vbo
        global _verts
        global _uniformInv
        global _position
        global _color
        global _vertex_normal
        global _uv_coords

        
        #Set the texture of the block
        self.fruit_texture.use()


        shaders.glUseProgram(_shader)

        inv = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX))
        glUniformMatrix4fv(_uniformInv, 1, False, inv)
        
        #glUniform3fv(_color, 1, self.color)
        
        #CHANGED
        glUniform4fv(_color, 1, self.color)

        try:
            _vbo.bind()
            try:
                glEnableVertexAttribArray(_position)
                glEnableVertexAttribArray(_vertex_normal)
                glEnableVertexAttribArray(_uv_coords)
                stride = 32
                glVertexAttribPointer(_position, 3, GL_FLOAT, False, stride, _vbo)
                glVertexAttribPointer(_vertex_normal, 3, GL_FLOAT, True, stride, _vbo+12)
                glVertexAttribPointer(_uv_coords, 2, GL_FLOAT, True, stride, _vbo+24)
                glDrawArrays(GL_QUADS, 0, 24)
            finally:
                _vbo.unbind()
                glDisableVertexAttribArray(_position)
                glDisableVertexAttribArray(_vertex_normal)
                glDisableVertexAttribArray(_uv_coords)
        finally:
            shaders.glUseProgram(0)
    
    def Render(self):  # Change these 2 values to adjust size
        #m = glGetDouble(GL_MODELVIEW_MATRIX)

        glPushMatrix()
        glTranslatef(*self.localPos)     # Translates the local position of each cube from pieces.py
        #glRotatef(self.ang, *self.axis)
        self._DrawBlock()
        glPopMatrix()

        #glLoadMatrixf(m)