from OpenGL.GL import *
import numpy as np

_lightVector = np.asarray([0, 0, 1, 0], dtype=np.float32)  # Define a light vector for lighting effects

class SlowTriangle:
    def __init__(self):
        # Define the vertices of the triangle around the origin
        self.verts = np.asarray([(0, 0, 0),
                                  (0.5, 0, 0),
                                  (0, 0.5, 0)], dtype=np.float32)
        # Define the surfaces as a single triangle
        self.surfaces = np.array([(0, 1, 2)])
        # Define the normal to the surface of the triangle
        self.normals = np.asarray([(0, 0, 1, 0)], dtype=np.float32)
        self.color = np.asarray([1, 0, 0], dtype=np.float32)  # Red color for the triangle

        self.ang = 0  # Initial rotation angle
        self.axis = (0, 0, 1)  # Axis of rotation

    def Update(self, deltaTime):
        # Update the rotation angle over time
        self.ang += 60.0 * deltaTime

    def _DrawBlock(self):
        global _lightVector

        # Calculate the lighting effect based on the current modelview matrix
        inv = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX))
        light = np.matmul(_lightVector, inv)

        glBegin(GL_TRIANGLES)  # Begin drawing triangles
        for n, surface in enumerate(self.surfaces):
            for vert in surface:
                # Calculate the color intensity based on light direction
                dotP = np.dot(light, self.normals[n])
                mult = max(min(dotP, 1), 0)
                glColor3fv(self.color * mult)  # Set the color
                glVertex3fv(self.verts[vert])  # Draw the vertex
        glEnd()  # End drawing triangles

    def Render(self):
        m = glGetDouble(GL_MODELVIEW_MATRIX)  # Save current matrix

        # Translate the triangle to the bottom left corner
        glTranslatef(-1.5, -1.5, 0)  # Adjust these values as needed for positioning

        # Apply rotation to the triangle
        glRotatef(self.ang, *self.axis)
        self._DrawBlock()  # Draw the triangle

        glLoadMatrixf(m)  # Restore the saved matrix
