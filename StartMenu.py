# StartMenu.py

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import UI

# screen size
width, height = 900, 750

def Render():
    # Setting up orthographic projection for text rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, height, 0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Disable depth testing for UI elements
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Render title (centered)
    title_text = "3D TETRIS"
    title_font_size = 48
    title_width, title_height = UI.get_text_size(title_text, title_font_size)
    title_x = (width - title_width) // 2
    UI.render_text_color(title_text, title_x, 80, title_font_size, (1.0, 1.0, 0.0))
    
    # Render rules on the left side
    left_x = 50
    header_font_size = 22  # Smaller header font
    UI.render_text_color("HOW TO PLAY", left_x, 180, header_font_size, (1.0, 1.0, 0.0))
    UI.render_text_color("Arrow Keys: Move", left_x, 220, 18, (1.0, 1.0, 1.0))
    UI.render_text_color("A: Rotate Left", left_x, 250, 18, (1.0, 1.0, 1.0))
    UI.render_text_color("D: Rotate Right", left_x, 280, 18, (1.0, 1.0, 1.0))
    UI.render_text_color("S: Rotate Down", left_x, 310, 18, (1.0, 1.0, 1.0))
    UI.render_text_color("Enter: Fast Drop", left_x, 340, 18, (1.0, 1.0, 1.0))
    UI.render_text_color("I/J/K/L: Camera", left_x, 370, 18, (1.0, 1.0, 1.0))
    UI.render_text_color("ESC: Pause", left_x, 400, 18, (1.0, 1.0, 1.0))
    
    # Render rules on the right side (make sure text fits on screen)
    right_header_text = "OBJECTIVE"
    header_font_size = 22
    
    # Calculate the longest text line to ensure everything fits
    right_text_lines = [
        ("OBJECTIVE", header_font_size),  # Include header in width calculation
        ("Fill rows or layers", 18),
        ("to clear them!", 18),
        ("Score = blocks", 18),
        ("cleared", 18),
        ("Don't let pieces", 18),
        ("reach the top!", 18)
    ]
    max_text_width = 0
    for line, font_size in right_text_lines:
        text_width, _ = UI.get_text_size(line, font_size)
        max_text_width = max(max_text_width, text_width)
    
    # Position text from the right with padding, ensuring it fits
    # Use at least 60 pixels padding to be safe
    right_x = width - max_text_width - 60  # 60 pixels padding from right edge
    UI.render_text_color(right_header_text, right_x, 180, header_font_size, (1.0, 1.0, 0.0))
    UI.render_text_color("Fill rows or layers", right_x, 220, 18, (1.0, 1.0, 1.0))
    UI.render_text_color("to clear them!", right_x, 250, 18, (1.0, 1.0, 1.0))
    UI.render_text_color("Score = blocks", right_x, 290, 18, (1.0, 1.0, 1.0))
    UI.render_text_color("cleared", right_x, 320, 18, (1.0, 1.0, 1.0))
    UI.render_text_color("Don't let pieces", right_x, 360, 18, (1.0, 1.0, 1.0))
    UI.render_text_color("reach the top!", right_x, 390, 18, (1.0, 1.0, 1.0))
    
    # Render start button in the center - make sure it's wide enough
    start_text = "START"
    start_font_size = 32
    start_text_width, _ = UI.get_text_size(start_text, start_font_size)
    button_width = max(start_text_width + 40, 200)  # Add padding, minimum 200
    button_height = 60
    button_x = (width - button_width) // 2
    button_y = height // 2 + 80
    button_bounds = UI.render_button(button_x, button_y, button_width, button_height, start_text, start_font_size, False)
    
    # Re-enable depth test
    glEnable(GL_DEPTH_TEST)

    # Restore the previous projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    return button_bounds

def ProcessClick(mouse_x, mouse_y, button_bounds):
    """ Check if the start button was clicked """
    return UI.is_point_in_button(mouse_x, mouse_y, button_bounds)

