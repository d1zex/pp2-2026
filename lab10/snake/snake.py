from tkinter import *
import random

# Game configuration
GAME_WIDTH = 800
GAME_HEIGHT = 700
SPEED = 200 
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Initialize level and score
LEVEL = 1
SCORE = 0


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Initialize the snake's body at the top-left corner
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        while True:
            # Generate a random position for the food
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

            # Ensure food doesn't spawn on the snake
            if [x, y] not in snake.coordinates:
                break

        self.coordinates = [x, y]

        # Create the food on the canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    global SCORE, SPEED, LEVEL

    # Get the current position of the snake's head
    x, y = snake.coordinates[0]

    # Update the snake's direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Add the new head position to the snake's body
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if the snake eats the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        SCORE += 1
        label_score.config(text=f"Score: {SCORE}")

        # Level up every 5 points
        if SCORE % 5 == 0:
            LEVEL += 1
            SPEED -= 20  # Increase speed
            label_level.config(text=f"Level: {LEVEL}")

        # Generate new food
        canvas.delete("food")
        food = Food()
    else:
        # Remove the tail if no food is eaten
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions
    if check_collisions(snake):
        game_over()
    else:
        # Continue the game
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    """Change the snake's direction based on user input."""
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions(snake):
    """Check for collisions with the walls or the snake's own body."""
    x, y = snake.coordinates[0]

    # Check if the snake hits the walls
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    # Check if the snake collides with itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    """Display Game Over message and stop the game."""
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=('consolas', 70),
        text="Ti proigral :(",
        fill="red",
        tag="gameover"
    )


# Initialize the main window
window = Tk()
window.title("Igra Zmeya")
window.resizable(False, False)

# Display score and level
label_score = Label(window, text=f"Score: {SCORE}", font=('consolas', 20))
label_score.pack()
label_level = Label(window, text=f"Level: {LEVEL}", font=('consolas', 20))
label_level.pack()

# Create the game canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center the window on the screen
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind arrow keys for snake movement
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Initialize the snake and food
snake = Snake()
food = Food()

# Set the initial direction
direction = 'down'

# Start the game loop
next_turn(snake, food)

# Run the tkinter main loop
window.mainloop()
