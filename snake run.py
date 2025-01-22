import tkinter as tk
import random

# Game settings
BLOCK_SIZE = 20
GAME_WIDTH = 600
GAME_HEIGHT = 400

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.running = False
        self.score = 0
        
        # Canvas for game
        self.canvas = tk.Canvas(root, width=GAME_WIDTH, height=GAME_HEIGHT, bg="black")
        self.canvas.pack()

        # Buttons
        self.start_button = tk.Button(root, text="Start Game", command=self.start_game, bg="green", fg="white", font=("Arial", 12))
        self.start_button.pack(pady=10)
        self.quit_button = tk.Button(root, text="Quit", command=root.quit, bg="red", fg="white", font=("Arial", 12))
        self.quit_button.pack(pady=10)

        # Game variables
        self.snake = [[100, 100], [80, 100], [60, 100]]  # Initial snake position
        self.food = None
        self.direction = "Right"

        # Keybindings
        self.root.bind("<KeyPress>", self.change_direction)

    def start_game(self):
        self.running = True
        self.score = 0
        self.snake = [[100, 100], [80, 100], [60, 100]]  # Reset snake
        self.direction = "Right"
        self.place_food()
        self.update_game()

    def place_food(self):
        x = random.randint(0, (GAME_WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        y = random.randint(0, (GAME_HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.food = [x, y]

    def change_direction(self, event):
        key = event.keysym
        if key == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.direction = "Right"

    def update_game(self):
        if not self.running:
            return

        # Move snake
        head = self.snake[0].copy()
        if self.direction == "Up":
            head[1] -= BLOCK_SIZE
        elif self.direction == "Down":
            head[1] += BLOCK_SIZE
        elif self.direction == "Left":
            head[0] -= BLOCK_SIZE
        elif self.direction == "Right":
            head[0] += BLOCK_SIZE
        self.snake.insert(0, head)

        # Check collision with walls or itself
        if (head[0] < 0 or head[1] < 0 or
            head[0] >= GAME_WIDTH or head[1] >= GAME_HEIGHT or
            head in self.snake[1:]):
            self.running = False
            self.canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, text=f"Game Over! Score: {self.score}", fill="red", font=("Arial", 20))
            return

        # Check if food is eaten
        if head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()  # Remove tail

        # Redraw game
        self.canvas.delete("all")
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + BLOCK_SIZE, self.food[1] + BLOCK_SIZE, fill="red")
        for block in self.snake:
            self.canvas.create_rectangle(block[0], block[1], block[0] + BLOCK_SIZE, block[1] + BLOCK_SIZE, fill="green")

        # Repeat game loop
        self.root.after(100, self.update_game)

# Initialize and run the game
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
