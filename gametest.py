import pygame

# Player class
class Player:
    def __init__(self):
        self.energy = 0
        self.money = 1000

    def buy_energy_generator(self, cost):
        if self.money >= cost:
            self.money -= cost
            return True
        return False

    def generate_energy(self, amount):
        self.energy += amount

    def sell_energy(self, amount):
        if self.energy >= amount:
            self.energy -= amount
            self.money += amount * 2  # Assuming 1 energy = 2 money
            return True
        return False
    def sell_building(self, cost):
       
        font = pygame.font.Font(None, 36)
        confirmation_text = font.render(f"  Do you want to sell this building for {cost} money?  ", True, (0, 0, 0))
        confirmation_rect = confirmation_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        
        # Draw the confirmation box
        pygame.draw.rect(window, (200, 200, 200), confirmation_rect)
        pygame.draw.rect(window, (0, 0, 0), confirmation_rect, 2)
        window.blit(confirmation_text, confirmation_rect)
        
        yes_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT // 2 + 40, 60, 40)
        no_button_rect = pygame.Rect(WINDOW_WIDTH // 2 + 20, WINDOW_HEIGHT // 2 + 40, 60, 40)
        
        pygame.draw.rect(window, (0, 255, 0), yes_button_rect)
        pygame.draw.rect(window, (255, 0, 0), no_button_rect)
        
        yes_text = font.render("Yes", True, (0, 0, 0))
        no_text = font.render("No", True, (0, 0, 0))
        
        window.blit(yes_text, (yes_button_rect.x + 10, yes_button_rect.y + 5))
        window.blit(no_text, (no_button_rect.x + 15, no_button_rect.y + 5))
        
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if yes_button_rect.collidepoint(mouse_pos):
                        self.money += cost
                        return True
                    elif no_button_rect.collidepoint(mouse_pos):
                        return False
  

# EnergyGenerator class
class EnergyGenerator:
    def __init__(self, cost, heat_per_tick):
        self.cost = cost
        self.heat_per_tick = heat_per_tick

    def generate_heat(self):
        return self.heat_per_tick

class EnergyConverter:
    def __init__(self, cost, energy_per_heat):
        self.cost = cost
        self.energy_per_heat = energy_per_heat

    def convert_heat(self, heat):
        return heat * self.energy_per_heat

class Office:
    def __init__(self):
        self.energy_sell_rate = 5/FPS  # Energy selling rate for the office (per second)

    def sell_energy(self, player):
        # Sell energy at the defined rate
        if player.energy >= self.energy_sell_rate:
            player.energy -= self.energy_sell_rate
            player.money += self.energy_sell_rate * 2  # Assuming 1 energy = 10 money
            
            
            
def switch_view(state):
    if(state == "Buy"):
        # Draw the "Buy" state sidebar
        labels = ["Converter", "Generator", "Office"]
        prices = [CONVERTER_PRICE, GENERATOR_PRICE, OFFICE_PRICE]
        for i in range(len(labels)):
            label_text = font.render(f'{labels[i]} (${prices[i]})', True, (0, 0, 0))
            print(label_text)
            window.blit(label_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, i * SIDEBAR_ITEM_HEIGHT + 10))
    elif(state == "Upgrade"):
        # Draw the "Upgrade" state sidebar
        labels = ["Converter2", "Generator2", "Office2"]
        prices = [CONVERTER_PRICE, GENERATOR_PRICE, OFFICE_PRICE]
        for i in range(len(labels)):
            label_text = font.render(f'{labels[i]} (${prices[i]})', True, (0, 0, 0))
            window.blit(label_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, i * SIDEBAR_ITEM_HEIGHT + 10))
        
        
    


# Tile constants
TILE_SIZE = 50
NUM_TILES_X = 16  # Adjusted for the grid size
NUM_TILES_Y = 12  # Adjusted for the grid size

# Sidebar constants
SIDEBAR_WIDTH = 500
SIDEBAR_ITEM_HEIGHT = 50

# Colors
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Tile types
TILE_EMPTY = 0
TILE_CONVERTER = 1
TILE_GENERATOR = 2
TILE_OFFICE = 3

# Object prices
CONVERTER_PRICE = 200
GENERATOR_PRICE = 300
OFFICE_PRICE = 500

# Energy production rates for each building type
ENERGY_RATE_CONVERTER = 2/60
ENERGY_RATE_GENERATOR = 5/60

# Initialize pygame
pygame.init()

# Initialize the window
WINDOW_WIDTH = NUM_TILES_X * TILE_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = NUM_TILES_Y * TILE_SIZE + 50
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Energy Tycoon')

# Clock to control FPS
FPS = 60  # Lower FPS for slower game
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)


# Initialize game objects
player = Player()
energy_generator = EnergyGenerator(cost=100, heat_per_tick=20/FPS)  # Slower energy generation
energy_converter = EnergyConverter(cost=150, energy_per_heat=50/FPS)  # More efficient conversion
heat_grid = [[0 for _ in range(NUM_TILES_Y)] for _ in range(NUM_TILES_X)]  # Heat grid for generators

# Initialize the grid with empty tiles
grid = [[TILE_EMPTY for _ in range(NUM_TILES_Y)] for _ in range(NUM_TILES_X)]



# Define building upgrades
upgrades = {
    "Converter": ("Improved Conversion", 100),
    "Generator": ("Increased Heat Generation", 150),
    "Office": ("Faster Energy Selling", 200)
}

# Initialize the state
current_state = "Buy"

# Game loop
running = True
selected_building = None  # Selected building type (None, CONVERTER, GENERATOR, OFFICE)
buy_button = font.render("Buy", True, (0, 0, 0))
buy_button_rect = buy_button.get_rect(center=(WINDOW_WIDTH + 100, WINDOW_HEIGHT + 250))
upgrade_button = font.render("Upgrade", True, (0, 0, 0))
upgrade_button_rect = upgrade_button.get_rect(center=(WINDOW_WIDTH - 250, 25))



office = Office()  # Initialize the office

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:  # Left click
                mouse_x, mouse_y = pygame.mouse.get_pos()

# Check if the mouse is within the "Buy" button area
                if (WINDOW_WIDTH - 100 <= mouse_x <= WINDOW_WIDTH and
                    WINDOW_HEIGHT - 25  <= mouse_y <= WINDOW_HEIGHT):
                        # Check if the "Upgrade" button is clicked
                        switch_view("Buy") 
                elif (WINDOW_WIDTH - 250 <= mouse_x <= WINDOW_WIDTH - 100  and
                      WINDOW_HEIGHT - 25  <= mouse_y <= WINDOW_HEIGHT):
                        # Check if the "Upgrade" button is clicked
                        switch_view("Upgrade") 
                if WINDOW_WIDTH - SIDEBAR_WIDTH <= mouse_pos[0] < WINDOW_WIDTH:
                    selected_building = (mouse_pos[1] // SIDEBAR_ITEM_HEIGHT) + 1
                if WINDOW_WIDTH - SIDEBAR_WIDTH + 10 <= mouse_pos[0] < WINDOW_WIDTH - SIDEBAR_WIDTH + 290 and WINDOW_HEIGHT - 160 <= mouse_pos[1] < WINDOW_HEIGHT - 110:
                        # Convert energy to money
                        player.sell_energy(player.energy)  # Sell all available energy
                        # Update money display after successful conversion
                        money_text = font.render(f'Money: {int(player.money)}', True, (0, 0, 0))
                else:
                    # Place selected building on the grid
                    grid_x = mouse_pos[0] // TILE_SIZE
                    grid_y = mouse_pos[1] // TILE_SIZE
                    if 0 <= grid_x < NUM_TILES_X and 0 <= grid_y < NUM_TILES_Y:
                        if selected_building == 1 and player.buy_energy_generator(CONVERTER_PRICE):
                            grid[grid_x][grid_y] = TILE_CONVERTER
                        elif selected_building == 2 and player.buy_energy_generator(GENERATOR_PRICE):
                            grid[grid_x][grid_y] = TILE_GENERATOR
                        elif selected_building == 3 and player.buy_energy_generator(OFFICE_PRICE):
                            grid[grid_x][grid_y] = TILE_OFFICE
            elif event.button == 3:  # Right click
                # Sell selected building on the grid
                grid_x = mouse_pos[0] // TILE_SIZE
                grid_y = mouse_pos[1] // TILE_SIZE
                if 0 <= grid_x < NUM_TILES_X and 0 <= grid_y < NUM_TILES_Y:
                    if grid[grid_x][grid_y] == TILE_CONVERTER:
                        if(player.sell_building(CONVERTER_PRICE)):
                            grid[grid_x][grid_y] = TILE_EMPTY
                    elif grid[grid_x][grid_y] == TILE_GENERATOR:
                        if(player.sell_building(GENERATOR_PRICE)):
                            grid[grid_x][grid_y] = TILE_EMPTY
                    elif grid[grid_x][grid_y] == TILE_OFFICE:
                        if(player.sell_building(OFFICE_PRICE)):
                            grid[grid_x][grid_y] = TILE_EMPTY
    # Draw the game window

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if buy_button_rect.collidepoint(mouse_pos):
            current_state = "Buy"
        elif upgrade_button_rect.collidepoint(mouse_pos):
            current_state = "Upgrade"            
                        
                        
    pygame.draw.rect(window, WHITE, (WINDOW_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))
    font = pygame.font.Font(None, 24)

    # Draw the "Buy" button
    pygame.draw.rect(window, (200, 200, 200), buy_button_rect)
    buy_button_text = font.render("Buy", True, (0, 0, 0))
    window.blit(buy_button_text, (buy_button_rect.x + 10, buy_button_rect.y + 10))

    # Draw the "Upgrade" button
    pygame.draw.rect(window, (200, 200, 200), upgrade_button_rect)
    upgrade_button_text = font.render("Upgrade", True, (0, 0, 0))
    window.blit(upgrade_button_text, (upgrade_button_rect.x + 10, upgrade_button_rect.y + 10))

   

    

    # Update game logic

    # Generate heat from generators
    total_heat_generated = 0
    for i in range(NUM_TILES_X):
        for j in range(NUM_TILES_Y):
            if grid[i][j] == TILE_GENERATOR:
                # Generate heat in adjacent tiles
                for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                        if 0 <= x < NUM_TILES_X and 0 <= y < NUM_TILES_Y and not (x == i and y == j):
                            heat_grid[x][y] += energy_generator.generate_heat()
                            total_heat_generated += energy_generator.generate_heat()

    # Convert heat to energy using converters
    total_energy = 0
    for i in range(NUM_TILES_X):
        for j in range(NUM_TILES_Y):
            if grid[i][j] == TILE_CONVERTER:
                total_energy += energy_converter.convert_heat(heat_grid[i][j])
                heat_grid[i][j] = 0  # Reset heat in the converter tile

    player.generate_energy(total_energy)

    # Calculate energy generation rate
    energy_generation_rate = total_energy * FPS

    # Sell energy using the office
    total_energy_sold = 0
    for i in range(NUM_TILES_X):
        for j in range(NUM_TILES_Y):
            if grid[i][j] == TILE_OFFICE:
                office.sell_energy(player)
                total_energy_sold += office.energy_sell_rate

    # Display game information
    window.fill(GRAY)
    

    # Draw tiles and objects
    for i in range(NUM_TILES_X):
        for j in range(NUM_TILES_Y):
            rect = pygame.Rect(i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if grid[i][j] == TILE_CONVERTER:
                pygame.draw.rect(window, RED, rect)
            elif grid[i][j] == TILE_GENERATOR:
                pygame.draw.rect(window, YELLOW, rect)
            elif grid[i][j] == TILE_OFFICE:
                pygame.draw.rect(window, GREEN, rect)
            else:
                pygame.draw.rect(window, WHITE, rect, 1)

    # Draw sidebar and objects to be placed
    pygame.draw.rect(window, WHITE, (WINDOW_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))

    # Sidebar labels and prices
    labels = ["Converter", "Generator", "Office"]
    prices = [CONVERTER_PRICE, GENERATOR_PRICE, OFFICE_PRICE]
    for i in range(len(labels)):
        label_text = font.render(f'{labels[i]} (${prices[i]})', True, (0, 0, 0))
        window.blit(label_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, i * SIDEBAR_ITEM_HEIGHT + 10))
        
    convert_button = font.render(f'Convert Energy To Money', True, (0, 0, 0), (125, 255,125)) 
    window.blit(convert_button, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 160))
    
    # Display game information (money and power)
    money_text = font.render(f'Money: {int(player.money)}', True, (0, 0, 0))
    energy_text = font.render(f'Energy: {int(player.energy)}', True, (0, 0, 0))
    total_energy_text = font.render(f'Energy Per Second: {int(total_energy_sold*60*2.5)}', True, (0, 0, 0))
    window.blit(money_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 80))
    window.blit(energy_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 300, WINDOW_HEIGHT - 80))
    window.blit(total_energy_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 120))
    
    
    # Create a new surface for the bottom bar
    bottom_bar = pygame.Surface((WINDOW_WIDTH, 50))
    bottom_bar.fill((200, 200, 200))

    # Draw the "Buy" button on the bottom bar
    buy_button = font.render("Buy", True, (0, 0, 0))
    buy_button_rect = buy_button.get_rect(center=(WINDOW_WIDTH - 100, 25))
    bottom_bar.blit(buy_button, buy_button_rect)

    # Draw the "Upgrade" button on the bottom bar
    upgrade_button = font.render("Upgrade", True, (0, 0, 0))
    upgrade_button_rect = upgrade_button.get_rect(center=(WINDOW_WIDTH - 250, 25))
    bottom_bar.blit(upgrade_button, upgrade_button_rect)

    # Blit the bottom bar onto the main window
    window.blit(bottom_bar, (0, WINDOW_HEIGHT - 50))



    # Check if mouse is hovering over a placed building
    mouse_pos = pygame.mouse.get_pos()
    grid_x = mouse_pos[0] // TILE_SIZE
    grid_y = mouse_pos[1] // TILE_SIZE
    if 0 <= grid_x < NUM_TILES_X and 0 <= grid_y < NUM_TILES_Y:
        if grid[grid_x][grid_y] == TILE_CONVERTER:
            info_text = font.render(f'Energy per heat: {energy_converter.energy_per_heat}', True, (0, 0, 0))
            window.blit(info_text, (mouse_pos[0] + 10, mouse_pos[1] + 10))
        elif grid[grid_x][grid_y] == TILE_GENERATOR:
            info_text = font.render(f'Heat per tick: {energy_generator.heat_per_tick}', True, (0, 0, 0))
            window.blit(info_text, (mouse_pos[0] + 10, mouse_pos[1] + 10))
        elif grid[grid_x][grid_y] == TILE_OFFICE:
            info_text = font.render(f'Energy sell rate: {office.energy_sell_rate * 60:.2f} per second', True, (0, 0, 0))
            window.blit(info_text, (mouse_pos[0] + 10, mouse_pos[1] + 10))

    
    

    # Update the screen
    pygame.display.flip()
    clock.tick(FPS)

# Quit pygame
pygame.quit()