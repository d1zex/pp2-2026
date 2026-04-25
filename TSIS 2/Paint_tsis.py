import pygame
import sys
from pygame.locals import *
from datetime import datetime
from collections import deque

pygame.init()

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint Application")

canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont("Verdana", 20)

current_color = BLACK
brush_size = 5

drawing = False
shape_mode = None
start_pos = None
last_pos = None

text_mode = False
text_input = ""
text_pos = None


def draw_ui(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def flood_fill(surface, x, y, fill_color):
    target_color = surface.get_at((x, y))
    if target_color == fill_color:
        return

    q = deque()
    q.append((x, y))

    while q:
        x, y = q.popleft()

        if x < 0 or y < 0 or x >= SCREEN_WIDTH or y >= SCREEN_HEIGHT:
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), fill_color)

        q.append((x + 1, y))
        q.append((x - 1, y))
        q.append((x, y + 1))
        q.append((x, y - 1))


while True:
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Mouse down
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:

                if shape_mode == "fill":
                    flood_fill(canvas, event.pos[0], event.pos[1], current_color)

                elif text_mode:
                    text_pos = event.pos
                    text_input = ""

                else:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

        # Mouse up
        if event.type == MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos

                if shape_mode == "rectangle":
                    rect = pygame.Rect(
                        min(start_pos[0], end_pos[0]),
                        min(start_pos[1], end_pos[1]),
                        abs(start_pos[0] - end_pos[0]),
                        abs(start_pos[1] - end_pos[1]),
                    )
                    pygame.draw.rect(canvas, current_color, rect, brush_size)

                elif shape_mode == "circle":
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 +
                                  (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)

                elif shape_mode == "square":
                    side = min(abs(start_pos[0] - end_pos[0]),
                               abs(start_pos[1] - end_pos[1]))
                    pygame.draw.rect(canvas, current_color,
                                     (start_pos[0], start_pos[1], side, side), brush_size)

                elif shape_mode == "right_triangle":
                    pygame.draw.polygon(canvas, current_color,
                                        [start_pos,
                                         (start_pos[0], end_pos[1]),
                                         end_pos], brush_size)

                elif shape_mode == "equilateral_triangle":
                    height = abs(start_pos[1] - end_pos[1])
                    base_half = height / 1.732
                    pygame.draw.polygon(canvas, current_color,
                                        [(start_pos[0] - base_half, end_pos[1]),
                                         (start_pos[0] + base_half, end_pos[1]),
                                         start_pos], brush_size)

                elif shape_mode == "rhombus":
                    width = abs(start_pos[0] - end_pos[0])
                    height = abs(start_pos[1] - end_pos[1])
                    pygame.draw.polygon(canvas, current_color,
                                        [(start_pos[0], start_pos[1] - height // 2),
                                         (start_pos[0] + width // 2, start_pos[1]),
                                         (start_pos[0], start_pos[1] + height // 2),
                                         (start_pos[0] - width // 2, start_pos[1])],
                                        brush_size)

                elif shape_mode == "line":
                    pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)

                drawing = False
                shape_mode = None
                start_pos = None

        # Keyboard
        if event.type == KEYDOWN:

            # Clear
            if event.key == K_c:
                canvas.fill(WHITE)

            # Brush sizes
            elif event.key == K_1:
                brush_size = 2
            elif event.key == K_2:
                brush_size = 5
            elif event.key == K_3:
                brush_size = 10

            # Colors
            elif event.key == K_q:
                current_color = BLACK
            elif event.key == K_w:
                current_color = RED
            elif event.key == K_e:
                current_color = GREEN
            elif event.key == K_r:
                current_color = BLUE
            elif event.key == K_t:
                current_color = YELLOW

            # Shapes
            elif event.key == K_a:
                shape_mode = "rectangle"
            elif event.key == K_s:
                shape_mode = "circle"
            elif event.key == K_d:
                shape_mode = "square"
            elif event.key == K_f:
                shape_mode = "right_triangle"
            elif event.key == K_g:
                shape_mode = "equilateral_triangle"
            elif event.key == K_h:
                shape_mode = "rhombus"
            elif event.key == K_l:
                shape_mode = "line"
            elif event.key == K_z:
                shape_mode = "fill"

            # Text mode
            elif event.key == K_x:
                text_mode = True

            # Save
            if event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, filename)

            # Text input handling
            if text_mode:
                if event.key == K_RETURN:
                    txt = font.render(text_input, True, current_color)
                    canvas.blit(txt, text_pos)
                    text_mode = False

                elif event.key == K_ESCAPE:
                    text_mode = False

                elif event.key == K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

    # Freehand drawing (pencil)
    if drawing and shape_mode is None:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(canvas, current_color, last_pos, mouse_pos, brush_size)
        last_pos = mouse_pos

    # Line preview
    if drawing and shape_mode == "line":
        pygame.draw.line(screen, current_color, start_pos,
                         pygame.mouse.get_pos(), brush_size)

    # Text preview
    if text_mode and text_pos:
        preview = font.render(text_input, True, current_color)
        screen.blit(preview, text_pos)

    # UI
    draw_ui("Brush: 1-2-3 | Colors: Q W E R T | Shapes A-S-D-F-G-H | L Line | Z Fill | X Text | Ctrl+S Save | C Clear", 10, 10)

    pygame.display.update()