import pygame


# Player class
class Player:
    def __init__(self):
        self.energy = 0
        self.money = 10000

    def buy_energy_generator(self, Building):
        if self.money >= Building.cost:
            self.money -= Building.cost
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
    def sell_building(self, Building):
       
        font = pygame.font.Font(None, 36)
        confirmation_text = font.render(f"  Do you want to sell this building for {Building.cost} money?  ", True, (0, 0, 0))
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
                        self.money += Building.cost
                        return True
                    elif no_button_rect.collidepoint(mouse_pos):
                        return False
  
    def sell_multiple_buildings(self, Building_grid):
        total_cost = 0
        for Building in Building_grid:
                if Building is not None:
                    total_cost += Building.cost
        
        font = pygame.font.Font(None, 36)
        confirmation_text = font.render(f"  Do you want to sell these buildings for {total_cost} money?  ", True, (0, 0, 0))
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
                        self.money += total_cost
                        return True
                    elif no_button_rect.collidepoint(mouse_pos):
                        return False

# EnergyGenerator class
class EnergyGenerator:
    def __init__(self, tier):
        self.cost = 300*tier*(1 if tier == 1 else 4)
        self.heat_per_tick = 5/60*tier*(1 if tier == 1 else 4)
        self.tier = tier
    def generate_heat(self):
        return self.heat_per_tick
    
    def upgrade(self):
        if self.tier < 8:
            self.tier += 1

class EnergyConverter:
    def __init__(self,tier):
        self.cost = 200*tier*(1 if tier == 1 else 4)
        self.energy_per_heat = 2 * tier*(1 if tier == 1 else 4)
        self.tier = tier
    def convert_heat(self, heat):
        return heat * self.energy_per_heat
    
    def upgrade(self):
        if self.tier < 8:
            self.tier += 1
    

class Office:
    def __init__(self,tier):
        self.energy_sell_rate = 5*tier*(1 if tier == 1 else 4)  # Energy selling rate for the office (per second)
        self.cost = 500*tier*(4 if tier != 1 else 1)
        self.tier = tier
    def sell_energy(self, player):
        # Sell energy at the defined rate
        if player.energy >= self.energy_sell_rate:
            player.energy -= self.energy_sell_rate 
            player.money += self.energy_sell_rate  # Assuming 1 energy = 10 money
    def upgrade(self):
        if self.tier < 8:
            self.tier += 1
            
class Button():
    def __init__(self, x, y, width, height, text='', command=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 22)
        self.command = command

    def draw(self, surface):
        pygame.draw.rect(surface,(0, 80, 200), self.rect)
        if self.text:
            text = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.command:
                self.command()
                
    def button_update(self, text=''):
        self.text = text
            
def switch_view(state, tier):
    labels = ["Converter", "Generator", "Office"]
    if state == "Buy":
        # testbutton.button_update("Buy Converter")
        items = [
            EnergyConverter(tier),
            EnergyGenerator(tier),
            Office(tier)
        ]

        for i, item in enumerate(items):
            # price = item.cost * (2 if state == "Upgrade" else 1)
            price = item.cost
            label_text = font.render(f'Tier {tier} {labels[i]} (${price})', True, (0, 0, 0))
            window.blit(label_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, i * SIDEBAR_ITEM_HEIGHT + 10))
        
    elif state == "Upgrade":

        #create a button for each upgrade
        # testbutton.button_update("Upgrade Converter")
        label_text = font.render(f'Upgrade Converter{CONVERTER_UPGRADE}(${1000*CONVERTER_UPGRADE*4})\n Upgrade heat generation by %50', True, (0, 0, 0))
        window.blit(label_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10,  SIDEBAR_ITEM_HEIGHT -40 ))
        label_text = font.render(f'Upgrade Generator{GENERATOR_UPGRADE}(${1000*GENERATOR_UPGRADE*4})\n Upgrade heat generation by %50', True, (0, 0, 0))
        window.blit(label_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 2 * SIDEBAR_ITEM_HEIGHT -40))
        label_text = font.render(f'Upgrade Office{OFFICE_UPGRADE}(${1000*OFFICE_UPGRADE*4}) Upgrade heat generation by %50', True, (0, 0, 0))
        window.blit(label_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 3 * SIDEBAR_ITEM_HEIGHT -40))
    

    
def display_sidebar(tier, page):
    print("display_sidebar")
    # labels = ["Converter", "Generator", "Office"]
    # prices = TIER_PRICES.get(tier, [])  # Get prices for the current tier and page

    # for i in range(len(labels)):
    #     label_text = font.render(f'Tier {page} {labels[i]} (${prices[page-1][i]})', True, (0, 0, 0))
    #     window.blit(label_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, i * SIDEBAR_ITEM_HEIGHT + 10))
       
    # convert_button = font.render(f'Convert Energy To Money', True, (0, 0, 0), (125, 255, 125)) 
    # window.blit(convert_button, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 160))

    # # Display page switch buttons
    # button_text = font.render(f'Page {page}', True, (0, 0, 0), (200, 200, 200))
    # window.blit(button_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 120))

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
HIGHLIGHT_COLOR = (255, 0, 0, 128)  # Red with 50% opacity

# Tile types
TILE_EMPTY = 0
TILE_CONVERTER = 1
TILE_GENERATOR = 2
TILE_OFFICE = 3

#Upgrade Stats
CONVERTER_UPGRADE = 1
GENERATOR_UPGRADE = 1
OFFICE_UPGRADE = 1


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
# WINDOW_HEIGHT = NUM_TILES_Y * TILE_SIZE +50
WINDOW_HEIGHT = NUM_TILES_Y * TILE_SIZE 
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
# energy_generator = EnergyGenerator(1)  # Slower energy generation
# energy_converter = EnergyConverter(1)  # More efficient conversion
# office = Office(1)
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


# Load building images
generator_images = {
 
    1 : pygame.transform.scale(pygame.image.load('Data/generatorfull.png'), (50, 50)),
    2 : pygame.transform.scale(pygame.image.load('Data/generator2full.png'), (50, 50)),
    3 : pygame.transform.scale(pygame.image.load('Data/generator3full.png'), (50, 50))
}

converter_images = {
    1: pygame.transform.scale(pygame.image.load('Data/windmill.png'), (50, 50)),
    2: pygame.transform.scale(pygame.image.load('Data/solarpanelfull.png'), (50, 50)),
    3: pygame.transform.scale(pygame.image.load('Data/coalfactory.png'), (50, 50))
}

office_images = {
    1: pygame.transform.scale(pygame.image.load('Data/officefull.png'), (50, 50)),
    2: pygame.transform.scale(pygame.image.load('Data/office2.png'), (50, 50)),
    3: pygame.transform.scale(pygame.image.load('Data/office3.png'), (50, 50))
}



# Game loop
running = True
selected_building = None  # Selected building type (None, CONVERTER, GENERATOR, OFFICE)



current_tier = 1




#DEFINE BUTTONS
buy_button1 = Button(815, 295, 100, 30, 'Buy', lambda: print('Button clicked'))
upgrade_button1 = Button(1100, 295, 100, 30, 'Upgrade', lambda: print('Button clicked'))
forward_button = Button(1100, 255, 100, 30, '>>', lambda: print('Button clicked'))
previous_button = Button(815, 255, 100, 30, '<<', lambda: print('Button clicked'))
testbutton = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, SIDEBAR_ITEM_HEIGHT , 100, 30, 'Buy')
delete_multiple_button = Button(961, 295 , 100, 30, 'X')
print_multiple_button = Button(961, 255 , 100, 30, 'Print')


state = "Buy"

switch_view("Buy",current_tier)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // TILE_SIZE
            grid_y = mouse_pos[1] // TILE_SIZE
            if event.button == 1:  # Left click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Clicked ", mouse_x//TILE_SIZE, mouse_y//TILE_SIZE)
                # if testbutton.rect.collidepoint(mouse_pos):
                #     print("test")
                if print_multiple_button.rect.collidepoint(mouse_pos):
                    print(grid)
                elif previous_button.rect.collidepoint(mouse_pos) and current_tier > 1:
                    current_tier -=1
                    
                elif forward_button.rect.collidepoint(mouse_pos) and current_tier < 8:
                    current_tier +=1

                elif buy_button1.rect.collidepoint(mouse_pos):
                    state = "Buy"
                    print("Buy button clicked")
                elif upgrade_button1.rect.collidepoint(mouse_pos):
                    state = "Upgrade"
                    print("upgrade button clicked")
                    
                elif delete_multiple_button.rect.collidepoint(mouse_pos):
                    # Enter delete multiple mode
                    selected_tiles = []
                    x_of_building =[]
                    y_of_building =[]
                    delete_multiple_mode = True
                    while delete_multiple_mode:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                delete_multiple_mode = False
                            elif event.type == pygame.MOUSEBUTTONDOWN:

                                if event.button == 1 and grid[grid_x][grid_y] != TILE_EMPTY:  # Left click
                                    if (grid[grid_x][grid_y]) not in selected_tiles:
                                        x_of_building.append(grid_x)
                                        print(grid_x, grid_y)
                                        y_of_building.append(grid_y)
                                        selected_tiles.append((grid[grid_x][grid_y]))
                                        rect = pygame.Rect(grid_x * TILE_SIZE, grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                                        pygame.draw.rect(window, HIGHLIGHT_COLOR, rect, 2) # the last parameter is the thickness of the border
                                        pygame.display.flip()

                                elif event.button == 3:  # Right click
                                    # Cancel selection
                                    delete_multiple_mode = False
                    if(player.sell_multiple_buildings(selected_tiles)):
                        print(selected_tiles)
                        for i in range(len(selected_tiles)):
                            grid[x_of_building[i]][y_of_building[i]] = TILE_EMPTY
                            
                            
                            


                            
                elif WINDOW_WIDTH - SIDEBAR_WIDTH <= mouse_pos[0] < WINDOW_WIDTH and state == "Buy":
                    selected_building = (mouse_pos[1] // SIDEBAR_ITEM_HEIGHT) + 1
                    print("Selected building: ", selected_building)
                    building_tier = current_tier
                elif WINDOW_WIDTH - SIDEBAR_WIDTH <= mouse_pos[0] < WINDOW_WIDTH and state == "Upgrade":
                    if(((mouse_pos[1] // SIDEBAR_ITEM_HEIGHT) + 1) == 1):
                         #need upgrade method
                        print("Converter Upgraded")
                    elif(((mouse_pos[1] // SIDEBAR_ITEM_HEIGHT) + 1) == 2):
                         #need upgrade method
                        print("Generator Upgraded")
                    elif(((mouse_pos[1] // SIDEBAR_ITEM_HEIGHT) + 1) == 3): 
                        #need upgrade method
                        print("Office Upgraded")
                    
                elif WINDOW_WIDTH - SIDEBAR_WIDTH + 10 <= mouse_pos[0] < WINDOW_WIDTH - SIDEBAR_WIDTH + 290 and WINDOW_HEIGHT - 160 <= mouse_pos[1] < WINDOW_HEIGHT - 110:
                        # Convert energy to money
                        player.sell_energy(player.energy)  # Sell all available energy
                        # Update money display after successful conversion
                        money_text = font.render(f'Money: {int(player.money)}', True, (0, 0, 0))
                elif grid[grid_x][grid_y] == TILE_EMPTY:
                    # Place selected building on the grid
                    grid_x = mouse_pos[0] // TILE_SIZE
                    grid_y = mouse_pos[1] // TILE_SIZE
                    if 0 <= grid_x < NUM_TILES_X and 0 <= grid_y < NUM_TILES_Y:
                        if selected_building == 1 and player.buy_energy_generator(EnergyConverter(current_tier)):
                            print("Converter bought")
                            grid[grid_x][grid_y] = EnergyConverter(current_tier)
                        elif selected_building == 2 and player.buy_energy_generator(EnergyGenerator(current_tier)):
                            print("Generator bought")
                            grid[grid_x][grid_y] = EnergyGenerator(current_tier)
                        elif selected_building == 3 and player.buy_energy_generator(Office(current_tier)):
                            print("Office bought")
                            grid[grid_x][grid_y] = Office(current_tier)
            elif event.button == 3:  # Right click
                # Sell selected building on the grid

                if 0 <= grid_x < NUM_TILES_X and 0 <= grid_y < NUM_TILES_Y:
                    if isinstance(grid[grid_x][grid_y], EnergyConverter):
                        if(player.sell_building(grid[grid_x][grid_y])):
                            grid[grid_x][grid_y] = TILE_EMPTY
                    elif isinstance(grid[grid_x][grid_y], EnergyGenerator):
                        if(player.sell_building(grid[grid_x][grid_y])):
                            grid[grid_x][grid_y] = TILE_EMPTY
                    elif isinstance(grid[grid_x][grid_y], Office):
                        if(player.sell_building(grid[grid_x][grid_y])):
                            grid[grid_x][grid_y] = TILE_EMPTY


               
  
    font = pygame.font.Font(None, 24)


    #draw
    window.fill(GRAY)

    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))   
    switch_view(state,current_tier)
    # display_sidebar(current_tier, current_page)

    # Update game logic

    # Generate heat from generators
    total_heat_generated = 0
    for i in range(NUM_TILES_X):
        for j in range(NUM_TILES_Y):
            if isinstance(grid[i][j], EnergyGenerator):
                # Generate heat in adjacent tiles
                for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                        if 0 <= x < NUM_TILES_X and 0 <= y < NUM_TILES_Y and not (x == i and y == j):
                            heat_grid[x][y] += grid[i][j].generate_heat()
                            total_heat_generated += grid[i][j].generate_heat()

    # Convert heat to energy using converters
    total_energy = 0
    for i in range(NUM_TILES_X):
        for j in range(NUM_TILES_Y):
            if isinstance(grid[i][j], EnergyConverter):
                total_energy += grid[i][j].convert_heat(heat_grid[i][j])
                heat_grid[i][j] = 0  # Reset heat in the converter tile

    player.generate_energy(total_energy)

    # Calculate energy generation rate
    energy_generation_rate = total_energy * FPS

    # Sell energy using the office
    total_energy_sold = 0
    for i in range(NUM_TILES_X):
        for j in range(NUM_TILES_Y):
            if isinstance(grid[i][j], Office):
                grid[i][j].sell_energy(player)
                total_energy_sold += grid[i][j].energy_sell_rate

    # Display game information
    
    

    tile_image = pygame.transform.scale(pygame.image.load('Data/tile2.jpg'), (50, 50))
    
   # Draw tiles and objects
    for i in range(NUM_TILES_X):
        for j in range(NUM_TILES_Y):
            rect = pygame.Rect(i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if isinstance(grid[i][j], EnergyConverter):
                window.blit(converter_images[grid[i][j].tier], rect)
            elif isinstance(grid[i][j], EnergyGenerator):
                window.blit(generator_images[grid[i][j].tier], rect)
            elif isinstance(grid[i][j], Office):
                window.blit(office_images[grid[i][j].tier], rect)
            else:
                window.blit(tile_image, rect)
                # pygame.draw.rect(window, WHITE, rect, 1)


        
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
    # window.blit(bottom_bar, (0, WINDOW_HEIGHT - 50))

    #DRAW BUTTONS
    buy_button1.draw(window)
    upgrade_button1.draw(window)
    forward_button.draw(window)
    previous_button.draw(window) 
    delete_multiple_button.draw(window)
    print_multiple_button.draw(window)
    # testbutton.draw(window)
  

    # Check if mouse is hovering over a placed building
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pos = pygame.mouse.get_pos()
    test = font.render(f'Coordinates: {mouse_x,mouse_y}', True, (0, 0, 0))
    window.blit(test,( mouse_pos[0], mouse_pos[1]))
    grid_x = mouse_pos[0] // TILE_SIZE
    grid_y = mouse_pos[1] // TILE_SIZE
    if 0 <= grid_x < NUM_TILES_X and 0 <= grid_y < NUM_TILES_Y:
        if isinstance(grid[grid_x][grid_y], EnergyConverter):
            info_text = font.render(f'Energy per heat: {grid[grid_x][grid_y].energy_per_heat}', True, (0, 0, 0))
            window.blit(info_text, (mouse_pos[0] + 10, mouse_pos[1] + 10))
        elif isinstance(grid[grid_x][grid_y], EnergyGenerator):
            info_text = font.render(f'Heat per tick: {grid[grid_x][grid_y].heat_per_tick}', True, (0, 0, 0))
            window.blit(info_text, (mouse_pos[0] + 10, mouse_pos[1] + 10))
        elif isinstance(grid[grid_x][grid_y], Office):
            info_text = font.render(f'Energy sell rate: {grid[grid_x][grid_y].energy_sell_rate * 60:.2f} per second tier {grid[grid_x][grid_y].tier}', True, (255, 255, 255))
            info_bg = pygame.Surface((info_text.get_width()+20, info_text.get_height()+20))
            info_bg.fill((0, 0, 0))
            info_bg.blit(info_text, (10, 10))
            info_bg.set_alpha(150)
            window.blit(info_bg, (mouse_pos[0] + 10, mouse_pos[1] + 10))
    
    

    # Update the screen
    pygame.display.flip()
    clock.tick(FPS)

# Quit pygame
pygame.quit()