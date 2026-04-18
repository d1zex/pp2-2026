import pygame
import os

pygame.init()

WIDTH, HEIGHT = 500, 300
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player")

music_files = [file for file in os.listdir() if file.endswith('.mp3')]
current_track_index = 0

# Track state
is_paused = False

def play_music():
    global is_paused
    if music_files:
        pygame.mixer.music.load(music_files[current_track_index])
        pygame.mixer.music.play()
        is_paused = False

def stop_music():
    pygame.mixer.music.stop()

def pause_music():
    global is_paused
    pygame.mixer.music.pause()
    is_paused = True

def unpause_music():
    global is_paused
    pygame.mixer.music.unpause()
    is_paused = False

def next_track():
    global current_track_index
    if music_files:
        current_track_index = (current_track_index + 1) % len(music_files)
        play_music()

def previous_track():
    global current_track_index
    if music_files:
        current_track_index = (current_track_index - 1) % len(music_files)
        play_music()

running = True
clock = pygame.time.Clock()

play_music()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy() and not is_paused:
                    pause_music()
                else:
                    unpause_music()

            elif event.key == pygame.K_RIGHT:
                next_track()

            elif event.key == pygame.K_LEFT:
                previous_track()

    screen.fill((200, 200, 200))

    if music_files:
        font = pygame.font.Font(None, 36)
        status = "Paused" if is_paused else "Playing"
        text = font.render(f"{status}: {music_files[current_track_index]}", True, (0, 0, 0))
        screen.blit(text, (20, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()