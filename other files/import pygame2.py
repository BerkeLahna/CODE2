import pygame

# Constants for sidebar layout
SIDEBAR_WIDTH = 200
SIDEBAR_ITEM_HEIGHT = 30
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Sample prices for different tiers (you should replace these with your actual prices)
TIER_PRICES = {
    1: [[10, 20, 30], [40, 50, 60]],  # Prices for tier 1 for pages 1 and 2
    2: [[50, 60, 70], [80, 90, 100]]   # Prices for tier 2 for pages 1 and 2 (example)
}

# Initialize pygame
pygame.init()

# Set up the window and font
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
font = pygame.font.Font(None, 24)

def display_sidebar(tier, page):
    labels = ["Converter", "Generator", "Office"]
    prices = TIER_PRICES.get(tier, [])  # Get prices for the current tier and page

    for i in range(len(labels)):
        label_text = font.render(f'{"Tier ",page," "+labels[i]} (${prices[page-1][i]})', True, (0, 0, 0))
        window.blit(label_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, i * SIDEBAR_ITEM_HEIGHT + 10))
       
    convert_button = font.render(f'Convert Energy To Money', True, (0, 0, 0), (125, 255, 125)) 
    window.blit(convert_button, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 160))

    # Display page switch buttons
    button_text = font.render(f'Page {page}', True, (0, 0, 0), (200, 200, 200))
    window.blit(button_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 120))

# Example usage: Display tier 1 sidebar and page switch buttons for page 1
current_tier = 1
current_page = 1
display_sidebar(current_tier, current_page)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if the mouse click is within the page switch button
            if WINDOW_WIDTH - SIDEBAR_WIDTH + 10 <= mouse_x <= WINDOW_WIDTH - SIDEBAR_WIDTH + 10 + 100 \
                    and WINDOW_HEIGHT - 120 <= mouse_y <= WINDOW_HEIGHT - 90:
                # Increment the page and redisplay the sidebar
                current_page = (current_page % 2) + 1  # Toggle between 1 and 2
                window.fill((255, 255, 255))  # Clear the window
                display_sidebar(current_tier, current_page)  # Display the updated sidebar

    # Update the display
    pygame.display.flip()

pygame.quit()
