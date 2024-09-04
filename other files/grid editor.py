import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Set the dimensions of the grid
GRID_WIDTH = 50
GRID_HEIGHT = 30
CELL_SIZE = 20

# Initialize Pygame
pygame.init()

# Set the size of the screen
screen_size = (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)
screen = pygame.display.set_mode(screen_size)

# Set the title of the window
pygame.display.set_caption("Grid Editor")

# Create a 2D array to store the state of each cell
grid = [[0 for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
dragging = False
last_toggled = None  # keep track of the last cell that was toggled

# Define a function to draw the grid
def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[x][y]:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

# Define a function to toggle the state of a cell
def toggle_cell(x, y):
    grid[x][y] = (1 if not grid[x][y] else 0)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle the state of the clicked cell
            x, y = event.pos
            if event.button == 1:  # left mouse button
                x //= CELL_SIZE
                y //= CELL_SIZE
                toggle_cell(x, y)
                dragging = True
                last_toggled = (x, y)  # update last_toggled
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # left mouse button
                dragging = False
                last_toggled = None  # reset last_toggled
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                x, y = event.pos
                x //= CELL_SIZE
                y //= CELL_SIZE
                if (x, y) != last_toggled:  # toggle only if different from last_toggled
                    toggle_cell(x, y)
                    last_toggled = (x, y)
            
    # Draw the grid
    draw_grid()

    # Update the screen
    pygame.display.flip()

# Quit Pygame
print(grid)
pygame.quit()
