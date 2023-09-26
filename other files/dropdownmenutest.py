import pygame
import sys

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Define the dropdown menus
dropdown_menus = [
    {
        'x': 50,
        'y': 50,
        'visible': False,
        'button_text': 'Menu 1',
        'options': ['Option 1', 'Option 2', 'Option 3']
    },
    {
        'x': 200,
        'y': 50,
        'visible': False,
        'button_text': 'Menu 2',
        'options': ['Option 4', 'Option 5', 'Option 6']
    }
]

def draw_dropdown_menu(menu):
    """Draw a dropdown menu on the screen."""
    # Draw the button
    button_rect = pygame.Rect(menu['x'], menu['y'], 120, 30)
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 1)
    font = pygame.font.SysFont(None, 24)
    button_text = font.render(menu['button_text'], True, BLACK)
    screen.blit(button_text, (menu['x'] + 10, menu['y'] + 5))

    # Calculate the position for the dropdown options
    dropdown_options_y = menu['y'] + 30

    # Draw the options
    if menu['visible']:
        for i, option in enumerate(menu['options']):
            option_rect = pygame.Rect(50, dropdown_options_y + i * 30, 120, 30)
            pygame.draw.rect(screen, WHITE, option_rect)
            pygame.draw.rect(screen, BLACK, option_rect, 1)
            font = pygame.font.SysFont(None, 24)
            option_text = font.render(option, True, BLACK)
            screen.blit(option_text, (50, dropdown_options_y + 5 + i * 30))


def main():
    """Run the main loop of the program."""
    global dropdown_menus

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    for menu in dropdown_menus:
                        if menu['x'] <= x <= menu['x'] + 120 and menu['y'] <= y <= menu['y'] + 30:
                            # Close any other visible menus
                            for other_menu in dropdown_menus:
                                if other_menu != menu and other_menu['visible']:
                                    other_menu['visible'] = False
                            # Open the selected menu
                            menu['visible'] = not menu['visible']
                            print(f'Button pressed: {menu["button_text"]}')
                        elif menu['visible']:
                            for i, option in enumerate(menu['options']):
                                option_rect = pygame.Rect( 50, menu['y'] + 30 + i * 30, 120, 30)
                                if option_rect.collidepoint(x, y):
                                    print(f'Option selected: {option}')

        # Clear the screen
        screen.fill(WHITE)

        # Draw the dropdown menus
        for menu in dropdown_menus:
            draw_dropdown_menu(menu)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()
    
if __name__ == '__main__':
    # Initialize pygame
    pygame.init()

    # Set up the screen
    WIDTH, HEIGHT = 400, 300
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Multiple Dropdown Menus Example")

    # Run the main function
    main()
