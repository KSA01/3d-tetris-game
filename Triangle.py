from OpenGL.GL import *
import numpy as np
from OpenGL.arrays import vbo
from OpenGL.GL import shaders

# Vertex data: 3 positions (x, y, z), 3 normals (nx, ny, nz), 2 UVs (u, v)
_verts = np.float32([
    # Front face
    (0, 1, 0, 0, 0, 1, 0.5, 1),   # Top vertex
    (-1, -1, 0, 0, 0, 1, 0, 0),   # Bottom left
    (1, -1, 0, 0, 0, 1, 1, 0),    # Bottom right
])

def Init():
    global _shader
    global _vbo
    global _uniformInv
    global _position
    global _color
    global _vertex_normal

    _VERTEX_SHADER = shaders.compileShader("""
    uniform mat4 inv;
    attribute vec3 position;
    uniform vec3 color;
    attribute vec3 vertex_normal;
    varying vec4 vertex_color;
    void main() {
        gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0);
        vec4 light = inv * vec4(0, 0, 1, 0);
        float dt = dot(light.xyz, vertex_normal);
        float mult = max(min(dt, 1.0), 0.0);
        vertex_color = vec4(color * mult, 1.0);
    }
    """, GL_VERTEX_SHADER)

    _FRAGMENT_SHADER = shaders.compileShader("""
    varying vec4 vertex_color;
    void main() {
        gl_FragColor = vertex_color;
    }
    """, GL_FRAGMENT_SHADER)

    _shader = shaders.compileProgram(_VERTEX_SHADER, _FRAGMENT_SHADER)
    _vbo = vbo.VBO(_verts)

    _uniformInv = glGetUniformLocation(_shader, "inv")
    _position = glGetAttribLocation(_shader, "position")
    _color = glGetUniformLocation(_shader, "color")
    _vertex_normal = glGetAttribLocation(_shader, "vertex_normal")

class Triangle:
    def __init__(self, pos):
        self.color = np.asfarray([1, 0, 0])  # Red color
        self.pos = pos

    def GetPos(self):
        return self.pos

    def SetPos(self, pos):
        self.pos = pos

    def Update(self, deltaTime, move):
        self.pos += move

    def _DrawShape(self):
        global _shader
        global _vbo
        global _uniformInv
        global _position
        global _color
        global _vertex_normal

        shaders.glUseProgram(_shader)

        inv = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX))
        glUniformMatrix4fv(_uniformInv, 1, False, inv)
        glUniform3fv(_color, 1, self.color)

        try:
            _vbo.bind()
            try:
                glEnableVertexAttribArray(_position)
                glEnableVertexAttribArray(_vertex_normal)

                stride = 32
                glVertexAttribPointer(_position, 3, GL_FLOAT, False, stride, _vbo)
                glVertexAttribPointer(_vertex_normal, 3, GL_FLOAT, False, stride, _vbo + 12)

                glDrawArrays(GL_TRIANGLES, 0, 3)  # Draw 3 vertices for the triangle
            finally:
                _vbo.unbind()
                glDisableVertexAttribArray(_position)
                glDisableVertexAttribArray(_vertex_normal)
        finally:
            shaders.glUseProgram(0)

    def Render(self):
        m = glGetDouble(GL_MODELVIEW_MATRIX)

        glTranslatef(*self.pos)
        self._DrawShape()

        glLoadMatrixf(m)

# Example usage
if __name__ == "__main__":
    # Initialize OpenGL context and create a window (not shown here)
    # ...

    Init()

    triangle = Triangle(np.array([0, 0, 0]))  # Create a triangle at the origin

    # Main loop (not shown here)
    # ...
