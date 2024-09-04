import pygame

# Initialize Pygame
pygame.init()

# Set up the window
window_width = 640
window_height = 480
window = pygame.display.set_mode((window_width, window_height))

# Set up the scrollbar container
scrollbar_container_width = 100
scrollbar_container_height = 200
scrollbar_container_surface = pygame.Surface((scrollbar_container_width, scrollbar_container_height))
scrollbar_container_rect = pygame.Rect(500, 50, scrollbar_container_width, scrollbar_container_height)

# Set up the scrollbar track
scrollbar_track_width = scrollbar_container_width
scrollbar_track_height = 180
scrollbar_track_surface = pygame.Surface((scrollbar_track_width, scrollbar_track_height))
scrollbar_track_rect = pygame.Rect(0, 10, scrollbar_track_width, scrollbar_track_height)
scrollbar_track_surface.fill((200, 200, 200))

# Set up the scrollbar thumb
scrollbar_thumb_width = 20
scrollbar_thumb_height = 50
scrollbar_thumb_surface = pygame.Surface((scrollbar_thumb_width, scrollbar_thumb_height))
scrollbar_thumb_rect = pygame.Rect(0, 0, scrollbar_thumb_width, scrollbar_thumb_height)
scrollbar_thumb_surface.fill((100, 100, 100))

# Set up the buttons
button_width = 80
button_height = 30
button_spacing = 10
button_list = []
for i in range(5):
    button_rect = pygame.Rect(10, i * (button_height + button_spacing) + 10, button_width, button_height)
    button_surface = pygame.Surface((button_width, button_height))
    button_surface.fill((255, 255, 255))
    button_list.append(Button(button_surface, button_rect))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw the scrollbar container
    window.blit(scrollbar_container_surface, scrollbar_container_rect)

    # Draw the scrollbar track
    scrollbar_container_surface.blit(scrollbar_track_surface, scrollbar_track_rect)

    # Draw the scrollbar thumb
    scrollbar_track_surface.blit(scrollbar_thumb_surface, scrollbar_thumb_rect)

    # Draw the buttons
    for button in button_list:
        scrollbar_container_surface.blit(button.surface, button.rect)

    # Update the display
    pygame.display.update()