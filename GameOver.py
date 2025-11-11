#GameOver.py

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import UI

def Render(screen_width=900, screen_height=750):
    """
    Render the game over menu with dynamic screen size support.
    All UI elements are positioned relative to screen dimensions.
    """
    # Setting up orthographic projection for text rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, screen_width, screen_height, 0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Disable depth testing for UI elements to ensure they render on top
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Render the game over text (centered)
    game_over_text = "GAME OVER"
    game_over_font_size = 48
    game_over_width, _ = UI.get_text_size(game_over_text, game_over_font_size)
    game_over_x = (screen_width - game_over_width) // 2
    UI.render_text_color(game_over_text, game_over_x, 250, game_over_font_size, (1.0, 0.0, 0.0))
    
    # Render play again button - fixed width, centered
    play_again_text = "PLAY AGAIN"
    play_again_font_size = 28
    play_again_text_width, _ = UI.get_text_size(play_again_text, play_again_font_size)
    play_again_width = max(play_again_text_width + 40, 260)  # Fixed width based on text
    play_again_height = 60
    play_again_x = (screen_width - play_again_width) // 2  # Centered
    play_again_y = screen_height // 2 + 50
    play_again_bounds = UI.render_button(play_again_x, play_again_y, play_again_width, play_again_height, play_again_text, play_again_font_size, False)
    
    # Render quit button - fixed width, centered
    quit_text = "QUIT"
    quit_font_size = 28
    quit_text_width, _ = UI.get_text_size(quit_text, quit_font_size)
    quit_width = max(quit_text_width + 40, 200)  # Fixed width based on text
    quit_height = 60
    quit_x = (screen_width - quit_width) // 2  # Centered
    quit_y = screen_height // 2 + 130
    quit_bounds = UI.render_button(quit_x, quit_y, quit_width, quit_height, quit_text, quit_font_size, False)

    # Re-enable depth test
    glEnable(GL_DEPTH_TEST)

    # Restore the previous projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    return play_again_bounds, quit_bounds

def ProcessClick(mouse_x, mouse_y, play_again_bounds, quit_bounds):
    """ Check which button was clicked. Returns 'play_again', 'quit', or None """
    if UI.is_point_in_button(mouse_x, mouse_y, play_again_bounds):
        return 'play_again'
    elif UI.is_point_in_button(mouse_x, mouse_y, quit_bounds):
        return 'quit'
    return None