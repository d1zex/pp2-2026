import pygame
import time
import math

pygame.init()

WIDTH, HEIGHT = 400, 400
CENTER = (WIDTH // 2, HEIGHT // 2)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock_image = pygame.image.load('mickeyclock.jpeg')
clock_image = pygame.transform.scale(clock_image, (WIDTH, HEIGHT))

def draw_hand(angle_deg, length, color, thickness):
    angle_rad = math.radians(angle_deg - 90)

    x = CENTER[0] + length * math.cos(angle_rad)
    y = CENTER[1] + length * math.sin(angle_rad)

    pygame.draw.line(screen, color, CENTER, (x, y), thickness)

def draw_clock(hour_angle, minute_angle, second_angle):
    screen.blit(clock_image, (0, 0))

    # hourses
    draw_hand(hour_angle, 40, (0, 255, 255), 8)

    # minutes
    draw_hand(minute_angle, 60, (128, 255, 0), 6)

    # seconds
    draw_hand(second_angle, 90, (255, 0, 0), 3)

    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        t = time.localtime()

        hours = t.tm_hour % 12
        minutes = t.tm_min
        seconds = t.tm_sec

        hour_angle = (hours * 30) + (minutes * 0.5)
        minute_angle = (minutes * 6) + (seconds * 0.1)
        second_angle = seconds * 6

        draw_clock(hour_angle, minute_angle, second_angle)

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()