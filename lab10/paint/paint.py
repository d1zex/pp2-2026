import pygame
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up the display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint Application")
DISPLAYSURF.fill(WHITE)

# Brush settings
current_color = BLACK
brush_size = 5
drawing = False
shape_mode = None  # 'circle', 'rectangle', 'eraser', or None
start_pos = None  # Start position for drawing shapes

# Fonts
font = pygame.font.SysFont("Verdana", 20)

def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    DISPLAYSURF.blit(text_surface, (x, y))

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Mouse button pressed
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                drawing = True
                start_pos = event.pos  # Capture starting position for shapes

        # Mouse button released
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                if shape_mode == 'rectangle' and start_pos:
                    end_pos = pygame.mouse.get_pos()
                    rect = pygame.Rect(min(start_pos[0], end_pos[0]),
                                       min(start_pos[1], end_pos[1]),
                                       abs(start_pos[0] - end_pos[0]),
                                       abs(start_pos[1] - end_pos[1]))
                    pygame.draw.rect(DISPLAYSURF, current_color, rect, 2)
                elif shape_mode == 'circle' and start_pos:
                    end_pos = pygame.mouse.get_pos()
                    radius = int(((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)**0.5)
                    pygame.draw.circle(DISPLAYSURF, current_color, start_pos, radius, 2)
                drawing = False
                shape_mode = None
                start_pos = None

        # Handle keypress events
        if event.type == KEYDOWN:
            if event.key == K_c:  # Clear screen
                DISPLAYSURF.fill(WHITE)
            elif event.key == K_1:  # Set color to black
                current_color = BLACK
            elif event.key == K_2:  # Set color to red
                current_color = RED
            elif event.key == K_3:  # Set color to green
                current_color = GREEN
            elif event.key == K_4:  # Set color to blue
                current_color = BLUE
            elif event.key == K_5:  # Set color to yellow
                current_color = YELLOW
            elif event.key == K_UP:  # Increase brush size
                brush_size += 2
            elif event.key == K_DOWN:  # Decrease brush size
                brush_size = max(1, brush_size - 2)
            elif event.key == K_r:  # Rectangle mode
                shape_mode = 'rectangle'
            elif event.key == K_o:  # Circle mode
                shape_mode = 'circle'
            elif event.key == K_e:  # Eraser mode
                shape_mode = 'eraser'

    # If drawing in freehand mode
    if drawing and shape_mode is None:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(DISPLAYSURF, current_color, mouse_pos, brush_size)

    # If eraser mode is active
    if drawing and shape_mode == 'eraser':
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(DISPLAYSURF, WHITE, mouse_pos, brush_size)

    # Draw UI text
    draw_text("C: Clear | 1-Black 2-Red 3-Green 4-Blue 5-Yellow | R: Rectangle O: Circle E: Eraser | Brush: UP/DOWN", 10, 10)

    pygame.display.update()
