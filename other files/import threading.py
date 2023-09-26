import threading
import pygame

# Define a function to run the code in a separate thread
def run_code(code):
    try:
        exec(code)
    except Exception as e:
        print(f'Error: {e}')

# Define the Pygame window and other variables
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
code = ''

# Start the main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and event.mod & pygame.KMOD_CTRL:
                # Run the code in a separate thread
                threading.Thread(target=run_code, args=(code,)).start()
                code = ''
            elif event.key == pygame.K_BACKSPACE:
                code = code[:-1]
            else:
                code += event.unicode

    # Clear the screen
    screen.fill((255, 255, 255))

    # Render the code
    code_surface = font.render(code, True, (0, 0, 0))
    screen.blit(code_surface, (10, 10))

    # Update the screen
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)