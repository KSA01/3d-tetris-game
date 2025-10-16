# Pieces.py

from OpenGL.GL import *
import numpy as np
import math
from Cube import *
from Texture import Texture
import Camera

#[r,g,b,a]
colors = (
        [0,1,1,1], # Cyan 0
        [0,0,1,1], # Blue 1
        [1,0.5,0,1], # Orange 2
        [1,1,0,1], # Yellow 3
        [0,1,0,1], # Green 4
        [1,0,1,1], # Purple 5
        [1,0,0,1] # Red 6
)

filepaths = (
    "Textures/blueberryI.png",
    "Textures/blackberriesJ.png",
    "Textures/orangeL.png",
    "Textures/bananaO.png",
    "Textures/pearZ.png",
    "Textures/grapesT.png",
    "Textures/strawberryS.png"
)

borders = (
    (-6, 6),
    (-5, 30),
    (-6, 6)
)

pieceNames = ["I", "J", "L", "O", "S", "T", "Z"]  # List of pieces by name
cubeCount = 4 # Amount of cubes per piece

tetrisPieces = []

CubeList = []

# A function to create Tetris pieces
def createTetrisPieces():

    for i in range(len(pieceNames)):
        piece = Piece(position=(0, 18, 0), color=colors[i], name=pieceNames[i], filepath=filepaths[i]) 
        tetrisPieces.append(piece)

    return tetrisPieces

def checkCubeCol(piece):
    # Collect position of all cubes in the piece
    for cube in piece.cubes:
        locPos = np.round(cube.GetCubePos()) + np.round(piece.GetPos())
        
        # Check if any cube in CubeList is within a distance of 2 in all three axes
        if any(all(np.abs(locPos - np.round(pos.GetCubePos())) < 2) for pos in CubeList):
            #print("Overlaps")
            return False  # overlaps

    return True # no overlaps

def freezeCubes(cube):
    CubeList.append(cube)

# function for ending the game once the player has lost
def CheckForCeil():
    if CubeList:
        for cube in CubeList:
            if np.rint(cube.GetCubePos()[1]) >= 8:
                return False
    
    return True

#Alfredo
#checks if bottom row is filled
def CheckForPoint():
    count = 0   # counter for cubes at bottom
    for cube in CubeList:
        if cube.GetCubePos()[1] <= -4.9:  # bottom y coord is -5
            count += 1
    if count >= 36:  # if there are this many cubes at bottom (6x6 layer)
        count = 0
        return False

    return True
#Alfredo

# Check and clear any fully-filled horizontal layers (across X-Z) at any Y inside the border
def ClearFullLayers():
    if not CubeList:
        return 0

    # Compute how many cells constitute a full layer based on borders and 2-unit grid spacing
    cells_per_x = int((borders[0][1] - borders[0][0]) // 2)
    cells_per_z = int((borders[2][1] - borders[2][0]) // 2)
    full_layer_size = cells_per_x * cells_per_z

    # Map each Y level to set of occupied (x, z) grid positions
    layer_to_positions = {}

    x_min, x_max = borders[0]
    z_min, z_max = borders[2]

    for cube in CubeList:
        pos = np.rint(cube.GetCubePos())
        y = int(pos[1])
        x = int(pos[0])
        z = int(pos[2])

        # Consider only cells within the inner play area
        if x <= x_min or x >= x_max or z <= z_min or z >= z_max:
            continue

        if y not in layer_to_positions:
            layer_to_positions[y] = set()
        layer_to_positions[y].add((x, z))

    # Identify any full layers
    full_layers = sorted([y for y, positions in layer_to_positions.items() if len(positions) >= full_layer_size])

    if not full_layers:
        return 0

    # Remove cubes that are in full layers
    remaining_cubes = []
    full_layers_set = set(full_layers)
    for cube in CubeList:
        y = int(np.rint(cube.GetCubePos()[1]))
        if y in full_layers_set:
            continue
        remaining_cubes.append(cube)

    # Drop remaining cubes by 2 units for each cleared layer below their Y
    for cube in remaining_cubes:
        y = int(np.rint(cube.GetCubePos()[1]))
        drop_layers_below = sum(1 for layer in full_layers if y > layer)
        if drop_layers_below > 0:
            cube.SetCubePos(cube.GetCubePos() + np.asarray([0, -2 * drop_layers_below, 0], dtype=np.float32))

    CubeList[:] = remaining_cubes

    return len(full_layers)

# Fallback: handle bottom row clearing with tolerant thresholding
def ClearBottomRowFallback():
    if not CubeList:
        return 0

    # Compute full layer size from borders
    cells_per_x = int((borders[0][1] - borders[0][0]) // 2)
    cells_per_z = int((borders[2][1] - borders[2][0]) // 2)
    full_layer_size = cells_per_x * cells_per_z

    bottom_y_threshold = -4.9  # Treat anything at/just below -5 as bottom

    bottom_cubes = [cube for cube in CubeList if cube.GetCubePos()[1] <= bottom_y_threshold]
    if len(bottom_cubes) < full_layer_size:
        return 0

    # Remove bottom cubes
    survivors = [cube for cube in CubeList if cube.GetCubePos()[1] > bottom_y_threshold]

    # Move survivors down by 2
    for cube in survivors:
        cube.MoveCubeDown()

    CubeList[:] = survivors
    return 1

# Clear any fully filled rows inside the border at any Y (both X-rows and Z-rows)
def ClearFullRows():
    if not CubeList:
        return 0

    # Determine grid dimensions (number of cells per axis)
    cells_per_x = int((borders[0][1] - borders[0][0]) // 2)
    cells_per_z = int((borders[2][1] - borders[2][0]) // 2)

    x_min, x_max = borders[0]
    z_min, z_max = borders[2]

    # Build occupancy maps
    # For rows along X (fixed y and z, varying x)
    occ_rows_x = {}
    # For rows along Z (fixed y and x, varying z)
    occ_rows_z = {}

    for cube in CubeList:
        pos = np.rint(cube.GetCubePos())
        y = int(pos[1])
        x = int(pos[0])
        z = int(pos[2])

        # Only consider cells strictly inside in X/Z
        if x <= x_min or x >= x_max or z <= z_min or z >= z_max:
            continue

        key_x = (y, z)
        key_z = (y, x)
        occ_rows_x.setdefault(key_x, set()).add(x)
        occ_rows_z.setdefault(key_z, set()).add(z)

    # Identify full rows
    full_rows_x = [key for key, xs in occ_rows_x.items() if len(xs) >= cells_per_x]
    full_rows_z = [key for key, zs in occ_rows_z.items() if len(zs) >= cells_per_z]
    if not full_rows_x and not full_rows_z:
        return 0

    # Compute which cubes to remove
    rows_x_set = set(full_rows_x)
    rows_z_set = set(full_rows_z)

    survivors = []
    removed_count = 0
    for cube in CubeList:
        pos = np.rint(cube.GetCubePos())
        y = int(pos[1])
        x = int(pos[0])
        z = int(pos[2])

        remove = ((y, z) in rows_x_set) or ((y, x) in rows_z_set)
        if remove:
            removed_count += 1
        else:
            survivors.append(cube)

    # Drop survivors by number of distinct Y levels cleared below them
    cleared_y_levels = sorted(set([y for (y, _) in full_rows_x] + [y for (y, _) in full_rows_z]))
    for cube in survivors:
        y = int(np.rint(cube.GetCubePos()[1]))
        drop_levels_below = sum(1 for lvl in cleared_y_levels if y > lvl)
        if drop_levels_below > 0:
            cube.SetCubePos(cube.GetCubePos() + np.asarray([0, -2 * drop_levels_below, 0], dtype=np.float32))

    CubeList[:] = survivors

    # Return number of individual rows cleared (not just levels)
    return len(full_rows_x) + len(full_rows_z)

class Piece:
    def __init__(self, position, color, name, filepath):
        #Smooth rotations
        #Tracks which direction the piece is currently rotating (left, right, down)
        self.rotateDir = None
        #Tracks how many degrees have been rotated in current rotation
        self.radRotated = math.radians(0)

        #Relative rotations
        #The axis to rotate the pieces on (horizontal by default, changes when rotation is toggled)
        self.rotateAxis = (0, -2, 0)

        self.name = name
        if self.name == "I":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (0, 2, 0), (0, 4, 0)]
        elif self.name == "J":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (0, 2, 0), (-2, 2, 0)]
        elif self.name == "L":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (-2, -2, 0), (0, 2, 0)]
        elif self.name == "O":
            self.localPositions = [(0, 0, 0), (-2, -2, 0), (0, -2, 0), (-2, 0, 0)]
        elif self.name == "S":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (-2, -2, 0), (2, 0, 0)]
        elif self.name == "T":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (-2, 0, 0), (2, 0, 0)]
        elif self.name == "Z":
            self.localPositions = [(0, 0, 0), (0, -2, 0), (2, -2, 0), (-2, 0, 0)]


        self.filepath = filepath


        self.cubes = [Cube(localPos, color, self.filepath) for localPos in self.localPositions]
        self.position = position        #takes position of each piece
        self.lastPosition = self.position #sets last position
        self.ang = 0
        self.axis = (3,1,1)             
        self.color = np.asarray(color, dtype=np.float32)  #takes a different color for each piece

        self.transforms = [np.eye(4) for _ in range(cubeCount)]

        #Set cubes within piece to be fully transparent on init
        for cube in self.cubes:
            cube.color[3] = 0

        #Toggle cubes to appear
        self.ToggleCubes(True, False)

    def GetPos(self):
        return self.position

    def SetPos(self, position):
        self.position = position

    # Reset Cube Orientation for in gameplay
    def ResetCubePos(self):
        for i, cube in enumerate(self.cubes):
            #reset each localPos
            cube.SetCubePos(self.localPositions[i])

    # Revert Cube Positions for rotation function
    def RevertCubePos(self, lastPos):
        for i, cube in enumerate(self.cubes):
            #revert each localPos
            cube.SetCubePos(lastPos[i])

    #Change the value of appearing and disappearing for all cubes within piece (pass in a boolean for appear and disappear)
    def ToggleCubes(self, appear, disappear):
        for cube in self.cubes:
            cube.appearing = appear
            cube.disappearing = disappear


    #Smooth Rotations
    #Takes a direction (left, right, down) and toggles the piece to rotate that way over 1/6s
    def ToggleRotate(self, dir):
        #If the piece is not currently rotating, toggle it to rotate in the given direction
        if self.rotateDir == None:
            self.rotateDir = dir

            #Reset rads rotated counter (for new rotation)
            self.radRotated = 0

            #Check axis facing the camera (for relative piece rotations)
            curSide = Camera.getCurSide()
            
            #If rotating left or right, rotate around y axis
            if self.rotateDir == "left":
                self.rotateAxis = (0, -2, 0)
            elif self.rotateDir == "right":
                self.rotateAxis = (0, 2, 0)
            #If rotating down, rotate around x or z axis
            elif self.rotateDir == "down":
                if curSide == 'z':
                    self.rotateAxis = (-2, 0, 0)
                elif curSide == '-z':
                    self.rotateAxis = (2, 0, 0)
                elif curSide == 'x':
                    self.rotateAxis = (0, 0, -2)
                elif curSide == '-x':
                    self.rotateAxis = (0, 0, 2)


    def RotateSmooth(self, deltaTime):
        # defines cur/prev pos in case to revert
        curLocalPositions = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        for i, cube in enumerate(self.cubes):
            curPos = cube.GetCubePos()
            curLocalPositions[i] = np.rint(curPos)

        #Tracks the rotation direction for this frame (for edge case)
        #This is needed in case rotation gets cancelled on the last frame of rotation (and self.rotateDir is None when reverting rotation)
        rotateDirThisFrame = self.rotateDir

        #Tracks if the rotation has failed
        failed = False

        center = np.asarray(self.cubes[0].localPos, dtype=np.float32)

        #The magnitude of the angle of rotation (in radians)
        mag = math.radians(90 * 6 * deltaTime)

        if self.rotateDir == "left":
            #If the rotation is almost complete, rotate the rest of the way
            if (self.radRotated + mag) >= math.radians(90):
                mag = math.radians(90) - self.radRotated
                #Reset rotation counter and rotation status
                #self.radRotated = math.radians(0)
                self.rotateDir = None
            else:
                #self.radRotated += mag
                pass

            self.radRotated += mag

            angle = mag
            axis = self.rotateAxis

        elif self.rotateDir == "right":
            #If the rotation is almost complete, rotate the rest of the way
            if (self.radRotated + mag) >= math.radians(90):
                mag = math.radians(90) - self.radRotated
                #Reset rotation counter and rotation status
                #self.radRotated = math.radians(0)
                self.rotateDir = None
            else:
                #self.radRotated += mag
                pass

            self.radRotated += mag

            angle = mag
            axis = self.rotateAxis

        elif self.rotateDir == "down":
            #If the rotation is almost complete, rotate the rest of the way
            if (self.radRotated + mag) >= math.radians(90):
                mag = math.radians(90) - self.radRotated
                #Reset rotation counter and rotation status
                #self.radRotated = math.radians(0)
                self.rotateDir = None
            else:
                #self.radRotated += mag
                pass

            self.radRotated += mag

            angle = -mag
            axis = self.rotateAxis

        rotation_matrix = axis_rotation_matrix(angle, axis)

        #Perform the rotation
        for cube in self.cubes:
            cube.localPos = np.dot(cube.localPos - center, rotation_matrix) + center
            
            # checks if in bounds or colliding and if so reverts cube positions 
            if not self.CheckInBounds() or not checkCubeCol(self):
                #print("collision detected, reverting rotation")
                failed = True


        if failed:
                #print("collision detected, reverting rotation")

                #self.RevertCubePos(curLocalPositions)

                #Revert piece back to its original orientation by reversing the current rotation
                if rotateDirThisFrame == "down":
                    self.Rotate(self.radRotated, self.rotateAxis)
                else:
                    #print("reverting horiz rotation")
                    self.Rotate(self.radRotated, (self.rotateAxis[0], -self.rotateAxis[1], self.rotateAxis[2]))

                #Toggle the piece to stop rotating
                self.rotateDir = None


    #Smooth Rotations


    # Rotates a piece in one frame
    def Rotate(self, angle, axis):
        curLocalPositions = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        for i, cube in enumerate(self.cubes):
            curPos = cube.GetCubePos()
            curLocalPositions[i] = curPos

        # Convert angle to radians
        angle = math.radians(angle)
        center = np.asarray(self.cubes[0].localPos, dtype=np.float32)
        rotation_matrix = axis_rotation_matrix(angle, axis)

        # checks if cubes are in bounds before completing rotation
        for cube in self.cubes:
            cube.localPos = np.rint(np.dot(cube.localPos - center, rotation_matrix)) + center
            if not self.CheckInBounds() or not checkCubeCol(self):
                self.RevertCubePos(curLocalPositions)
                break

    # Check if all cubes of a piece are in bounds
    def CheckInBounds(self):
        for cube in self.cubes:
            for i in range(3): # for each axis (x,y,z)
                pos = cube.GetCubePos() + np.rint(self.position)
                # checks if each axis value is between border limits for that axis
                if pos[i] <= borders[i][0] or pos[i] >= borders[i][1]:
                    return False  # Cube is out of bounds for at least one dimension

        return True  # All cubes are within bounds for all dimensions

    #NOTE: Fading in/out can no longer be paused (because this update is no longer locked behind pause status)
    def Update(self, deltaTime, move, paused): #Takes pause status to gatekeep all update actions except ongoing fade and rotate
        #If the game is paused, don't update position
        if not paused:
            self.ang += 50.0 * deltaTime
            self.position += move

            if not self.CheckInBounds():
                self.position[0] = self.lastPosition[0]
                self.position[2] = self.lastPosition[2]
                
            # Save last position
            self.lastPosition = np.copy(self.position)

        #TEST: Update Cubes within piece regardless of pause status
        for cube in self.cubes:
            cube.Update(deltaTime)

        #Smooth Rotations
        if self.rotateDir != None:
            self.RotateSmooth(deltaTime)

    def Render(self):
        #m = glGetDouble(GL_MODELVIEW_MATRIX)
        #center = self.cubes[0].localPos

        glPushMatrix()
        glTranslatef(*self.position)
        #glRotatef(self.ang, *center)
        for cube in self.cubes:
            cube.Render()
        glPopMatrix()
        
        #glLoadMatrixf(m)

# quaternians rotation matrix 
def axis_rotation_matrix(angle, axis):
    axis = np.asarray(axis)
    axis = axis / np.sqrt(np.dot(axis, axis))
    q = np.array([np.cos(angle / 2.0), *(-axis * np.sin(angle / 2.0))])
    rotation_matrix = np.array([
        [1 - 2 * (q[2]**2 + q[3]**2), 2 * (q[1] * q[2] - q[0] * q[3]), 2 * (q[1] * q[3] + q[0] * q[2])],
        [2 * (q[1] * q[2] + q[0] * q[3]), 1 - 2 * (q[1]**2 + q[3]**2), 2 * (q[2] * q[3] - q[0] * q[1])],
        [2 * (q[1] * q[3] - q[0] * q[2]), 2 * (q[2] * q[3] + q[0] * q[1]), 1 - 2 * (q[1]**2 + q[2]**2)],
    ])
    return rotation_matrix
