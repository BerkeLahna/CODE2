import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Empty Rectangle Example")

# Create a transparent surface
transparent_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
# transparent_surface.fill((0, 0, 0, 0))  # Fill with a transparent color
# transparent_surface.set_alpha(0)  # Set the alpha value to make it fully transparent

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    # Fill the screen with a background color
    screen.fill((255, 255, 255))

    # Blit the transparent surface at (300, 200)
    screen.blit(transparent_surface, (300, 200))

    # Draw a rectangle over the transparent surface
    pygame.draw.rect(screen, (0, 0, 255), (522, 200, 200, 100))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
