import pygame
import random
import json
import sys
import psycopg2
import time

pygame.init()

# ================= DATABASE =================
def connect():
    import psycopg2

    dsn = "dbname=snake_db user=postgres password=lolpoqpwerty host=localhost port=5432"

    return psycopg2.connect(dsn)

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER,
        level INTEGER,
        played_at TIMESTAMP DEFAULT NOW()
    );
    """)

    conn.commit()
    conn.close()

def get_player(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    r = cur.fetchone()

    if r:
        return r[0]

    cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
    pid = cur.fetchone()[0]

    conn.commit()
    conn.close()
    return pid

def save_game(pid, score, level):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO game_sessions (player_id, score, level)
        VALUES (%s, %s, %s)
    """, (pid, score, level))

    conn.commit()
    conn.close()

def leaderboard():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, g.score, g.level
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        ORDER BY g.score DESC
        LIMIT 10
    """)

    data = cur.fetchall()
    conn.close()
    return data

def best_score(pid):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id=%s", (pid,))
    r = cur.fetchone()[0]

    conn.close()
    return r or 0

# ================= SETTINGS =================
def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
        return {"snake_color": [0,255,0], "grid": True, "sound": True}

def save_settings(s):
    with open("settings.json", "w") as f:
        json.dump(s, f)

settings = load_settings()

# ================= GAME =================
WIDTH, HEIGHT = 800, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)

state = "menu"

username = ""
player_id = None
pb = 0

snake = []
direction = (CELL, 0)

food = None
poison = None
power = None
obstacles = []

score = 0
level = 1
speed = 10

shield = False

# power timing
speed_time = 0
slow_time = 0

# ================= HELPERS =================
def spawn():
    return (random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL))

def spawn_obstacles():
    return [spawn() for _ in range(level * 3)]

def draw_button(text, x, y, w, h):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    rect = pygame.Rect(x, y, w, h)
    color = (80,80,80)

    if rect.collidepoint(mouse):
        color = (130,130,130)
        if click[0]:
            return True

    pygame.draw.rect(screen, color, rect)
    screen.blit(font.render(text, True, (255,255,255)), (x+10,y+10))
    return False

def reset_game():
    global snake, direction, score, level, food, poison, power, obstacles, shield

    snake = [(100,100)]
    direction = (CELL,0)

    food = spawn()
    poison = None
    power = None
    obstacles = []

    score = 0
    level = 1
    shield = False

# ================= INIT =================
init_db()

# ================= SCREENS =================
def menu():
    global state, username, player_id, pb

    screen.fill((0,0,0))
    screen.blit(font.render("SNAKE GAME", True, (0,255,0)), (300,80))

    if draw_button("PLAY", 300,200,200,50):
        if username:
            player_id = get_player(username)
            pb = best_score(player_id)
            reset_game()
            state = "game"

    if draw_button("LEADERBOARD",300,270,200,50):
        state = "leaderboard"

    if draw_button("SETTINGS",300,340,200,50):
        state = "settings"

    if draw_button("QUIT",300,410,200,50):
        pygame.quit()
        sys.exit()

    screen.blit(font.render("Username: "+username, True,(255,255,255)), (250,500))

def game():
    global snake, direction, food, poison, power, score, level
    global speed, shield, state, speed_time, slow_time

    screen.fill((0,0,0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: direction = (-CELL,0)
    if keys[pygame.K_RIGHT]: direction = (CELL,0)
    if keys[pygame.K_UP]: direction = (0,-CELL)
    if keys[pygame.K_DOWN]: direction = (0,CELL)

    head = (snake[0][0]+direction[0], snake[0][1]+direction[1])
    snake.insert(0, head)

    # walls
    if head[0]<0 or head[1]<0 or head[0]>=WIDTH or head[1]>=HEIGHT:
        state = "gameover"

    # self
    if head in snake[1:] and not shield:
        state = "gameover"

    # obstacles
    if level>=3 and head in obstacles:
        state = "gameover"

    # food
    if head == food:
        score += 1
        food = spawn()

        if score % 5 == 0:
            level += 1
            obstacles = spawn_obstacles()
    else:
        snake.pop()

    # poison
    if random.random() < 0.01:
        poison = spawn()

    if poison and head == poison:
        snake = snake[:-2]
        poison = None
        if len(snake)<=1:
            state="gameover"

    # power
    now = pygame.time.get_ticks()

    if not power and random.random()<0.005:
        power = {"pos":spawn(),"type":random.choice(["speed","slow","shield"]),"t":now}

    if power:
        if head == power["pos"]:
            if power["type"]=="speed":
                speed_time = now + 5000
            if power["type"]=="slow":
                slow_time = now + 5000
            if power["type"]=="shield":
                shield = True
            power = None

    # speed logic
    current_speed = speed
    if now < speed_time:
        current_speed = 18
    if now < slow_time:
        current_speed = 5

    # draw
    for s in snake:
        pygame.draw.rect(screen, settings["snake_color"], (*s,CELL,CELL))

    pygame.draw.rect(screen,(0,255,0),(*food,CELL,CELL))

    if poison:
        pygame.draw.rect(screen,(150,0,0),(*poison,CELL,CELL))

    if power:
        pygame.draw.rect(screen,(0,0,255),(*power["pos"],CELL,CELL))

    for o in obstacles:
        pygame.draw.rect(screen,(120,120,120),(*o,CELL,CELL))

    screen.blit(font.render(f"Score:{score} Level:{level} PB:{pb}",True,(255,255,255)),(10,10))

    pygame.display.update()
    clock.tick(current_speed)

def gameover():
    global state

    screen.fill((50,0,0))
    screen.blit(font.render("GAME OVER",True,(255,0,0)),(300,100))
    screen.blit(font.render(f"Score:{score}",True,(255,255,255)),(320,180))

    if draw_button("RETRY",300,300,200,50):
        reset_game()
        state="game"

    if draw_button("MENU",300,370,200,50):
        save_game(player_id,score,level)
        state="menu"

def leaderboard_screen():
    screen.fill((0,0,50))

    screen.blit(font.render("LEADERBOARD",True,(255,255,0)),(300,50))

    y=120
    for u,s,l in leaderboard():
        screen.blit(font.render(f"{u} {s} L{l}",True,(255,255,255)),(250,y))
        y+=40

    if draw_button("BACK",300,500,200,50):
        state="menu"

def settings_screen():
    global state

    screen.fill((30,30,30))

    if draw_button("GREEN SNAKE",250,200,300,50):
        settings["snake_color"]=[0,255,0]

    if draw_button("SAVE & BACK",250,300,300,50):
        save_settings(settings)
        state="menu"

# ================= MAIN LOOP =================
running=True

while running:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False

        if e.type==pygame.KEYDOWN and state=="menu":
            if e.key==pygame.K_BACKSPACE:
                username=username[:-1]
            else:
                username+=e.unicode

    if state=="menu": menu()
    elif state=="game": game()
    elif state=="gameover": gameover()
    elif state=="leaderboard": leaderboard_screen()
    elif state=="settings": settings_screen()

    clock.tick(60)

pygame.quit()