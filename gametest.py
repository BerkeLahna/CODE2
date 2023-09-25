import pygame
import importablemenu

# Player class
class Player:
    def __init__(self):
        self.energy = 0
        self.money = 100000

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
    def __init__(self, tier,cost, heat_per_tick):
        self.cost = cost*tier*(4 if tier != 1 else 1)
        self.heat_per_tick = heat_per_tick*(1 if tier == 1 else 4)

    def generate_heat(self):
        return self.heat_per_tick

class EnergyConverter:
    def __init__(self,tier, cost, energy_per_heat):
        self.cost = cost*tier*(1 if tier == 1 else 4)
        self.energy_per_heat = energy_per_heat*(1 if tier == 1 else 4)

    def convert_heat(self, heat):
        return heat * self.energy_per_heat

class Office:
    def __init__(self,tier,cost):
        self.energy_sell_rate = 5*tier/FPS  # Energy selling rate for the office (per second)
        self.cost = cost*tier*(4 if tier != 1 else 1)
    def sell_energy(self, player):
        # Sell energy at the defined rate
        if player.energy >= self.energy_sell_rate:
            player.energy -= self.energy_sell_rate 
            player.money += self.energy_sell_rate  # Assuming 1 energy = 10 money
            
class Button():
    def __init__(self, x, y, width, height, text='', command=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 22)
        self.command = command

    def draw(self, surface):
        pygame.draw.rect(surface,GRAY , self.rect)
        if self.text:
            text = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.command:
                self.command()
            
def switch_view(state, tier):
    if state == "Buy":
        items = [
            EnergyConverter(tier,CONVERTER_PRICE, ENERGY_RATE_CONVERTER*tier),
            EnergyGenerator(tier, GENERATOR_PRICE, ENERGY_RATE_GENERATOR*tier),
            Office(tier, OFFICE_PRICE)
        ]
    elif state == "Upgrade":
        items = [
            EnergyConverter(tier,CONVERTER_PRICE, ENERGY_RATE_CONVERTER*tier),
            EnergyGenerator(tier, GENERATOR_PRICE, ENERGY_RATE_GENERATOR*tier),
            Office(tier, OFFICE_PRICE)
        ]

    labels = ["Converter", "Generator", "Office"]
    for i, item in enumerate(items):
        # price = item.cost * (2 if state == "Upgrade" else 1)
        price = item.cost
        label_text = font.render(f'{labels[i],tier} (${price})', True, (0, 0, 0))
        window.blit(label_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, i * SIDEBAR_ITEM_HEIGHT + 10))
        
    
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



# Create a new surface for the bottom bar
bottom_bar = pygame.Surface((WINDOW_WIDTH, 50))
bottom_bar.fill((200, 200, 200))

# Clock to control FPS
FPS = 60  # Lower FPS for slower game
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)


# Initialize game objects
player = Player()
energy_generator = EnergyGenerator(1,cost=100, heat_per_tick=20/FPS)  # Slower energy generation
energy_converter = EnergyConverter(1,cost=150, energy_per_heat=50/FPS)  # More efficient conversion
heat_grid = [[0 for _ in range(NUM_TILES_Y)] for _ in range(NUM_TILES_X)]  # Heat grid for generators

# Initialize the grid with empty tiles
grid = [[TILE_EMPTY for _ in range(NUM_TILES_Y)] for _ in range(NUM_TILES_X)]



# Sample prices for different tiers (you should replace these with your actual prices)
TIER_PRICES = {
    1: [[10, 20, 30], [40, 50, 60]],  # Prices for tier 1 for pages 1 and 2
    2: [[50, 60, 70], [80, 90, 100]]   # Prices for tier 2 for pages 1 and 2 (example)
}

# Define building upgrades
upgrades = {
    "Converter": ("Improved Conversion", 100),
    "Generator": ("Increased Heat Generation", 150),
    "Office": ("Faster Energy Selling", 200)
}



# Game loop
running = True
selected_building = None  # Selected building type (None, CONVERTER, GENERATOR, OFFICE)



current_tier = 1
current_page = 1
display_sidebar(current_tier, current_page)



#DEFINE BUTTONS
buy_button1 = Button(815, 295, 100, 30, 'Buy', lambda: print('Button clicked'))
upgrade_button1 = Button(1100, 295, 100, 30, 'Upgrade', lambda: print('Button clicked'))
forward_button = Button(1100, 255, 100, 30, '>>', lambda: print('Button clicked'))
previous_button = Button(815, 255, 100, 30, '<<', lambda: print('Button clicked'))



state = "Buy"

switch_view("Buy",current_tier)
office = Office(1,OFFICE_PRICE)  # Initialize the office

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:  # Left click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if previous_button.rect.collidepoint(mouse_pos):
                    current_tier -=1
                    
                if forward_button.rect.collidepoint(mouse_pos):
                    current_tier +=1
                    
                if buy_button1.rect.collidepoint(mouse_pos):
                    state = "Buy"
                    print("Buy button clicked")
                if upgrade_button1.rect.collidepoint(mouse_pos):
                    state = "Upgrade"
                    print("upgrade button clicked")
# Check if the mouse is within the "Buy" button area
                
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
                        if selected_building == 1 and player.buy_energy_generator(CONVERTER_PRICE*current_tier):
                            grid[grid_x][grid_y] = TILE_CONVERTER
                        elif selected_building == 2 and player.buy_energy_generator(GENERATOR_PRICE*current_tier):
                            grid[grid_x][grid_y] = TILE_GENERATOR
                        elif selected_building == 3 and player.buy_energy_generator(OFFICE_PRICE*current_tier):
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


               
  
    font = pygame.font.Font(None, 24)


    #draw
    window.fill(GRAY)
    pygame.draw.rect(window, WHITE, (WINDOW_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))   
    switch_view(state,current_tier)
    # display_sidebar(current_tier, current_page)

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
    
    

    converter_image = pygame.transform.scale(pygame.image.load('converter.png'), (50, 50))
    generator_image = pygame.transform.scale(pygame.image.load('generator1.png'), (50, 50))
    office_image = pygame.transform.scale(pygame.image.load('office.png'), (50, 50))
   # Draw tiles and objects
    for i in range(NUM_TILES_X):
        for j in range(NUM_TILES_Y):
            rect = pygame.Rect(i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if grid[i][j] == TILE_CONVERTER:
                window.blit(converter_image, rect)
            elif grid[i][j] == TILE_GENERATOR:
                window.blit(generator_image, rect)
            elif grid[i][j] == TILE_OFFICE:
                window.blit(office_image, rect)
            else:
                pygame.draw.rect(window, WHITE, rect, 1)


        
    convert_button = font.render(f'Convert Energy To Money', True, (0, 0, 0), (125, 255,125)) 
    window.blit(convert_button, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 160))
    
    # Display game information (money and power)
    money_text = font.render(f'Money: {int(player.money)}', True, (0, 0, 0))
    energy_text = font.render(f'Energy: {int(player.energy)}', True, (0, 0, 0))
    total_energy_text = font.render(f'Energy Per Second: {int(total_energy_sold*60*2.5)}', True, (0, 0, 0))
    window.blit(money_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 80))
    window.blit(energy_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 300, WINDOW_HEIGHT - 80))
    window.blit(total_energy_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 120))
    


    # Blit the bottom bar onto the main window
    window.blit(bottom_bar, (0, WINDOW_HEIGHT - 50))

    #DRAW BUTTONS
    buy_button1.draw(window)
    upgrade_button1.draw(window)
    forward_button.draw(window)
    previous_button.draw(window)    

    # Check if mouse is hovering over a placed building
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pos = pygame.mouse.get_pos()
    test = font.render(f'Coordinates: {mouse_x,mouse_y}', True, (0, 0, 0))
    window.blit(test,( mouse_pos[0], mouse_pos[1]))
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