import pygame
import threading


# Player class
class Player:
    def __init__(self):
        self.energy = 0
        self.money = 1000000
        self.research = 111110
        self.max_energy = 200

    def buy_energy_generator(self, Building):
        if self.money >= Building.cost:
            self.money -= Building.cost
            return True
        return False




    def buy_research(self, cost):
        if self.research >= cost:
            self.research -= cost
            return True
        return False
    
    def buy_upgrade(self, cost):
        if self.money >= cost:
            self.money -= cost
            return True
        return False

    def generate_energy(self, amount):
        if self.energy + amount <= self.max_energy:
            self.energy += amount
        else :
            self.energy = self.max_energy

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
        confirmation_text = font.render(f"  Do you want to sell these buildings for {(total_cost if total_cost != None else None)} money?  ", True, (0, 0, 0))
        yes_text = font.render("Yes", True, (0, 0, 0))
        no_text = font.render("No", True, (0, 0, 0))
      
      
      
      
        if(confirmation_window(confirmation_text,yes_text,no_text)):
            self.money += total_cost
            return True
        else:
            return False

# HeatGenerator class
class HeatGenerator:
    def __init__(self, tier,upgrade):
        self.cost = 1000 * (4 ** (tier - 1)) * (tier - 1) + (10 if tier == 1 else 0)
        self.heat_per_tick = 1*tier*upgrade*1.50/120 *(100 ** (tier - 1))
        self.life_cycle = 600
        self.tier = tier
        
        
        
    def generate_heat(self):
        
        
        if self.life_cycle == 0:
            handle_destruction(self)
            
            return 0
        
        if (self.tier > 1):
            self.life_cycle -=1
            return self.heat_per_tick
        else:

            player.generate_energy(self.heat_per_tick)
            self.life_cycle -=1
            return 0
            

class EnergyConverter:
    def __init__(self, tier, upgrade):
        self.cost = 2000 * (4 ** (tier - 1)) 
        self.tier = tier

        self.max_heat = 10*tier*upgrade*2*(100 ** (tier - 1))
        self.heat_conversion_per_second = 1*tier*upgrade*1.25*(100 ** (tier - 1))
        self.stored_heat = 0


    def convert_heat(self, heat):

        if heat <= self.heat_conversion_per_second:
          player.generate_energy(heat)

        else:
            if self.stored_heat + heat < self.max_heat:
                player.generate_energy(heat)
                self.stored_heat += heat
            else:
                handle_destruction(self)
        



class Office:
    def __init__(self,tier,upgrade):
        self.energy_sell_rate = 1*tier*upgrade*1.5 *(100 ** (tier - 1)) # Energy selling rate for the office (per second)
        self.cost = 10000 * (4 ** (tier - 1)) 
        self.tier = tier
    def sell_energy(self, player):
        # Sell energy at the defined rate
        if player.energy >= self.energy_sell_rate:
            player.energy -= self.energy_sell_rate 
            player.money += self.energy_sell_rate  # Assuming 1 energy = 10 money
        elif player.energy > 0:
            player.money += player.energy *2
            player.energy = 0

class ResearchLab:
    def __init__(self,tier,upgrade):
        self.research_rate = 1*tier*upgrade*1.5  *(100 ** (tier - 1))
        self.cost = 50000 * (4 ** (tier - 1))  
        self.tier = tier
    def research(self, player):
            player.research += self.research_rate/60

            
class Button():
    def __init__(self, x, y, width,height, text='', command=None, color=(0,80,200), image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 22)
        self.command = command
        self.color = color
        self.image = image
        self.width = width
        self.height = height

        
    def draw(self, surface):
            pygame.draw.rect(surface,self.color, self.rect)
            if self.text and not self.image:
                text = self.font.render(self.text, True, (255, 255, 255))
                text_rect = text.get_rect(center=self.rect.center)
                surface.blit(text, text_rect)
            elif self.text and self.image :
                text = self.font.render(self.text, True, (255, 255, 255))
                new_surface = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
                new_surface.blit(self.image, (5, 5))
                new_surface.blit(text, (self.image.get_width()+20, 16))
                pygame.draw.rect(new_surface, (0, 0, 0), (0, 0, self.width,self.height), 1)
                surface.blit(new_surface, (self.rect.x, self.rect.y))
                self.rect.move_ip(0, scroll_offset)

                
                
                
                
            # elif self.text and self.image and self.scrollarea != None:
            #     text = self.font.render(self.text, True, (255, 255, 255))
            #     new_surface = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
            #     new_surface.blit(self.image, (5, 5))
            #     new_surface.blit(text, (self.image.get_width()+20, 16))
            #     pygame.draw.rect(new_surface, (0, 0, 0), (0, 0, self.width,self.height), 1)
            #     scroll_bar.blit(new_surface, (0, 0))
            #     surface.blit(scroll_bar, (self.rect.x, self.rect.y))

                
            

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.command:
                self.command()
                
    def button_update(self, text=None, image=None):
        if (text != None and image == None):
            self.text = text
        elif (text == None and image != None):
            self.image = image
        elif (text != None and image != None):
            self.text = text
            self.image = image
            
            
            
    
def handle_destruction(building):
    for i in range(NUM_TILES_X):
        for j in range(NUM_TILES_Y):
            if grid[i][j] == building:
                grid[i][j] = TILE_EMPTY
                x = i * TILE_SIZE
                y = j * TILE_SIZE
                explosion_delay = 100
                last_explosion_time = pygame.time.get_ticks()
                explosion_frame = 1


                while explosion_frame < len(explosion_images):
                    now = pygame.time.get_ticks()
                    if now - last_explosion_time > explosion_delay:
                        explosion_frame += 1
                        last_explosion_time = now
                    explosion_image = explosion_images[explosion_frame].convert_alpha()

                    window.blit(explosion_image, (x, y))
                    pygame.display.update(x,y,TILE_SIZE,TILE_SIZE)
                return 0
     
# def render_grid_movement(grid):    
#     for row in range(len(grid)):
#         for col in range(len(grid[0])):
#             cell_value = grid[row][col]
#             x = col * TILE_SIZE - camera_x
#             y = row * TILE_SIZE - camera_y
#             pygame.draw.rect(window, (255, 255, 255), (x, y, TILE_SIZE, TILE_SIZE), 1)

def confirmation_window(confirmation_text,yes_text=None,no_text=None):    
        
        
        
    confirmation_rect = confirmation_text.get_rect(center=(WINDOW_WIDTH // 2+10, WINDOW_HEIGHT // 2+10))
    confirmation_rect.inflate_ip(0, 5) # increase the size of the rectangle by 50 pixels in both directions
    
    # Draw the confirmation box
    pygame.draw.rect(window, (200, 200, 200), confirmation_rect)
    pygame.draw.rect(window, (0, 0, 0), confirmation_rect, 2)
    window.blit(confirmation_text, confirmation_rect)
    
    if  yes_text != None and no_text == None:
        yes_button_rect = pygame.Rect(WINDOW_WIDTH // 2 -25, WINDOW_HEIGHT // 2 +25, 80, 35)
        pygame.draw.rect(window, (0, 255, 0), yes_button_rect)
        window.blit(yes_text, (yes_button_rect.x + 20, yes_button_rect.y + 8))
    elif yes_text != None:
        yes_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT // 2 + 40, 60, 40)
        pygame.draw.rect(window, (0, 255, 0), yes_button_rect)
        window.blit(yes_text, (yes_button_rect.x + 10, yes_button_rect.y + 5))

    if no_text != None:
        no_button_rect = pygame.Rect(WINDOW_WIDTH // 2 + 20, WINDOW_HEIGHT // 2 + 40, 60, 40)
        pygame.draw.rect(window, (255, 0, 0), no_button_rect)
        window.blit(no_text, (no_button_rect.x + 15, no_button_rect.y + 5))

    
    
    # yes_text = font.render("Yes", True, (0, 0, 0))
    # no_text = font.render("No", True, (0, 0, 0))
    

    
    pygame.display.flip()  

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_button_rect.collidepoint(mouse_pos):
                    return True
                elif no_button_rect.collidepoint(mouse_pos):
                    return False
            
def switch_view(state, tier):
    label_list = ["Heat Generator", "Energy Converter", "Office", "Research Lab"]
    building_list = [HeatGenerator,EnergyConverter,  Office, ResearchLab]
    upgrade_list = [ GENERATOR_UPGRADE,CONVERTER_UPGRADE, OFFICE_UPGRADE, RESEARCHLAB_UPGRADE]
    image_list = [generator_menu_images,converter_menu_images,  office_menu_images, researchlab_menu_images]
    
    if state == "Buy":
    
        
        for i in range(4):
            menu_button_list[i].button_update(f'Tier {tier} {label_list[i]}(${building_list[i](tier,upgrade_list[i]).cost})' ,image_list[i][tier])
                                                                        
        
    elif state == "Upgrade":
        upgrades = {
        "Generator": ("Upgrade heat generation by %50", 50*(2**GENERATOR_UPGRADE)),
        "Converter": ("Upgrade heat to energy conversion by %25", 50*(2**CONVERTER_UPGRADE)),
        "Office": ("Upgrade energy to money conversion by %50", 50*(2**OFFICE_UPGRADE)),
        "ResearchLab": ("Upgrade research rate by %50 ", 50*(2**RESEARCHLAB_UPGRADE))
    }

      
        i=0       
        for upgrade in upgrades:
            menu_button_list[i].button_update(f' {upgrades[upgrade][0]} (${upgrades[upgrade][1]})')
            i+=1
                                                                        

    elif state == "Research":

        Labels = ["Heat Generator", "Energy Converter", "Office", "Research Lab"]
        
           
            
        for i in range(len(Researches)):

            if tier == 1 and Researches[i+1][0] == False:
                menu_button_list[i].button_update(f'Unlock Tier {(current_tier+1 if current_tier < 3 else 3)} {Labels[i]} ({Researches[i+1][2]*(1 if current_tier < 2 else 10) } Research)',image_list[i][(tier+1 if tier < 3 else 3)])
            elif tier == 2 and Researches[i+1][1] == False:
                menu_button_list[i].button_update(f'Unlock Tier {(current_tier+1 if current_tier < 3 else 3)} {Labels[i]} ({Researches[i+1][2]*(1 if current_tier < 2 else 10) } Research)',image_list[i][(tier+1 if tier < 3 else 3)])
            else:
                menu_button_list[i].button_update(f'Research Bought!')
            
                

    

        # for i in Researches:
        #     if Researches[i][0] == False:
        #         label_text = font.render(f'Unlock Tier {(current_tier+1 if current_tier < 3 else 3)} {Labels[i-1]} ({Researches[i][1]*(1 if current_tier < 2 else 10) } Research)', True, (0, 0, 0))
        #         window.blit(label_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, i* SIDEBAR_ITEM_HEIGHT -40 ))
        #     else:
        #         label_text = font.render(f'Research Bought!', True, (0, 0, 0))
        #         window.blit(label_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, i* SIDEBAR_ITEM_HEIGHT -40 ))
                
          
    energy_gen_thread = threading.Thread(target=energy_gen)
    energy_gen_thread.start()

# Create two threads
 
def energy_gen():
    if grid != None:
        for i in range(NUM_TILES_X):
            for j in range(NUM_TILES_Y):
                if isinstance(grid[i][j], HeatGenerator) and grid[i][j].tier != 1:
                    # Generate heat in adjacent tiles
                    if i+1 < NUM_TILES_X and isinstance(grid[i+1][j], EnergyConverter):
                        grid[i+1][j].convert_heat(grid[i][j].generate_heat())
                    if i-1 >= 0 and isinstance(grid[i-1][j], EnergyConverter):
                        grid[i-1][j].convert_heat(grid[i][j].generate_heat())
                    if j+1 < NUM_TILES_Y and isinstance(grid[i][j+1], EnergyConverter):
                        grid[i][j+1].convert_heat(grid[i][j].generate_heat())
                    if  j-1 >= 0 and isinstance(grid[i][j-1], EnergyConverter):
                        grid[i][j-1].convert_heat(grid[i][j].generate_heat())
                elif isinstance(grid[i][j], HeatGenerator) and grid[i][j].tier == 1 :
                    grid[i][j].generate_heat()


#     energy_gen_thread = threading.Thread(target=refresh_display)
#     energy_gen_thread.start()
# def refresh_display():
#     pygame.display.flip()


def research_check(building,tier):
    if tier == 2:
        if Researches[building][0] == True:
            return True
        else: 
            return False
    elif tier == 3: 
        if Researches[building][1] == True:
            return True
        else: 
            return False
    else:
        return True

    
    
    
def delete_mult():
                     
    selected_tiles = []
    x_of_building =[]
    y_of_building =[]
    delete_multiple_mode = True
    font1 = pygame.font.Font(None, 26)
    label_text = font1.render('Select Buildings To Sell, Right Click To Sell Or Cancel', True, (255, 0, 0), (0, 0, 0))
    window.blit(label_text, ((WINDOW_WIDTH - SIDEBAR_WIDTH)/5 , 8* SIDEBAR_ITEM_HEIGHT -10 ))
    pygame.display.flip()

    while delete_multiple_mode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                delete_multiple_mode = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                grid_x = mouse_pos[0] // TILE_SIZE
                grid_y = mouse_pos[1] // TILE_SIZE
                if event.button == 1 and (0 <= grid_x < NUM_TILES_X and 0 <= grid_y < NUM_TILES_Y) and grid[grid_x][grid_y] != TILE_EMPTY:  # Left click
                    if (grid[grid_x][grid_y] not in selected_tiles):
                        x_of_building.append(grid_x)
                        print(grid_x, grid_y)
                        y_of_building.append(grid_y)
                        selected_tiles.append((grid[grid_x][grid_y]))
                        rect = pygame.Rect(grid_x * TILE_SIZE, grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(window, HIGHLIGHT_COLOR, rect, 2) # the last parameter is the thickness of the border
                        pygame.display.flip()
                        # pygame.display.update(rect)


                elif event.button == 3:  # Right click
                    # Cancel selection
                    delete_multiple_mode = False
    if(selected_tiles != [] and player.sell_multiple_buildings(selected_tiles)):
        print(selected_tiles)
        for i in range(len(selected_tiles)):
            grid[x_of_building[i]][y_of_building[i]] = TILE_EMPTY
                            

# complicated because of objects
# def load_grid(filename):
#     try:
#         with open(filename, 'r') as f:
#             for i in range(NUM_TILES_X):
#                 for j in range(NUM_TILES_Y):
#                     grid[i][j] = f[i][j]
#     except FileNotFoundError:
#         print("File not found")
#         return None

# def save_grid(filename):  
#     for i in range(NUM_TILES_X):
#         for j in range(NUM_TILES_Y):
#             if isinstance(grid[i][j], HeatGenerator):
#                 grid[i][j] = 1
#             elif isinstance(grid[i][j], EnergyConverter):
#                 grid[i][j] = 2
#             elif isinstance(grid[i][j], Office):
#                 grid[i][j] = 3
#             else:
#                 grid[i][j] = 0
#     with open(filename, 'w') as f:
#         json.dump(grid, f)
     



# load_grid("save.json")



# Tile constants
TILE_SIZE = 50
# NUM_TILES_X = 16  # Adjusted for the grid size
NUM_TILES_X = 16
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
TILE_ResearchLab = 4

#Upgrade Stats
CONVERTER_UPGRADE = 1
GENERATOR_UPGRADE = 1
OFFICE_UPGRADE = 1
RESEARCHLAB_UPGRADE = 1


# Object prices
CONVERTER_PRICE = 200
GENERATOR_PRICE = 300
OFFICE_PRICE = 500
RESEARCHLAB_PRICE = 1000

# Energy production rates for each building type
ENERGY_RATE_CONVERTER = 2/60
ENERGY_RATE_GENERATOR = 5/60

# Initialize pygame
pygame.init()

# Initialize the window
WINDOW_WIDTH = NUM_TILES_X * TILE_SIZE + SIDEBAR_WIDTH
# WINDOW_HEIGHT = NUM_TILES_Y * TILE_SIZE +50
WINDOW_HEIGHT = NUM_TILES_Y * TILE_SIZE  
# WINDOW_HEIGHT = 1080
# WINDOW_WIDTH = 1920
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
# energy_generator = HeatGenerator(1)  # Slower energy generation
# energy_converter = EnergyConverter(1)  # More efficient conversion
# office = Office(1)
heat_grid = [[0 for _ in range(NUM_TILES_Y)] for _ in range(NUM_TILES_X)]  # Heat grid for generators

# Initialize the grid with empty tiles
grid = [[TILE_EMPTY for _ in range(NUM_TILES_Y)] for _ in range(NUM_TILES_X)]
converters= []
generators = []
offices = []
labs = []


# Sample prices for different tiers (you should replace these with your actual prices)
TIER_PRICES = {
    1: [[10, 20, 30], [40, 50, 60]],  # Prices for tier 1 for pages 1 and 2
    2: [[50, 60, 70], [80, 90, 100]]   # Prices for tier 2 for pages 1 and 2 (example)
}


Researches = {
    1: (False,False ,1000),
    2 : (False,False ,1000),
    3: (False,False ,1000),
    4: (False,False ,1000)
}
    


# Load building images
generator_images = {
 
    1: pygame.transform.scale(pygame.image.load('Data/windmill.png'), (50,50)),
    2: pygame.transform.scale(pygame.image.load('Data/solarpanelfull.png'), (50,50)),
    3: pygame.transform.scale(pygame.image.load('Data/coalfactory.png'), (50,50))
}

converter_images = {
    1 : pygame.transform.scale(pygame.image.load('Data/generatorfull.png'), (50,50)),
    2 : pygame.transform.scale(pygame.image.load('Data/generator2full.png'), (50,50)),
    3 : pygame.transform.scale(pygame.image.load('Data/generator3full.png'), (50,50)),
    4 : pygame.transform.scale(pygame.image.load('Data/generator4full.png'), (50,50)),
    5 : pygame.transform.scale(pygame.image.load('Data/generator5full.png'), (50,50)),
    6 : pygame.transform.scale(pygame.image.load('Data/generator6full.png'), (50,50))
}

office_images = {
    1: pygame.transform.scale(pygame.image.load('Data/officefull.png'), (50,50)),
    2: pygame.transform.scale(pygame.image.load('Data/office2.png'), (50,50)),
    3: pygame.transform.scale(pygame.image.load('Data/office3.png'), (50,50))
}

researchlab_images = {
    1: pygame.transform.scale(pygame.image.load('Data/research1full.png'), (50,50)),
    2: pygame.transform.scale(pygame.image.load('Data/research2full.png'), (50,50)),
    3: pygame.transform.scale(pygame.image.load('Data/research3full.png'), (50,50))
}

converter_menu_images = {
    1: pygame.transform.scale(pygame.image.load('Data/generator1.png'), (40, 40)),
    2: pygame.transform.scale(pygame.image.load('Data/generator2fullmenu.png'), (40, 40)),
    3: pygame.transform.scale(pygame.image.load('Data/generator3fullmenu.png'), (40, 40))

    
}
generator_menu_images = {
 
    1 : pygame.transform.scale(pygame.image.load('Data/windmill_menu.png'), (40, 40)),
    2 : pygame.transform.scale(pygame.image.load('Data/convertermenu.png'), (40, 40)),
    3 : pygame.transform.scale(pygame.image.load('Data/coalfactorymenu.png'), (40, 40))
}
office_menu_images = {
 
    1 : pygame.transform.scale(pygame.image.load('Data/office.png'), (40, 40)),
    2 : pygame.transform.scale(pygame.image.load('Data/office2menu.png'), (40, 40)),
    3 : pygame.transform.scale(pygame.image.load('Data/office3menu.png'), (40, 40))
}
researchlab_menu_images = {
 
    1 : pygame.transform.scale(pygame.image.load('Data/research1.png'), (40, 40)),
    2 : pygame.transform.scale(pygame.image.load('Data/research2.png'), (40, 40)),
    3 : pygame.transform.scale(pygame.image.load('Data/research3.png'), (40, 40))
}

explosion_images = {
    1 : pygame.transform.scale(pygame.image.load('Data/explosion1.png'), (50,50)),
    2 : pygame.transform.scale(pygame.image.load('Data/explosion2.png'), (50,50)),
    3 : pygame.transform.scale(pygame.image.load('Data/explosion3.png'), (50,50)),
    4 : pygame.transform.scale(pygame.image.load('Data/explosion4.png'), (50,50)),
    5 : pygame.transform.scale(pygame.image.load('Data/explosion5_scuffed.png'), (50,50)),
    6 : pygame.transform.scale(pygame.image.load('Data/explosion6.png'), (50,50)),
    7 : pygame.transform.scale(pygame.image.load('Data/explosion7.png'), (50,50))
}
battery_image = pygame.transform.scale(pygame.image.load('Data/batterymenu.png'), (40,40))

# Game loop
running = True
selected_building = None  # Selected building type (None, CONVERTER, GENERATOR, OFFICE)



current_tier = 1

not_researched_text = font.render(f'   Not Researched    ', True, (0, 0, 0))
ok_text = font.render(f'Ok', True, (0, 0, 0))



#DEFINE BUTTONS
buy_button1 = Button(WINDOW_WIDTH - SIDEBAR_WIDTH +15,7* SIDEBAR_ITEM_HEIGHT -55, 100, 30, 'Buy', lambda: print('Button clicked'))
upgrade_button1 = Button(WINDOW_WIDTH - SIDEBAR_WIDTH +300, 7* SIDEBAR_ITEM_HEIGHT -55, 100, 30, 'Upgrade', lambda: print('Button clicked'))
forward_button = Button(WINDOW_WIDTH - SIDEBAR_WIDTH +300, 6* SIDEBAR_ITEM_HEIGHT -45, 100, 30, '>>', lambda: print('Button clicked'))
previous_button = Button(WINDOW_WIDTH - SIDEBAR_WIDTH +15, 6* SIDEBAR_ITEM_HEIGHT -45, 100, 30, '<<', lambda: print('Button clicked'))
testbutton = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, SIDEBAR_ITEM_HEIGHT , 100, 30, 'Buy')
delete_multiple_button = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 161, 7* SIDEBAR_ITEM_HEIGHT -55 , 100, 30, 'X')
research_button = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 161, 6* SIDEBAR_ITEM_HEIGHT -45, 100, 30, 'Research')
convert_button = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 200, 200 , 30, 'Convert Energy To Money', lambda: print('Button clicked'),(125, 200, 125))
menu_button1  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 1 * SIDEBAR_ITEM_HEIGHT - 40, 450, 50)
menu_button2  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 2 * SIDEBAR_ITEM_HEIGHT - 40, 450, 50)
menu_button3  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 3 * SIDEBAR_ITEM_HEIGHT - 40, 450, 50)
menu_button4  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 4 * SIDEBAR_ITEM_HEIGHT - 40, 450, 50)
menu_button5  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 5 * SIDEBAR_ITEM_HEIGHT - 40, 450, 50, "Tier 1 Battery", lambda: print('Button clicked'),(0,80,200),battery_image)
# menu_button5  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 6 * SIDEBAR_ITEM_HEIGHT - 40, 450, 50)




scroll_bar = pygame.Surface((WINDOW_WIDTH - SIDEBAR_WIDTH, 5 * SIDEBAR_ITEM_HEIGHT - 40),pygame.SRCALPHA)
scroll_bar_rect = pygame.Rect(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 1 * SIDEBAR_ITEM_HEIGHT - 40, 450, 200)
# side_bar = pygame.Surface((WINDOW_WIDTH - SIDEBAR_WIDTH, WINDOW_HEIGHT))
# side_bar.fill((200, 200, 200))
# side_bar_rect = pygame.Rect(side_bar.get_rect())
scroll_offset = 0
scroll_speed = 15
max_offset_top=0
max_offset_bottom=50
current_offset=0



menu_button_list = [menu_button1, menu_button2, menu_button3, menu_button4]

dragging = False
test_text = None
state = "Buy"

# Camera position
camera_x = 0
camera_y = 0
mouse_dragging = False
prev_mouse_pos = (0, 0)


switch_view("Buy",current_tier)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // TILE_SIZE
            grid_y = mouse_pos[1] // TILE_SIZE
            
            # if event.button == 1 and scroll_bar_rect.collidepoint(mouse_pos):  # Left click
            if event.button == 1 :  # Left click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Clicked ", mouse_x//TILE_SIZE, mouse_y//TILE_SIZE)
                # if testbutton.rect.collidepoint(mouse_pos):
                #     print("test")
                
                if research_button.rect.collidepoint(mouse_pos):
                    state = "Research"

                    print("Research button clicked")
                    

                elif previous_button.rect.collidepoint(mouse_pos) and current_tier > 1:
                    current_tier -=1
                    
                elif forward_button.rect.collidepoint(mouse_pos) and current_tier < 3:
                    current_tier +=1

                elif buy_button1.rect.collidepoint(mouse_pos):
                    state = "Buy"
                    print("Buy button clicked")
                elif upgrade_button1.rect.collidepoint(mouse_pos):
                    state = "Upgrade"
                    print("upgrade button clicked")
                    
                elif delete_multiple_button.rect.collidepoint(mouse_pos):
                    delete_mult()
                                  
                    
                elif convert_button.rect.collidepoint(mouse_pos):
                        # Convert energy to money
                        print("Energy converted to money")
                        player.sell_energy(player.energy)  # Sell all available energy

                        # Update money display after successful conversion
                        money_text = font.render(f'Money: {int(player.money)}', True, (0, 0, 0))
                elif WINDOW_WIDTH - SIDEBAR_WIDTH <= mouse_pos[0] < WINDOW_WIDTH and state == "Buy":

                    # Minor optimization problem
                    # for i in range(len(menu_button_list)):
                    #     if menu_button_list[i].rect.collidepoint(mouse_pos):
                    #         selected_building   = i
                        
                        
                    if menu_button1.rect.collidepoint(mouse_pos):
                        selected_building   = 1
                    elif menu_button2.rect.collidepoint(mouse_pos):
                        selected_building   = 2
                    elif menu_button3.rect.collidepoint(mouse_pos):
                        selected_building   = 3
                    elif menu_button4.rect.collidepoint(mouse_pos):
                        selected_building   = 4
                    elif menu_button4.rect.collidepoint(mouse_pos):
                        selected_building   = 5
                    
                    
                    
                elif WINDOW_WIDTH - SIDEBAR_WIDTH <= mouse_pos[0] < WINDOW_WIDTH and state == "Research":
                    if(((mouse_pos[1] // SIDEBAR_ITEM_HEIGHT) + 1) == 1):

 
                        if player.buy_research(Researches[1][2]):
                            if(current_tier == 1):
                                Researches[1] = list(Researches[1])  # Convert tuple to list
                                Researches[1][0] = True  # Modify boolean value
                                Researches[1] = tuple(Researches[1]) 
                            elif(current_tier == 2):
                                Researches[1] = list(Researches[1])  # Convert tuple to list
                                Researches[1][1] = True  # Modify boolean value
                                Researches[1] = tuple(Researches[1]) 
                            
                    elif(((mouse_pos[1] // SIDEBAR_ITEM_HEIGHT) + 1) == 2):
                        
                        if player.buy_research(Researches[2][2]):
                            if (current_tier == 1):
                                Researches[2] = list(Researches[2])  # Convert tuple to list
                                Researches[2][0] = True  # Modify boolean value
                                Researches[2] = tuple(Researches[2])
                            elif (current_tier == 2):
                                Researches[2] = list(Researches[2])
                                Researches[2][1] = True
                                Researches[2] = tuple(Researches[2])
                                 
                        



                    elif(((mouse_pos[1] // SIDEBAR_ITEM_HEIGHT) + 1) == 3): 
                        
                        if player.buy_research(Researches[3][2]):
                            if (current_tier == 1):
                                Researches[3] = list(Researches[3])  # Convert tuple to list
                                Researches[3][0] = True  # Modify boolean value
                                Researches[3] = tuple(Researches[3])
                            elif (current_tier == 2):
                                Researches[3] = list(Researches[3])
                                Researches[3][1] = True
                                Researches[3] = tuple(Researches[3])
                                 
                            
                    elif(((mouse_pos[1] // SIDEBAR_ITEM_HEIGHT) + 1) == 4): 
                        
                        if player.buy_research(Researches[4][2]):
                            if (current_tier == 1):
                                Researches[4] = list(Researches[4])  # Convert tuple to list
                                Researches[4][0] = True  # Modify boolean value
                                Researches[4] = tuple(Researches[4])
                            elif (current_tier == 2):
                                Researches[4] = list(Researches[4])
                                Researches[4][1] = True
                                Researches[4] = tuple(Researches[4])
                                 



                        
                elif WINDOW_WIDTH - SIDEBAR_WIDTH <= mouse_pos[0] < WINDOW_WIDTH and state == "Upgrade":
                    if(menu_button1.rect.collidepoint(mouse_pos)):
                        if player.buy_upgrade(50*(2**GENERATOR_UPGRADE)):
                            print("Generator Upgraded")
                            GENERATOR_UPGRADE+=1
                            for generator in generators:
                                generator.heat_per_tick *= 1.5
                            print(GENERATOR_UPGRADE)
                        # else: 
                        #     # not_enough_money = font.render(f'Not Enough Money', True, (0, 0, 0))
                        #     # window.blit(not_enough_money,( mouse_pos[0], mouse_pos[1]))
                    elif(menu_button2.rect.collidepoint(mouse_pos)):
                        if player.buy_upgrade( 50*(2**CONVERTER_UPGRADE)):
                            print("Converter Upgraded")
                            CONVERTER_UPGRADE+=1
                            for converter in converters:
                                converter.heat_conversion_per_second *= 1.5
                            print(CONVERTER_UPGRADE)

                    elif(menu_button3.rect.collidepoint(mouse_pos)): 
                        if player.buy_upgrade(50*(2**OFFICE_UPGRADE)):
                            print("Office Upgraded")
                            OFFICE_UPGRADE+=1
                            for office in offices:
                                office.energy_sell_rate *= 1.5
                            print(OFFICE_UPGRADE)
  
                    elif(menu_button4.rect.collidepoint(mouse_pos)): 
                        if player.buy_upgrade(50*(2**RESEARCHLAB_UPGRADE)):
                            print("Research Lab Upgraded")
                            RESEARCHLAB_UPGRADE+=1
                            for lab in labs:
                                lab.research_rate *= 1.5
                            print(RESEARCHLAB_UPGRADE)

                        
                
                elif grid[grid_x][grid_y] == TILE_EMPTY:
                    # Place selected building on the grid
                    grid_x = mouse_pos[0] // TILE_SIZE
                    grid_y = mouse_pos[1] // TILE_SIZE
                    # if 0 <= grid_x < NUM_TILES_X and 0 <= grid_y < NUM_TILES_Y:
                    #     if selected_building == 1 and player.buy_energy_generator(HeatGenerator(current_tier,GENERATOR_UPGRADE)):
                    #         if research_check(1,current_tier):
                    #             print("Generator bought")
                    #             grid[grid_x][grid_y] = HeatGenerator(current_tier,GENERATOR_UPGRADE)
                    #             generators.append(grid[grid_x][grid_y]) 
                    #         else:


                    #             confirmation_window(not_researched_text,ok_text)
                                
                    #     elif selected_building == 2 and player.buy_energy_generator(EnergyConverter(current_tier,CONVERTER_UPGRADE)):
                    #         if research_check(2,current_tier):
                    #             print("Converter bought")
                    #             grid[grid_x][grid_y] = EnergyConverter(current_tier,CONVERTER_UPGRADE)
                    #             converters.append(grid[grid_x][grid_y])
                    #         else:
 

                    #             confirmation_window(not_researched_text,ok_text)
                    #     elif selected_building == 3 and player.buy_energy_generator(Office(current_tier,OFFICE_UPGRADE)) :
                    #         if research_check(3,current_tier):
                                
                    #             print("Office bought")
                    #             grid[grid_x][grid_y] = Office(current_tier,OFFICE_UPGRADE)
                    #             offices.append(grid[grid_x][grid_y])
                    #         else:


                    #             confirmation_window(not_researched_text,ok_text)
                            
                    #     elif selected_building == 4 and player.buy_energy_generator(ResearchLab(current_tier,RESEARCHLAB_UPGRADE)):
                    #         if research_check(4,current_tier):
                    #             print("Lab bought")
                    #             grid[grid_x][grid_y] = ResearchLab(current_tier,RESEARCHLAB_UPGRADE)
                    #             labs.append(grid[grid_x][grid_y])
                    #         else:
                    #             confirmation_window(not_researched_text,ok_text)
                    #     elif selected_building == 5 :

                    #             print("Battery bought")

            elif event.button == 3:  # Right click
                # Sell selected building on the grid

                if 0 <= grid_x < NUM_TILES_X and 0 <= grid_y < NUM_TILES_Y:
                    if isinstance(grid[grid_x][grid_y], EnergyConverter):
                        if(player.sell_building(grid[grid_x][grid_y])):
                            grid[grid_x][grid_y] = TILE_EMPTY
                    elif isinstance(grid[grid_x][grid_y], HeatGenerator):
                        if(player.sell_building(grid[grid_x][grid_y])):
                            grid[grid_x][grid_y] = TILE_EMPTY
                    elif isinstance(grid[grid_x][grid_y], Office):
                        if(player.sell_building(grid[grid_x][grid_y])):
                            grid[grid_x][grid_y] = TILE_EMPTY
                    elif isinstance(grid[grid_x][grid_y], ResearchLab):
                            if(player.sell_building(grid[grid_x][grid_y])):
                                grid[grid_x][grid_y] = TILE_EMPTY
            elif event.button == 4 and scroll_bar_rect.collidepoint(mouse_pos)   :  # Mouse wheel up
               
                if current_offset > max_offset_top:
                    scroll_offset += scroll_speed
                    current_offset -= scroll_speed
                    print("scroll up",scroll_offset,current_offset," ",max_offset_top)
                # menu_button1.rect.move(0, scroll_speed)
            elif event.button == 5 and scroll_bar_rect.collidepoint(mouse_pos):  # Mouse wheel down
               if current_offset < max_offset_bottom:
                    scroll_offset -= scroll_speed
                    current_offset += scroll_speed
                    print("scroll up",scroll_offset,current_offset," ",max_offset_top)
  
    font = pygame.font.Font(None, 24)



    total_energy_sold = 0
    # for i in range(NUM_TILES_X):
    #     for j in range(NUM_TILES_Y):
    #         if isinstance(grid[i][j], Office):
    #             grid[i][j].sell_energy(player)
    #             total_energy_sold += grid[i][j].energy_sell_rate
    
    for office in offices:
        office.sell_energy(player)
        total_energy_sold += office.energy_sell_rate
                
    for lab in labs:
        lab.research(player)       


    # Display game information
    
    # continent = pygame.Surface((WINDOW_WIDTH - SIDEBAR_WIDTH, WINDOW_HEIGHT))
  
 
   # Draw tiles and objects
#     for i in range(NUM_TILES_X):
#         for j in range(NUM_TILES_Y):
#             rect = pygame.Rect(i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE)
#             if isinstance(grid[i][j], EnergyConverter):
#                 continent.blit(converter_images[grid[i][j].tier], rect)
#             elif isinstance(grid[i][j], HeatGenerator):
#                continent.blit(generator_images[grid[i][j].tier], rect)
#             elif isinstance(grid[i][j], Office):
#                continent.blit(office_images[grid[i][j].tier], rect)
#             elif isinstance(grid[i][j], ResearchLab):
#                 continent.blit(researchlab_images[grid[i][j].tier], rect)
#             else:
#                 continent.blit(tile_image, rect)
# #                 # pygame.draw.rect(window, WHITE, rect, 1)
#             window.blit(continent, (0,0))
    
    
    
    tile_image = pygame.transform.scale(pygame.image.load('Data/tile2.jpg'), (50, 50))

   # Draw tiles and objects
    for i in range(NUM_TILES_X):
        for j in range(NUM_TILES_Y):
            rect = pygame.Rect(i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if isinstance(grid[i][j], EnergyConverter):
                window.blit(converter_images[grid[i][j].tier], rect)
            elif isinstance(grid[i][j], HeatGenerator):
                window.blit(generator_images[grid[i][j].tier], rect)
            elif isinstance(grid[i][j], Office):
                window.blit(office_images[grid[i][j].tier], rect)
            elif isinstance(grid[i][j], ResearchLab):
                window.blit(researchlab_images[grid[i][j].tier], rect)
            else:
                window.blit(tile_image, rect)
#                 # pygame.draw.rect(window, WHITE, rect, 1)


        # window.blit(scroll_bar, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 1 * SIDEBAR_ITEM_HEIGHT - 40))


    # window.blit(side_bar, (WINDOW_WIDTH - SIDEBAR_WIDTH, WINDOW_HEIGHT))
    # scroll_bar.convert_alpha()
    # window.blit(scroll_bar, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 1 * SIDEBAR_ITEM_HEIGHT - 40))
    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)) 


    menu_button1.draw(window)
    menu_button2.draw(window)
    menu_button3.draw(window)
    menu_button4.draw(window)
    menu_button5.draw(window)
    # testbutton.draw(window)
    scroll_offset = 0

    #Draw sidebar
    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH, 0,10 , WINDOW_HEIGHT)) 
    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH , 1 * SIDEBAR_ITEM_HEIGHT - 40)) 
    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH+460, 0,SIDEBAR_WIDTH-460 , WINDOW_HEIGHT)) 
    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH, 5 * SIDEBAR_ITEM_HEIGHT - 40, SIDEBAR_WIDTH , WINDOW_HEIGHT-  SIDEBAR_ITEM_HEIGHT - 40)) 
    switch_view(state,current_tier)
    # pygame.draw.rect(window, (0, 105, 148), scroll_bar_rect)


    # Display game information (money and power)
    money_text = font.render(f'Money: {int(player.money)}', True, (0, 0, 0))
    energy_text = font.render(f'Energy: {int(player.energy)}/{int(player.max_energy)}', True, (0, 0, 0))
    research_text = font.render(f'Research: {int(player.research)}', True, (0, 0, 0))
    total_energy_text = font.render(f'Energy Per Second: {int(total_energy_sold*60*2.5)}', True, (0, 0, 0))
    window.blit(money_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 80))
    window.blit(energy_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 175, WINDOW_HEIGHT - 80))
    window.blit(research_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 350, WINDOW_HEIGHT - 80))
    window.blit(total_energy_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 120))
    


    # Blit the bottom bar onto the main window
    # window.blit(bottom_bar, (0, WINDOW_HEIGHT - 50))

    #DRAW BUTTONS
    buy_button1.draw(window)
    upgrade_button1.draw(window)
    forward_button.draw(window)
    previous_button.draw(window) 
    delete_multiple_button.draw(window)
    research_button.draw(window)
    convert_button.draw(window)




    # Check if mouse is hovering over a placed building
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pos = pygame.mouse.get_pos()
    test = font.render(f'Coordinates: {mouse_x,mouse_y}', True, (0, 0, 0))
    window.blit(test,( mouse_pos[0], mouse_pos[1]))

    
    grid_x = mouse_pos[0] // TILE_SIZE
    grid_y = mouse_pos[1] // TILE_SIZE
    if 0 <= grid_x < NUM_TILES_X and 0 <= grid_y < NUM_TILES_Y:
        info_text = None
        if isinstance(grid[grid_x][grid_y], EnergyConverter):
            info_text = font.render(f'Energy per heat: {grid[grid_x][grid_y].heat_conversion_per_second}', True, (255, 255, 255))

        elif isinstance(grid[grid_x][grid_y], HeatGenerator):
            info_text = font.render(f'Heat per tick: {grid[grid_x][grid_y].heat_per_tick}', True, (255, 255, 255))

        elif isinstance(grid[grid_x][grid_y], Office):
            info_text = font.render(f'Energy sell rate: {grid[grid_x][grid_y].energy_sell_rate * 60:.2f} per second tier {grid[grid_x][grid_y].tier}', True, (255, 255, 255))
        
        elif isinstance(grid[grid_x][grid_y], ResearchLab):
            info_text = font.render(f'Research rate: {grid[grid_x][grid_y].research_rate * 60:.2f} per second tier {grid[grid_x][grid_y].tier}', True, (255, 255, 255))

        else :
            info_text = None
    
        if(info_text != None):
            info_bg = pygame.Surface((info_text.get_width()+20, info_text.get_height()+20))
            info_bg.fill((0, 0, 0))
            info_bg.blit(info_text, (10, 10))
            info_bg.set_alpha(150)
            window.blit(info_bg, (mouse_pos[0] + 10, mouse_pos[1] + 10))
    
    
    # Update the screen
    pygame.display.flip()
    clock.tick(FPS)

# Quit pygame
# save_grid("save.json")
pygame.quit()