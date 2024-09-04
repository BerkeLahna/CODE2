import pygame
import sys

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Pygame GUI")

# Font
font = pygame.font.Font(None, 36)

# List to hold buttons
buttons = []

# Function to create a button
def create_button(x, y, width, height, text):
    button_surface = pygame.Surface((width, height))
    button_rect = button_surface.get_rect()
    button_rect.topleft = (x, y)
    
    # Render text on the button
    button_text = font.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=button_rect.center)
    
    # Draw button background
    button_surface.fill(GRAY)
    
    # Draw button border
    pygame.draw.rect(button_surface, BLACK, button_rect, 2)
    
    # Blit text on button
    button_surface.blit(button_text, text_rect)
    
    return button_surface, button_rect

# Add initial buttons
buttons.append(create_button(50, 50, 200, 50, "Button 1"))
buttons.append(create_button(50, 150, 200, 50, "Button 2"))

# Main loop
running = True
while running:
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for button, rect in buttons:
                    if rect.collidepoint(event.pos):
                        # Remove the button when clicked
                        buttons.remove((button, rect))
                        break
            elif event.button == 3:  # Right mouse button
                # Add a new button where clicked
                new_button = create_button(event.pos[0], event.pos[1], 200, 50, "New Button")
                buttons.append(new_button)

    # Draw buttons
    for button, rect in buttons:
        screen.blit(button, rect)
    
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
