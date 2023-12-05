from OpenGL.GL import *
import numpy as np


def Init():
    #The vertical angle of the camera (ranges from 2 to -2, in increments of 30 degrees. >0 looking down, 0 eye-level, <0 looking up)
    global camPosV
    camPosV = 0

    #NEW
    #A list containing the four horizontal views, each named after the axis facing the camera
    global sides
    sides = ['z', 'x', '-z', '-x']
    #Tracks the current side being viewed from (used for proper vertical rotations)
    global curSide
    curSide = 0

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




#Toggles the camera to move in a given H or V direction (pass in -1, 0, or 1)
def toggleCamMove(dirH, dirV):
    global camPosV
    global camDirH
    global camDirV
    global sides
    global curSide

    #If the camera is not currently rotating, toggle it to rotate in a given direction (horizontal movement takes priority)
    if camDirH == 0 and camDirV == 0:
        #Horizontal movement
        if dirH != 0:
            camDirH = dirH
            #Update current side (since rotating horizontally changes the axis parallel with camera)
            if curSide + camDirH < 0:
                curSide = 3
            elif curSide + camDirH > 3:
                curSide = 0
            else:
                curSide += camDirH
            
            #print("Current axis pointing to camera:")
            #print(sides[curSide])

        #Vertical movement
        elif dirV != 0:
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
    global sides
    global curSide

    #The magnitude of rotation (based on deltaTime and desired direction)
    mag = 0

    #Calculate the magnitude of rotation based on direction (90 or 30 degrees over 1/6s for horizontal/vertical)
    
    #Vertical rotation
    if dir == 0 or dir == 1:
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

    #Horizontal rotation
    elif dir == 2 or dir == 3:
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


    #Perform the rotation

    #UP
    if dir == 0:
        if sides[curSide] == 'z':
            glRotate(mag, 1, 0, 0)
        if sides[curSide] == 'x':
            glRotate(mag, 0, 0, 1)
        if sides[curSide] == '-z':
            glRotate(-mag, 1, 0, 0)
        if sides[curSide] == '-x':
            glRotate(-mag, 0, 0, 1)

    #DOWN
    elif dir == 1:
        if sides[curSide] == 'z':
            glRotate(-mag, 1, 0, 0)
        if sides[curSide] == 'x':
            glRotate(-mag, 0, 0, 1)
        if sides[curSide] == '-z':
            glRotate(mag, 1, 0, 0)
        if sides[curSide] == '-x':
            glRotate(mag, 0, 0, 1)

    #LEFT
    elif dir == 2:
        glRotate(mag, 0, 1, 0)

    #RIGHT
    elif dir == 3:
        glRotate(-mag, 0, 1, 0)


#Return the axis currently pointing towards the camera
def getCurSide():
    global sides
    global curSide
    return sides[curSide]


def Update(deltaTime):
    global degRotatedH
    global degRotatedV
    global camDirH
    global camDirV
    global sides
    global curSide

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