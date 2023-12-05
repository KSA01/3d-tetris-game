from OpenGL.GL import *
import numpy as np

#glRotate guide: (-y right, +y left, +x up, -x down)

def Init():
    #The vertical angle of the camera (ranges from 2 to -2, in increments of 30 degrees. >0 looking down, 0 eye-level, <0 looking up)
    global camPosV
    camPosV = 0

    #Which direction the camera is currently rotating (-1 = right/down, 0 = not rotating, 1 = left/up)
    global camDirH
    global camDirV
    camDirH = 0
    camDirV = 0

    #The degrees the camera has rotated in the current rotation, horizontally and vertically
    global degRotatedH
    global degRotatedV
    degRotatedH = 0
    degRotatedV = 0



#Toggles the camera to move in a given X and Y direction (pass in -1, 0, or 1)
def toggleCamMove(dirH, dirV):
    global camPosV
    global camDirH
    global camDirV

    #If camera not currently rotating horizontally/vertically, toggle it to move in specified direction
    if camDirH == 0:
        camDirH = dirH
    if camDirV == 0:
        #Ensure that the camera does not move 60 degrees above or below 0 (eye-level)
        if camPosV + dirV <= 2 and camPosV + dirV >= -2:
            camDirV = dirV
            #Increment vertical camera position
            camPosV += dirV

            #TEST
            print(camPosV)



#Rotates the camera in a given direction (dir: 0 = up, 1 = down, 2 = left, 3 = right)
def rotateCamera(dir, deltaTime):
    global degRotatedH
    global degRotatedV
    global camDirH
    global camDirV


    #TEST
    #Translate camera to center before rotating
    #glTranslate(-1.0, 0.0, 30.0) #Creates a first person camera effect (not what I want)
    #Need case by case basis?

    #The magnitude of rotation (based on deltaTime and desired direction)
    mag = 0

    #Vertical Rotation

    #Rotate up
    if dir == 0:
        mag = deltaTime * 6 * 30

        #Check if the camera is about to rotate past 30 degrees total for this rotation
        if degRotatedV + mag > 30:
            #Only rotate the remaining degrees for this rotation
            mag = 30 - degRotatedV
            #Reset degrees rotated tracker
            degRotatedV = 0
            #Reset vertical camera movement to 0 (not moving)
            camDirV = 0
        else:
            #Update the degrees rotated tracker
            degRotatedV += abs(mag)

        #Perform the vertical rotation around X axis
        glRotate(mag, 1, 0, 0)

    #Rotate down
    elif dir == 1:
        mag = deltaTime * 6 * 30

        #Check if the camera is about to rotate past 30 degrees total for this rotation
        if degRotatedV + mag > 30:
            #Only rotate the remaining degrees for this rotation
            mag = 30 - degRotatedV
            #Reset degrees rotated tracker
            degRotatedV = 0
            #Reset vertical camera movement to 0 (not moving)
            camDirV = 0
        else:
            #Update the degrees rotated tracker
            degRotatedV += abs(mag)

        #Perform the vertical rotation around X axis
        glRotate(-mag, 1, 0, 0)


    #Horizontal Rotation

    #Rotate left
    elif dir == 2:

        mag = deltaTime * 6 * 90

        #Check if the camera is about to rotate past 90 degrees total for this rotation
        if degRotatedH + mag > 90:
            #Only rotate the remaining degrees for this rotation
            mag = 90 - degRotatedH
            #Reset degrees rotated tracker
            degRotatedH = 0
            #Reset vertical camera movement to 0 (not moving)
            camDirH = 0
        else:
            #Update the degrees rotated tracker
            degRotatedH += abs(mag)

        #Perform the horizontal rotation around Y axis
        glRotate(mag, 0, 1, 0)


    #Rotate right
    elif dir == 3:
        mag = deltaTime * 6 * 90

        #Check if the camera is about to rotate past 90 degrees total for this rotation
        if degRotatedH + mag > 90:
            #Only rotate the remaining degrees for this rotation
            mag = 90 - degRotatedH
            #Reset degrees rotated tracker
            degRotatedH = 0
            #Reset vertical camera movement to 0 (not moving)
            camDirH = 0
        else:
            #Update the degrees rotated tracker
            degRotatedH += abs(mag)

        #Perform the horizontal rotation around Y axis
        glRotate(-mag, 0, 1, 0)



    #TEST
    #Translate camera back out after rotating
    #glTranslate(1.0, 0.0, -30.0)



def Update(deltaTime):
    global camPosV
    global degRotatedH
    global degRotatedV
    global camDirH
    global camDirV

    #Call rotateCamera if camera is toggled to rotate

    if camDirH != 0:
        #Left
        if camDirH > 0:
            rotateCamera(2, deltaTime)
        #Right
        if camDirH < 0:
            rotateCamera(3, deltaTime)


    if camDirV != 0:
        #Up
        if camDirV > 0:
            rotateCamera(0, deltaTime)
        #Down
        if camDirV < 0:
            rotateCamera(1, deltaTime)