import pygame
import sys
import random
import json

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer TSIS 3")
clock = pygame.time.Clock()
FPS = 60

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# ---------------- GAME VARIABLES ----------------
speed = 3
game_speed = 3
score = 0
coins_collected = 0
distance = 0

game_state = "MENU"
username = "Player"

# ---------------- FONTS ----------------
font = pygame.font.SysFont("Verdana", 40)
small_font = pygame.font.SysFont("Verdana", 20)

# ---------------- BACKGROUND ----------------
bg = pygame.image.load("AnimatedStreet.png")

# ---------------- LEADERBOARD ----------------
leaderboard_file = "leaderboard.json"

def load_scores():
    try:
        with open(leaderboard_file, "r") as f:
            return json.load(f)
    except:
        return []

def save_score(name, score, distance):
    data = load_scores()
    data.append({"name": name, "score": score, "distance": distance})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    with open(leaderboard_file, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- PLAYER ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("Player.png")
        self.image = pygame.transform.scale(img, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 80)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(5, 0)

# ---------------- ENEMY ----------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("traffic.png")
        self.image = pygame.transform.scale(img, (90, 100))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.choice([80,160,240,320]), -100)

    def update(self):
        global score
        self.rect.move_ip(0, game_speed)

        if self.rect.top > HEIGHT:
            score += 1
            self.reset()

# ---------------- COIN ----------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("Coin.png")
        self.image = pygame.transform.scale(img, (22, 22))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.choice([80,160,240,320]), -200)

    def update(self):
        self.rect.move_ip(0, game_speed)
        if self.rect.top > HEIGHT:
            self.reset()

# ---------------- POWERUPS ----------------
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind

        try:
            img = pygame.image.load(f"{kind}.png")
            self.image = pygame.transform.scale(img, (40, 40))
        except:
            self.image = pygame.Surface((30, 30))
            self.image.fill((150, 150, 150))

        self.rect = self.image.get_rect()
        self.rect.center = (random.choice([80,160,240,320]), -50)

    def update(self):
        self.rect.move_ip(0, game_speed)
        if self.rect.top > HEIGHT:
            self.kill()

# ---------------- OBJECTS ----------------
player = Player()
enemy = Enemy()
coin = Coin()

powerups = pygame.sprite.Group()

# ---------------- POWER STATES ----------------
active_power = None
power_timer = 0
shield = False

# ---------------- RESET FUNCTION (IMPORTANT FIX) ----------------
def reset_game():
    global score, coins_collected, distance, speed
    global game_speed, active_power, shield

    score = 0
    coins_collected = 0
    distance = 0
    speed = 3
    game_speed = 3

    active_power = None
    shield = False

    player.rect.center = (WIDTH // 2, HEIGHT - 80)
    enemy.reset()
    coin.reset()

    powerups.empty()

# ---------------- SPAWN TIMER ----------------
POWER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(POWER_EVENT, 2000)

# ---------------- GAME LOOP ----------------
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == POWER_EVENT:
            if len(powerups) < 2:
                kind = random.choice(["shield", "nitro", "repair"])
                p = PowerUp(kind)
                powerups.add(p)

    # ---------------- MENU ----------------
    if game_state == "MENU":
        screen.fill(WHITE)

        title = font.render("RACER GAME", True, BLACK)
        screen.blit(title, (70, 200))

        hint = small_font.render("Press ENTER to start", True, BLACK)
        screen.blit(hint, (90, 300))

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            game_state = "PLAYING"

    # ---------------- GAME ----------------
    elif game_state == "PLAYING":
        screen.blit(bg, (0, 0))

        distance += game_speed * 0.1

        if active_power == "nitro":
            game_speed = speed * 2
            if pygame.time.get_ticks() - power_timer > 4000:
                active_power = None
        else:
            game_speed = speed

        player.update()
        enemy.update()
        coin.update()
        powerups.update()

        # ---------------- COLLISIONS ----------------
        if pygame.sprite.collide_rect(player, enemy):
            if shield:
                shield = False
                enemy.reset()
            else:
                save_score(username, score, int(distance))
                game_state = "GAME_OVER"

        if pygame.sprite.collide_rect(player, coin):
            coins_collected += 1
            score += 1
            coin.reset()

        for p in powerups:
            if player.rect.colliderect(p.rect):
                if p.kind == "shield":
                    shield = True
                elif p.kind == "nitro":
                    active_power = "nitro"
                    power_timer = pygame.time.get_ticks()
                elif p.kind == "repair":
                    score += 5
                    speed = max(2, speed - 1)
                p.kill()

        # ---------------- DRAW ----------------
        screen.blit(player.image, player.rect)
        screen.blit(enemy.image, enemy.rect)
        screen.blit(coin.image, coin.rect)

        for p in powerups:
            screen.blit(p.image, p.rect)

        screen.blit(small_font.render(f"Score: {score}", True, BLACK), (10, 10))
        screen.blit(small_font.render(f"Coins: {coins_collected}", True, BLACK), (10, 35))
        screen.blit(small_font.render(f"Dist: {int(distance)}", True, BLACK), (10, 60))

    # ---------------- GAME OVER ----------------
    elif game_state == "GAME_OVER":
        screen.fill(RED)

        text = font.render("GAME OVER", True, WHITE)
        screen.blit(text, (80, 200))

        info = small_font.render(f"Score: {score}", True, WHITE)
        screen.blit(info, (130, 300))

        hint = small_font.render("Press R to restart", True, WHITE)
        screen.blit(hint, (100, 350))

        if pygame.key.get_pressed()[pygame.K_r]:
            reset_game()
            game_state = "MENU"

    pygame.display.update()

pygame.quit()
sys.exit()