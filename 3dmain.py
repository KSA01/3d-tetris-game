# 3dmain.py

import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
#from SlowCube import SlowCube
from SlowTriangle import SlowTriangle
import Cube
import Pieces
import Border
import GamePlay
import GameOver
import StartMenu
import UI

#Camera
import Camera
#Camera

#Need to install for UI
from freetype import *
import pygame.freetype

pygame.init()
size = width, height = 900, 750
screen = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width/height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

glTranslate(1.0, 0.0, -36.0)     #translates the camera
#glRotate(-15, 0, 1, 0)           #rotate -15 degrees around y
#glRotate(30, 1, 0, 0)            #rotate 30 degrees around x

# Game state: 'start_menu', 'playing', 'game_over'
game_state = 'start_menu'

_isPaused = False
_isGameOver = False

# Button bounds for menu interaction
start_button_bounds = None
play_again_bounds = None
quit_bounds = None

#UI
triangle = SlowTriangle()
#UI

tetrisPieces = Pieces.createTetrisPieces()
#print("NUM TETRIS PIECES: " + str(len(tetrisPieces)))

tetrisCubes = 0
for piece in tetrisPieces:
    tetrisCubes += len(piece.cubes)

#print("NUMBER OF CUBES: " + str(tetrisCubes))

def Update(deltaTime):

    global _isPaused #Access the global pause variable
    global game_state
    global _isGameOver

    # Handle mouse cursor changes - check if mouse is over any button
    # Note: button bounds are set in Render(), so we check them after rendering
    # This is handled in the Render() function to avoid frame delay

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        # Handle mouse clicks for menus
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouse_x, mouse_y = event.pos
            # Convert mouse coordinates (pygame uses top-left origin, OpenGL UI uses same)
            
            if game_state == 'start_menu':
                # Check if start button was clicked
                global start_button_bounds
                if start_button_bounds and StartMenu.ProcessClick(mouse_x, mouse_y, start_button_bounds):
                    try:
                        GamePlay.Init(tetrisPieces)
                        game_state = 'playing'
                        _isGameOver = False
                        _isPaused = False
                    except Exception as e:
                        print(f"Error initializing game: {e}")
                        import traceback
                        traceback.print_exc()
                        # Don't change game state if initialization fails
                        pass
            elif game_state == 'game_over':
                # Check if game over buttons were clicked
                global play_again_bounds, quit_bounds
                if play_again_bounds and quit_bounds:
                    result = GameOver.ProcessClick(mouse_x, mouse_y, play_again_bounds, quit_bounds)
                    if result == 'play_again':
                        try:
                            GamePlay.Reset(tetrisPieces)
                            game_state = 'playing'
                            _isGameOver = False
                            _isPaused = False
                        except Exception as e:
                            print(f"Error resetting game: {e}")
                            import traceback
                            traceback.print_exc()
                    elif result == 'quit':
                        return False
        
        if game_state == 'playing':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Check if ESC key is pressed
                _isPaused = not _isPaused #Toggle the pause state
                if _isPaused:
                    GamePlay.Pause() # Call a new function to handle pause in GamePlay
                else:
                    GamePlay.Resume() # Call a new function to handle resume in GamePlay
                continue
            if _isPaused:
                continue # Skip the rest of the loop if the game is paused

            if GamePlay.ProcessEvent(event):
                continue
    
    if game_state == 'playing':
        # Check if game is over
        if not Pieces.CheckForCeil():
            if not _isGameOver:
                _isGameOver = True
                game_state = 'game_over'
                GamePlay.Pause()
        else:
            GamePlay.Update(deltaTime, tetrisPieces)
            
            #Camera
            Camera.Update(deltaTime)

            #UI
            triangle.Update(deltaTime)
            #UI

    return True

def Render():
    global game_state
    global start_button_bounds, play_again_bounds, quit_bounds
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    if game_state == 'start_menu':
        # Render start menu
        start_button_bounds = StartMenu.Render()
        
        # Update cursor based on button hover
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if start_button_bounds and UI.is_point_in_button(mouse_x, mouse_y, start_button_bounds):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
    elif game_state == 'game_over':
        # Render the 3D game scene first (in background)
        Border.Render()
        GamePlay.Render()
        
        # Switch to 2D orthographic projection for UI
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Clear depth buffer and disable depth testing for UI overlay
        glClear(GL_DEPTH_BUFFER_BIT)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Render semi-transparent overlay to darken the background
        glDisable(GL_TEXTURE_2D)
        glColor4f(0.0, 0.0, 0.0, 0.6)  # Semi-transparent black overlay
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(width, 0)
        glVertex2f(width, height)
        glVertex2f(0, height)
        glEnd()
        
        # Render the game over menu on top (depth test already disabled)
        play_again_bounds, quit_bounds = GameOver.Render()
        
        # Update cursor based on button hover
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_over_button = False
        if play_again_bounds and quit_bounds:
            mouse_over_button = (UI.is_point_in_button(mouse_x, mouse_y, play_again_bounds) or 
                                UI.is_point_in_button(mouse_x, mouse_y, quit_bounds))
        if mouse_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        # Restore 3D projection
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
    elif game_state == 'playing':
        # Render the game
        #NEW
        #Render Border first so transparency works correctly
        Border.Render()

        GamePlay.Render()
        
        #UI TEST
        #triangle.Render()
        #UI
        
        # Reset cursor to arrow during gameplay
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    pygame.display.flip()

_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
while Update(_gDeltaTime):
    Render()
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTickLastFrame) / 1000.0
    _gTickLastFrame = t
