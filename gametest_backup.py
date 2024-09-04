import pygame
import threading
import json

# Player class
class Player:
    def __init__(self):
        self.energy = 0
        self.money = 10000000
        self.research = 50000
        self.max_energy = 200

    def buy_energy_generator(self, Building):
        if self.money >= Building.cost:
            self.money -= Building.cost
            return True
        return False

    def enough_money(self, Building):
        if self.money >= Building.cost:
            return True
        return False

    def buy_research(self, cost):
        if self.research >= cost.cost:
            self.research -= cost.cost
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
    def __init__(self, tier,upgrade,name):
        self.cost = 1000 * (4 ** (tier - 1)) * (tier - 1) + (10 if tier == 1 else 0)
        self.heat_per_tick = 1*tier*upgrade*1.50/120 *(100 ** (tier - 1))
        # self.life_cycle = 600
        self.tier = tier
        self.name = name
        self.upgrade = upgrade
        
    def generate_heat(self):
        
        
          
        if (self.tier > 1):

            return self.heat_per_tick
        else:

            player.generate_energy(self.heat_per_tick)

            return 0
        
        
        # if self.life_cycle == 0:
        #     handle_destruction(self)
            
        #     return 0
        
        # if (self.tier > 1):
        #     self.life_cycle -=1
        #     return self.heat_per_tick
        # else:

        #     player.generate_energy(self.heat_per_tick)
        #     self.life_cycle -=1
        #     return 0
            
            
    def upgrade_production(self):
        self.heat_per_tick *= 1.5
          

class EnergyConverter:
    def __init__(self, tier, upgrade,name):
        self.cost = 2000 * (12 ** (tier - 1)) 
        self.tier = tier
        self.upgrade = upgrade

        self.max_heat = 10*tier*upgrade*2*(100 ** (tier - 1))
        self.heat_conversion_per_second = 1*tier*upgrade*1.25*(100 ** (tier - 1))
        self.stored_heat = 0
        self.name = name

    def convert_heat(self, heat):

        if heat <= self.heat_conversion_per_second:
          player.generate_energy(heat)

        else:
            if self.stored_heat + heat < self.max_heat:
                player.generate_energy(heat)
                self.stored_heat += heat
            else:
                handle_destruction(self)
        
    def upgrade_production(self):
        self.heat_conversion_per_second *= 1.25


class Office:
    def __init__(self,tier,upgrade,name):
        self.energy_sell_rate = 1*tier*upgrade*1.5 *(100 ** (tier - 1)) # Energy selling rate for the office (per second)
        self.cost = 10000 * (4 ** (tier - 1)) 
        self.tier = tier
        self.name = name
        self.upgrade = upgrade

    def sell_energy(self, player):
        # Sell energy at the defined rate
        if player.energy >= self.energy_sell_rate:
            player.energy -= self.energy_sell_rate 
            player.money += self.energy_sell_rate  # Assuming 1 energy = 10 money
        elif player.energy > 0:
            player.money += player.energy *2
            player.energy = 0
            
            
    def upgrade_production(self):
        self.energy_sell_rate *= 1.5

class ResearchLab:
    def __init__(self,tier,upgrade,name):
        self.research_rate = 1*tier*upgrade*1.5  *(100 ** (tier - 1))
        self.cost = 500 * (160 ** (tier - 1))  
        self.tier = tier
        self.name = name
        self.upgrade = upgrade

    def research(self, player):
            player.research += self.research_rate/60
            
    def upgrade_production(self):
        self.research_rate *= 1.5

        
class Battery:
    def __init__(self,tier,upgrade,name):
        self.battery_capacity = 200*upgrade*2
        self.cost = 5000
        self.name = name
        self.tier = tier
        self.upgrade = upgrade
        
    def upgrade_production(self):
        self.battery_capacity *= 2
    

            
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
        self.y = y
        
    def draw(self, surface):
        pygame.draw.rect(surface,self.color, self.rect)
        if self.text and not self.image and not self.text == "Tracker":
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

        if self.text == "Tracker":
            if 10 <= self.rect.y <= 400:
                self.rect.move_ip(0, 0.334*-scroll_offset)
            elif  self.rect.y < 10: 
                self.rect.y = 1 * SIDEBAR_ITEM_HEIGHT - 40
            elif self.rect.y > 400:
                self.rect.y = 400

        else:  
            self.rect.move_ip(0, scroll_offset)
        
                
                


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.command:
                self.command()
                
    def button_update(self, text=None, image=None):



        self.text = text
        self.image = image


                
def tab_change(current_offset):
    
    scroll_tracker.rect.y = 1 * SIDEBAR_ITEM_HEIGHT - 40
    for button in menu_button_list:
        button.rect.move_ip(0,current_offset)

    
def handle_destruction(building):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
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
                elif no_text != None and no_button_rect.collidepoint(mouse_pos):
                    return False
            
def switch_view(state, tier):

    
    if state == "Buy":
    
        
        menu_text = font.render("Buy Menu",True,(255,255,255))

        for i in buy_menu:
            menu_button_list[i-1].button_update(text=f'{buy_menu[i][0]} (${number_format(buy_menu[i][1](buy_menu[i][4],1,buy_menu[i][0]).cost)})', image = pygame.transform.scale(tile_images[i],(40,40)))

 
         
         
                                                                        
        
    elif state == "Upgrade":


        building_index = []
        for key, value in buy_menu.items():
            if value[1] == HeatGenerator:
                building_index.append(key)
        

        menu_button_list[0].button_update(text=f'{buy_menu[1][0]}: Increase Production by %50 (${number_format(upgrade_costs[0])})', image = pygame.transform.scale(tile_images[1],(40,40)))
        menu_button_list[1].button_update(text=f'{buy_menu[1][0]}: Increase Lifetime by %100 (${number_format(upgrade_costs[1])})', image = pygame.transform.scale(tile_images[1],(40,40)))
        menu_button_list[2].button_update(text=f'Research Center: Increase Research Rate by %25 (${number_format(upgrade_costs[2])})', image = pygame.transform.scale(tile_images[2],(40,40)))
        menu_button_list[3].button_update(text=f'Office: Increase Sell Rate by %50 (${number_format(upgrade_costs[3])})', image = pygame.transform.scale(tile_images[4],(40,40)))
        menu_button_list[4].button_update(text=f'Battery: Increase Max Energy by %100 (${number_format(upgrade_costs[4])})', image = pygame.transform.scale(tile_images[3],(40,40)))
        menu_button_list[5].button_update(text=f'Generator: Increase Max Heat %100 (${number_format(upgrade_costs[5])})', image = pygame.transform.scale(tile_images[6],(40,40)))
        menu_button_list[6].button_update(text=f'Generator: Increase Conversion Rate by %25 (${number_format(upgrade_costs[6])})', image = pygame.transform.scale(tile_images[6],(40,40)))


        del building_index[0]

        i = 7
        for key in building_index:
            menu_button_list[i].button_update(text=f'{buy_menu[key][0]}: Increase Production by %50 (${number_format(upgrade_costs[i])})', image = pygame.transform.scale(tile_images[key],(40,40)))
            menu_button_list[i+1].button_update(text=f'{buy_menu[key][0]}: Increase Lifetime by %100 (${number_format(upgrade_costs[i+1])})', image = pygame.transform.scale(tile_images[key],(40,40)))
            i+=2
        menu_text = font.render("Upgrade Menu",True,(255,255,255))
        
      
      
      
      
      
      
      
        # 0 1 (23456) 7 8 ..... 35

        # for i in buy_menu:
        #     if buy_menu[i][1] == HeatGenerator:
        #         menu_button_list[i-1].button_update(text=f'{buy_menu[i][0]} Increase Production by %50 (${number_format(buy_menu[i][1](buy_menu[i][4],1,buy_menu[i][0]).cost)})', image = pygame.transform.scale(tile_images[i],(40,40)))
        #         menu_button_list[i].button_update(text=f'{buy_menu[i][0]} Increase Lifetime by %100 (${number_format(buy_menu[i][1](buy_menu[i][4],1,buy_menu[i][0]).cost)})', image = pygame.transform.scale(tile_images[i],(40,40)))



    elif state == "Research":
        
        menu_text = font.render("Research Menu",True,(255,255,255))
        # menu_button_list[0].button_update(text=f'{buy_menu[2][0]} (${buy_menu[2][1](buy_menu[2][4],1,buy_menu[2][0]).cost*2})', image = pygame.transform.scale(tile_images[2],(40,40)))

        for i in range(len(buy_menu)-1):

            # menu_button_list[i-1].button_update(text=f'{buy_menu[i][0]} (${buy_menu[i][1](current_tier,1,buy_menu[i][0]).cost})', image = buy_menu[i][2])
            if buy_menu[i+2][5] == False:
                menu_button_list[i].button_update(text=f'{buy_menu[i+2][0]} ({number_format(research_costs[i])} Research Points)', image = pygame.transform.scale(tile_images[i+2],(40,40)))
            else:
                menu_button_list[i].button_update(text = f'Research Bought!')

        menu_button_list[31].button_update()
 
          
    energy_gen_thread = threading.Thread(target=energy_gen)
    energy_gen_thread.start()

# Create two threads
 
def energy_gen():
    if grid != None:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
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


def research_check(building,index,state):
    
    return state

    
    
    
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
                grid_x = (mouse_pos[0]-move_x) // TILE_SIZE
                grid_y = (mouse_pos[1]-move_y) // TILE_SIZE
                if event.button == 1 and (0 <= grid_x < len(grid)*TILE_SIZE+move_x and 0 <= grid_y < len(grid[grid_x])*TILE_SIZE+move_y) and grid[grid_x][grid_y] != TILE_EMPTY and grid[grid_x][grid_y] != TILE_OCEAN:  # Left click
                    if (grid[grid_x][grid_y] not in selected_tiles):
                        x_of_building.append(grid_x)
                        print(grid_x, grid_y)
                        y_of_building.append(grid_y)
                        selected_tiles.append((grid[grid_x][grid_y]))
                        rect = pygame.Rect(grid_x * TILE_SIZE+move_x, grid_y * TILE_SIZE+move_y, TILE_SIZE, TILE_SIZE)
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

def button_creator():
    
    for i in range(35):
        if i < 32:
            menu_button_list.append(Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, (i+1) * SIDEBAR_ITEM_HEIGHT - 40, 450, 50, text=f'{buy_menu[i+1][0]} (${buy_menu[i+1][1](buy_menu[i+1][4],1,buy_menu[i+1][0]).cost})',image=buy_menu[i+1][2]))
        else :
            menu_button_list.append(Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, (i+1) * SIDEBAR_ITEM_HEIGHT - 40, 450, 50))

        print(menu_button_list[i].text,menu_button_list[i].rect)
        
        
        
        
    
def button_drawer():
    for button in menu_button_list:

            button.draw(window) 
        
        
def number_format(number):
    numbers = ["0","K","M","B","T","AA","AB","AC","BA","BB","BC"]    
    for i in range(len(numbers)):
        if number < 1000**(i+1):
            if i > 0:
                return f"{number/1000**i:.2f}{numbers[i]}"
            else:
                return str(number)
    return f"{number/1000**(len(numbers)-1):.2f}{numbers[-1]}"
   
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

# Save the grid to a file

def save_grid(filename):
    player_dict = {"energy": player.energy, "money": player.money, "research": player.research, "max_energy": player.max_energy}
    new_grid = {}
    researches = []

    for i in range(NUM_TILES_X):
        for j in range(NUM_TILES_Y):
            if grid[i][j] != TILE_EMPTY:
                new_grid[f"{i},{j}"] = {"tile_type": grid[i][j].name, "tier": grid[i][j].tier, "upgrade": grid[i][j].upgrade}
                
    for i in range(len(buy_menu)):
        researches.append(buy_menu[i+1][5])

    data = {"player": player_dict, "grid": new_grid, "researches": researches}

    with open(filename, 'w') as f:
        json.dump(data, f)
    print("saved")


# Load the grid from a file
def load_grid(filename,player,grid):
    # Load the JSON data from the file
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("File not found")
        return None
    # for data in player_data:
    #     player1 = Player(data["energy"], data["money"], data["research"], data["max_energy"])
    player_data = data.get("player", {})
    player.energy = player_data.get("energy", 0)
    player.money = player_data.get("money", 0)
    player.research = player_data.get("research", 0)
    player.max_energy = player_data.get("max_energy", 0)
    
    researches = data.get("researches", {})
    for i in range(len(buy_menu)):
        research = list(buy_menu[i+1])
        research[5] = researches[i]
        buy_menu[i+1] = research
    
    
    
    
    
    grid_list = data.get("grid", {})
    grid = [[TILE_EMPTY for j in range(NUM_TILES_Y)] for i in range(NUM_TILES_X)]
    for key, value in grid_list.items():
        i, j = key.split(",")
        i, j = int(i), int(j)
        print(i,j)
        tile_type = value.get("tile_type", "")
        tile_tier = value.get("tier", 1)
        tile_upgrade = value.get("upgrade", 0)
        for key, value in buy_menu.items():
            if value[0] == tile_type:
                grid[i][j] = buy_menu[key][1](tile_tier,tile_upgrade,tile_type)
    return grid

# class PlayerEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Player):
#             return {"energy": obj.energy, "money": obj.money, "research": obj.research, "max_energy": obj.max_energy}
#         else:
#             return super().default(obj)




# Tile constants
TILE_SIZE = 50
# NUM_TILES_X = 16  # Adjusted for the grid size
# NUM_TILES_X = 16
# NUM_TILES_Y = 12 
NUM_TILES_X = 16
NUM_TILES_Y = 12 

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
TILE_EMPTY = 1
TILE_OCEAN = 0
TILE_CONVERTER = 1
TILE_GENERATOR = 2
TILE_OFFICE = 3
TILE_ResearchLab = 4




# # Object prices
# CONVERTER_PRICE = 200
# GENERATOR_PRICE = 300
# OFFICE_PRICE = 500
# RESEARCHLAB_PRICE = 1000

# # Energy production rates for each building type
# ENERGY_RATE_CONVERTER = 2/60
# ENERGY_RATE_GENERATOR = 5/60

# Initialize pygame
pygame.init()

# Initialize the window
# WINDOW_WIDTH = NUM_TILES_X * TILE_SIZE + SIDEBAR_WIDTH
# WINDOW_HEIGHT = NUM_TILES_Y * TILE_SIZE +50
# WINDOW_HEIGHT = NUM_TILES_Y * TILE_SIZE  
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1700
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
grid = [[TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_EMPTY, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, 
TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, 
TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, 
TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, 
TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, 
TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, 
TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, 
TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_EMPTY, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN,TILE_OCEAN,TILE_OCEAN,TILE_OCEAN,TILE_OCEAN,TILE_OCEAN], [TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN,TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN, TILE_OCEAN]]

# grid = [[TILE_EMPTY for _ in range(NUM_TILES_Y)] for _ in range(NUM_TILES_X)]

# converters= []
# generators = []
# offices = []
# labs = []

turkey_grid = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 
1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 
0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0], [0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


# Sample prices for different tiers (you should replace these with your actual prices)
TIER_PRICES = {
    1: [[10, 20, 30], [40, 50, 60]],  # Prices for tier 1 for pages 1 and 2
    2: [[50, 60, 70], [80, 90, 100]]   # Prices for tier 2 for pages 1 and 2 (example)
}


Researches = {
    1: (False,False ,1000),
    2: (False,False ,1000),
    3: (False,False ,1000),
    4: (False,False ,1000),
    5: (True,True ,1000)

}
    


# Load building images
tile_images = {
 

    1: pygame.transform.scale(pygame.image.load('Data/windmill.png'), (50,50)),
    2: pygame.transform.scale(pygame.image.load('Data/research1full.png'), (50,50)),
    3: pygame.transform.scale(pygame.image.load('Data/battery.png'), (50,50)),
    4: pygame.transform.scale(pygame.image.load('Data/officefull.png'), (50,50)),
    5: pygame.transform.scale(pygame.image.load('Data/solarpanelfull.png'), (50,50)),
    6: pygame.transform.scale(pygame.image.load('Data/generatorfull.png'), (50,50)),
    7: pygame.transform.scale(pygame.image.load('Data/coalfactory.png'), (50,50)),
    8: pygame.transform.scale(pygame.image.load('Data/office2.png'), (50,50)),
    9: pygame.transform.scale(pygame.image.load('Data/gasburnerfull.png'), (50,50)),
    10: pygame.transform.scale(pygame.image.load('Data/generator2full.png'), (50,50)),
    11: pygame.transform.scale(pygame.image.load('Data/research2full.png'), (50,50)),
    12: pygame.transform.scale(pygame.image.load('Data/nuclearreactorfull.png'), (50,50)),
    13: pygame.transform.scale(pygame.image.load('Data/office3.png'), (50,50)),
    14: pygame.transform.scale(pygame.image.load('Data/thermoreactorfull.png'), (50,50)),
    15: pygame.transform.scale(pygame.image.load('Data/office4.png'), (50,50)),
    16: pygame.transform.scale(pygame.image.load('Data/fusion.png'), (50,50)),
    17: pygame.transform.scale(pygame.image.load('Data/generator3full.png'), (50,50)),
    18: pygame.transform.scale(pygame.image.load('Data/office5.png'), (50,50)),
    19: pygame.transform.scale(pygame.image.load('Data/tokamak.png'), (50,50)),
    20: pygame.transform.scale(pygame.image.load('Data/stellarator.png'), (50,50)),
    21: pygame.transform.scale(pygame.image.load('Data/generator4.png'), (50,50)),
    22: pygame.transform.scale(pygame.image.load('Data/office6.png'), (50,50)),
    23: pygame.transform.scale(pygame.image.load('Data/ufo.png'), (50,50)),
    24: pygame.transform.scale(pygame.image.load('Data/arc.png'), (50,50)),
    25: pygame.transform.scale(pygame.image.load('Data/office7.png'), (50,50)),
    26: pygame.transform.scale(pygame.image.load('Data/research3full.png'), (50,50)),
    27: pygame.transform.scale(pygame.image.load('Data/cosmic.png'), (50,50)),
    28: pygame.transform.scale(pygame.image.load('Data/geothermal.png'), (50,50)),
    29: pygame.transform.scale(pygame.image.load('Data/generator5full2.png'), (50,50)),
    30: pygame.transform.scale(pygame.image.load('Data/tesla.png'), (50,50)),
    31: pygame.transform.scale(pygame.image.load('Data/office8.png'), (50,50)),
    32: pygame.transform.scale(pygame.image.load('Data/dark.png'), (50,50))
}

background_image = pygame.transform.scale(pygame.image.load('Data/background.jpg'), (50, 50))
# turkey_grid = pygame.transform.scale(pygame.image.load('Data/turkey_map.png'), (50, 50))

converter_menu_images = {
    1: pygame.transform.scale(pygame.image.load('Data/generator1.png'), (40, 40)),
    2: pygame.transform.scale(pygame.image.load('Data/generator2fullmenu.png'), (40, 40)),
    3: pygame.transform.scale(pygame.image.load('Data/generator1.png'), (40, 40)),
    4: pygame.transform.scale(pygame.image.load('Data/generator2fullmenu.png'), (40, 40)),
    5: pygame.transform.scale(pygame.image.load('Data/generator3fullmenu.png'), (40, 40))

    
}
generator_menu_images = {
 
    1 : pygame.transform.scale(pygame.image.load('Data/windmill_menu.png'), (40, 40)),
    2 : pygame.transform.scale(pygame.image.load('Data/convertermenu.png'), (40, 40)),
    3 : pygame.transform.scale(pygame.image.load('Data/coalfactorymenu.png'), (40, 40)),
    4: pygame.transform.scale(pygame.image.load('Data/gasburnerfull.png'), (40, 40)),
    5: pygame.transform.scale(pygame.image.load('Data/nuclearreactorfull.png'), (40, 40)),
    6: pygame.transform.scale(pygame.image.load('Data/generator4full.png'), (40, 40)),
    7: pygame.transform.scale(pygame.image.load('Data/generator5full.png'), (40, 40)),
    8 : pygame.transform.scale(pygame.image.load('Data/convertermenu.png'), (40, 40)),
    9 : pygame.transform.scale(pygame.image.load('Data/coalfactorymenu.png'), (40, 40)),
    10: pygame.transform.scale(pygame.image.load('Data/gasburnerfull.png'), (40, 40)),
    11: pygame.transform.scale(pygame.image.load('Data/nuclearreactorfull.png'), (40, 40)),
    12: pygame.transform.scale(pygame.image.load('Data/generator4full.png'), (40, 40)),
    13: pygame.transform.scale(pygame.image.load('Data/generator5full.png'), (40, 40)),
    14: pygame.transform.scale(pygame.image.load('Data/generator6full.png'), (40, 40)),
    15: pygame.transform.scale(pygame.image.load('Data/generator5full.png'), (40, 40))
 
}
office_menu_images = {
 
    1 : pygame.transform.scale(pygame.image.load('Data/office.png'), (40, 40)),
    2 : pygame.transform.scale(pygame.image.load('Data/office2menu.png'), (40, 40)),
    3 : pygame.transform.scale(pygame.image.load('Data/office3menu.png'), (40, 40)),
    4 : pygame.transform.scale(pygame.image.load('Data/office.png'), (40, 40)),
    5 : pygame.transform.scale(pygame.image.load('Data/office2menu.png'), (40, 40)),
    6 : pygame.transform.scale(pygame.image.load('Data/office3menu.png'), (40, 40)),   
    7 : pygame.transform.scale(pygame.image.load('Data/office2menu.png'), (40, 40)),
    8 : pygame.transform.scale(pygame.image.load('Data/office3menu.png'), (40, 40))
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

battery_images = {
    1:pygame.transform.scale(pygame.image.load('Data/batterymenu.png'), (40,40)),
    2:pygame.transform.scale(pygame.image.load('Data/battery.png'), (50,50))

}

upgrade_costs = []

for i in range(35):
    upgrade_costs.append(50*i+50)
    
    
research_costs = []

for i in range(35):
    # research_costs.append(500*(i**8)+50)
    research_costs.append(500*(i**3)+50)


menu_button_list = []


buy_menu_tags= ["name","class","image","upgrade1","tier","research","upgrade2"]




#Upgrade Stats
CONVERTER_UPGRADE = 1
CONVERTER_UPGRADE2 = 1
# GENERATOR_UPGRADE = 1
OFFICE_UPGRADE = 1
RESEARCHLAB_UPGRADE = 1
BATTERY_UPGRADE = 1


buy_menu = {
    1:("Wind Turbine",HeatGenerator,generator_menu_images[1],1,1,True,1),
    2:("Small Research Center",ResearchLab,researchlab_menu_images[1],RESEARCHLAB_UPGRADE,1,False,1),
    3:("Battery",Battery,battery_images[1],BATTERY_UPGRADE,1,False,1),
    4:("Small Office",Office,office_menu_images[1],OFFICE_UPGRADE,1,False,1),
    5:("Solar Panel",HeatGenerator,generator_menu_images[2],1,2,False,1),
    6:("Small Generator",EnergyConverter,converter_menu_images[1],CONVERTER_UPGRADE,1,False,CONVERTER_UPGRADE2),
    7:("Coal Burner",HeatGenerator,generator_menu_images[3],1,3,False,1),
    8:("Big Office",Office,office_menu_images[2],OFFICE_UPGRADE,2,False,1),
    9:("Gas Burner",HeatGenerator,generator_menu_images[4],1,4,False,1),
    10:("Medium Generator",EnergyConverter,converter_menu_images[2],CONVERTER_UPGRADE,2,False,CONVERTER_UPGRADE2),
    11:("Research Center",ResearchLab,researchlab_menu_images[2],RESEARCHLAB_UPGRADE,2,False,1),
    12:("Nuclear Reactor",HeatGenerator,generator_menu_images[5],1,5,False,1),
    13:("Small Corp",Office,office_menu_images[3],OFFICE_UPGRADE,3,False,1),
    14:("Thermo Reactor",HeatGenerator,generator_menu_images[6],1,6,False,1),
    15:("Medium Corp",Office,office_menu_images[4],OFFICE_UPGRADE,4,False,1),
    16:("Fusion Reactor",HeatGenerator,generator_menu_images[7],1,7,False,1),
    17:("Big Generator",EnergyConverter,converter_menu_images[3],CONVERTER_UPGRADE,3,False,CONVERTER_UPGRADE2),
    18:("Big Corp",Office,office_menu_images[5],OFFICE_UPGRADE,5,False,1),
    19:("Tokamak",HeatGenerator,generator_menu_images[8],1,8,False,1),
    20:("Stellarator",HeatGenerator,generator_menu_images[9],1,9,False,1),
    21:("The Biggest Generator",EnergyConverter,converter_menu_images[4],CONVERTER_UPGRADE,4,False,CONVERTER_UPGRADE2),
    22:("Small Bank",Office,office_menu_images[6],OFFICE_UPGRADE,6,False,1),
    23:("Ufo Spaceship Reactor",HeatGenerator,generator_menu_images[10],1,10,False,1),
    24:("Arc Reactor",HeatGenerator,generator_menu_images[11],1,11,False,1),
    25:("Medium Bank",Office,office_menu_images[7],OFFICE_UPGRADE,7,False,1),
    26:("Big Research Center",ResearchLab,researchlab_menu_images[3],RESEARCHLAB_UPGRADE,3,False,1),
    27:("Cosmic Radiation Reactor",HeatGenerator,generator_menu_images[12],1,12,False,1),
    28:("Geothermal Reactor",HeatGenerator,generator_menu_images[13],1,13,False,1),
    29:("Ultra Generator",EnergyConverter,converter_menu_images[5],CONVERTER_UPGRADE,5,False,CONVERTER_UPGRADE2),
    30:("Tesla Reactor",HeatGenerator,generator_menu_images[14],1,14,False,1),
    31:("Big Bank",Office,office_menu_images[8],OFFICE_UPGRADE,8,False,1),
    32:("Dark Energy Reactor",HeatGenerator,generator_menu_images[15],1,15,False,1),
}

# upgrade_menu = {
#     1: ("Wind Turbine", buy_menu[1][3]),
#     2: ("Wind Turbine", buy_menu[1][6]),
#     3: ("Research Center", RESEARCHLAB_UPGRADE),
#     4: ("Office", OFFICE_UPGRADE),
#     5: ("Battery", BATTERY_UPGRADE),
#     6: ("Generator", CONVERTER_UPGRADE),
#     7: ("Generator", CONVERTER_UPGRADE2),
#     8: ("Solar Panel", buy_menu[5][3]),
#     9: ("Solar Panel", buy_menu[5][6]),
#     10: ("Coal Burner", buy_menu[7][3]),
#     11: ("Coal Burner", buy_menu[7][6]),
#     12: ("Gas Burner", buy_menu[9][3]),
#     13: ("Gas Burner", buy_menu[9][6]),
#     14: ("Nuclear Reactor", buy_menu[12][3]),
#     15: ("Nuclear Reactor", buy_menu[12][6]),
#     16: ("Thermo Reactor", buy_menu[14][3]),
#     17: ("Thermo Reactor", buy_menu[14][6]),
#     18: ("Fusion Reactor", buy_menu[16][3]),
#     19: ("Fusion Reactor", buy_menu[16][6]),
#     20: ("Tokamak", buy_menu[19][3]),
#     21: ("Tokamak", buy_menu[19][6]),
#     22: ("Stellarator", buy_menu[20][3]),
#     23: ("Stellarator", buy_menu[20][6]),
#     24: ("Ufo Spaceship Reactor", buy_menu[23][3]),
#     25: ("Ufo Spaceship Reactor", buy_menu[23][6]),
#     26: ("Arc Reactor", buy_menu[24][3]),
#     27: ("Arc Reactor", buy_menu[24][6]),
#     28: ("Cosmic Radiation Reactor", buy_menu[27][3]),
#     29: ("Cosmic Radiation Reactor", buy_menu[27][6]),
#     30: ("Geothermal Reactor", buy_menu[28][3]),
#     31: ("Geothermal Reactor", buy_menu[28][6]),
#     32: ("Tesla Reactor", buy_menu[30][3]),
#     33: ("Tesla Reactor", buy_menu[30][6]),
#     34: ("Dark Energy Reactor", buy_menu[32][3]),
#     35: ("Dark Energy Reactor", buy_menu[32][6])
# }

upgrade_menu = {
    1: ("Wind Turbine", 1,3),
    2: ("Wind Turbine", 1,6),
    3: ("Research Center", RESEARCHLAB_UPGRADE,ResearchLab),
    4: ("Office", OFFICE_UPGRADE,Office),
    5: ("Battery", BATTERY_UPGRADE,Battery),
    6: ("Generator", CONVERTER_UPGRADE,EnergyConverter),
    7: ("Generator", CONVERTER_UPGRADE2,EnergyConverter),
    8: ("Solar Panel", 5,3),
    9: ("Solar Panel", 5,6),
    10: ("Coal Burner", 7,3),
    11: ("Coal Burner", 7,6),
    12: ("Gas Burner", 9,3),
    13: ("Gas Burner", 9,6),
    14: ("Nuclear Reactor", 12,3),
    15: ("Nuclear Reactor", 12,6),
    16: ("Thermo Reactor", 14,3),
    17: ("Thermo Reactor", 14,6),
    18: ("Fusion Reactor", 16,3),
    19: ("Fusion Reactor", 16,6),
    20: ("Tokamak", 19,3),
    21: ("Tokamak", 19,6),
    22: ("Stellarator", 20,3),
    23: ("Stellarator", 20,6),
    24: ("Ufo Spaceship Reactor", 23,3),
    25: ("Ufo Spaceship Reactor", 23,6),
    26: ("Arc Reactor", 24,3),
    27: ("Arc Reactor", 24,6),
    28: ("Cosmic Radiation Reactor", 27,3),
    29: ("Cosmic Radiation Reactor", 27,6),
    30: ("Geothermal Reactor", 28,3),
    31: ("Geothermal Reactor", 28,6),
    32: ("Tesla Reactor", 30,3),
    33: ("Tesla Reactor", 30,6),
    34: ("Dark Energy Reactor", 32,3),
    35: ("Dark Energy Reactor", 32,6)
}


upgrade_menu_2 = [RESEARCHLAB_UPGRADE,OFFICE_UPGRADE,BATTERY_UPGRADE,CONVERTER_UPGRADE,CONVERTER_UPGRADE2]

# Game loop
running = True
selected_building = None  # Selected building type (None, CONVERTER, GENERATOR, OFFICE)


current_tier = 1

not_researched_text = font.render(f'   Not Researched    ', True, (0, 0, 0))
ok_text = font.render(f'Ok', True, (0, 0, 0))
not_enough_money_text = font.render(f'   Not Enough Money    ', True, (0, 0, 0))
not_enough_research = font.render(f'   Not Enough Research    ', True, (0, 0, 0))

menu_text = font.render("Buy Menu", True, (255, 255, 255))


dragging = False
test_text = None
state = "Buy"

scroll_offset = 0
scroll_speed = 15
# max_offset_top=0
# max_offset_bottom=1410
current_offset=0


offsets = {
    "Buy": (0 , 1200),
    "Research": (0 , 1150),
    "Upgrade": (0 , 1360)
}







#DEFINE BUTTONS
# buy_button1 = Button(WINDOW_WIDTH - SIDEBAR_WIDTH +15,7* SIDEBAR_ITEM_HEIGHT -55, 100, 30, 'Buy', lambda: print('Button clicked'))
# upgrade_button1 = Button(WINDOW_WIDTH - SIDEBAR_WIDTH +300, 7* SIDEBAR_ITEM_HEIGHT -55, 100, 30, 'Upgrade', lambda: print('Button clicked'))
upgrade_button1  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH +300, 10* SIDEBAR_ITEM_HEIGHT -45, 100, 30, 'Upgrade', lambda: print('Button clicked'))
buy_button1 = Button(WINDOW_WIDTH - SIDEBAR_WIDTH +15, 10* SIDEBAR_ITEM_HEIGHT -45, 100, 30, 'Buy', lambda: print('Button clicked'))
testbutton = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, SIDEBAR_ITEM_HEIGHT , 100, 30, 'Buy')
delete_multiple_button = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 161, 11* SIDEBAR_ITEM_HEIGHT -55 , 100, 30, 'X')
research_button = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 161, 10* SIDEBAR_ITEM_HEIGHT -45, 100, 30, 'Research')
convert_button = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 200, 200 , 30, 'Convert Energy To Money', lambda: print('Button clicked'),(125, 200, 125))
# menu_button1  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 1 * SIDEBAR_ITEM_HEIGHT - 40, 450, 50)
# menu_button2  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 2 * SIDEBAR_ITEM_HEIGHT - 40, 450, 50)
# menu_button3  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 3 * SIDEBAR_ITEM_HEIGHT - 40, 450, 50)
# menu_button4  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 4 * SIDEBAR_ITEM_HEIGHT - 40, 450, 50)
# menu_button5  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 5 * SIDEBAR_ITEM_HEIGHT - 40, 450, 50, "Tier 1 Battery", lambda: print('Button clicked'),(0,80,200),battery_images)
# menu_button5  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 6 * SIDEBAR_ITEM_HEIGHT - 40, 450, 50)
scroll_tracker  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10+450,1 * SIDEBAR_ITEM_HEIGHT - 40, 15, 10,"Tracker")




label_list = ["Heat Generator", "Energy Converter", "Office", "Research Lab","Battery"]
building_list = [HeatGenerator,EnergyConverter,  Office, ResearchLab,Battery]
# upgrade_list = [ GENERATOR_UPGRADE,CONVERTER_UPGRADE, OFFICE_UPGRADE, RESEARCHLAB_UPGRADE,  BATTERY_UPGRADE]
image_list = [generator_menu_images,converter_menu_images,  office_menu_images, researchlab_menu_images, battery_images]


lists_of_buildings =    {
    HeatGenerator: [],
    EnergyConverter: [],
    Office: [],
    ResearchLab: [],
    Battery: []
}

scroll_bar = pygame.Surface((WINDOW_WIDTH - SIDEBAR_WIDTH, 5 * SIDEBAR_ITEM_HEIGHT - 40),pygame.SRCALPHA)
scroll_bar_rect = pygame.Rect(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 1 * SIDEBAR_ITEM_HEIGHT - 40, 450, 400)
# side_bar = pygame.Surface((WINDOW_WIDTH - SIDEBAR_WIDTH, WINDOW_HEIGHT))
# side_bar.fill((200, 200, 200))
# side_bar_rect = pygame.Rect(side_bar.get_rect())

grid_rect = pygame.Rect(0, 0, NUM_TILES_X * TILE_SIZE, NUM_TILES_Y * TILE_SIZE)





# # Camera position
# camera_x = 0
# camera_y = 0
# mouse_dragging = False
# prev_mouse_pos = (0, 0)



button_creator()


x_offset = 0
y_offset = 0
move_x=0
move_y=0
mouse_pos = pygame.mouse.get_pos()
map_x_max = 300
map_y_max = 300





switch_view("Buy",current_tier)
# grid = load_grid("save.json",player,grid)
save_buildings= []


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
  
                print(dragging)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Clicked ", mouse_x//TILE_SIZE, mouse_y//TILE_SIZE)
                # if testbutton.rect.collidepoint(mouse_pos):
                #     print("test")
                
                if research_button.rect.collidepoint(mouse_pos):
                    state = "Research"
                    tab_change(current_offset)
                    current_offset = 0
                    print("Research button clicked")
                    

                # elif previous_button.rect.collidepoint(mouse_pos) and current_tier > 1:
                #     current_tier -=1
                    
                # elif forward_button.rect.collidepoint(mouse_pos) and current_tier < 3:
                #     current_tier +=1

                elif buy_button1.rect.collidepoint(mouse_pos):
                    state = "Buy"
                    tab_change(current_offset)
                    current_offset = 0
                    print("Buy button clicked")
                elif upgrade_button1.rect.collidepoint(mouse_pos):
                    state = "Upgrade"
                    tab_change(current_offset)
                    current_offset = 0
                    print("upgrade button clicked")
                    
                elif delete_multiple_button.rect.collidepoint(mouse_pos):
                    delete_mult()
                                  
                    
                elif convert_button.rect.collidepoint(mouse_pos):
                        # Convert energy to money
                        print("Energy converted to money")
                        player.sell_energy(player.energy)  # Sell all available energy

                        # Update money display after successful conversion
                        money_text = font.render(f'Money: {int(player.money)}', True, (0, 0, 0))
                        
                        
                # Opens buy menu
                elif scroll_bar_rect.collidepoint(mouse_pos) and state == "Buy":



                    for buttons in menu_button_list:
                        if buttons.rect.collidepoint(mouse_pos):
                            selected_building =( buttons.y  //(SIDEBAR_ITEM_HEIGHT - 40))//5+1
                            print("selected: ",buttons.text,"/buy menu: ",buy_menu[selected_building])



                    
                    
                 #opens res menu   
                elif scroll_bar_rect.collidepoint(mouse_pos) and state == "Research":
                    
                    building_researchable = False
                    for buttons in menu_button_list:
                        if buttons.rect.collidepoint(mouse_pos):
                            selected_research = buttons.y//(SIDEBAR_ITEM_HEIGHT - 40)//5+2 
                            print(selected_research)
                            # research_cost = buy_menu[selected_research][1](buy_menu[selected_research][4],buy_menu[selected_research][3],buy_menu[selected_research][0])
                            research_cost = research_costs[selected_research-2]
                            if  buy_menu[selected_research][5] == False and player.research >= research_cost and selected_research < 33:
                                player.research-=research_cost
                                object_list = list(buy_menu[selected_research])
                                object_list[5] = True
                                buy_menu[selected_research] = object_list
                                print("selected: ",buttons.text,"/buy menu: ",buy_menu[selected_research],"/ object list : ",object_list)
                                building_researchable = True
                                break

                            elif buy_menu[selected_research][5] == False and player.research < research_cost :
                                print("not enough research")
                                confirmation_window(not_enough_research,ok_text)
                                break
                            else:
                                # confirmation_window(not_enough_research,ok_text)
                                break




                  # upgrade mne      
                elif scroll_bar_rect.collidepoint(mouse_pos) and state == "Upgrade":
                    
                    
                    for i, button in enumerate(menu_button_list):
                        if button.rect.collidepoint(mouse_pos):
                            money_check = player.money > upgrade_costs[i]
                            if money_check:
                                if 1 < i < 7:
                                    print(player.money,upgrade_costs[i])
                                    player.buy_upgrade(upgrade_costs[i])
                                    upgrade_menu_2[i-2]+=1
                                    upgrade_costs[i]*=2
                                    print("eww",lists_of_buildings[upgrade_menu[i+1][2]])
                                    
                                    for building in lists_of_buildings[upgrade_menu[i+1][2]]:
                                        building.upgrade_production()
                                else :
                                    print("money check ",player.money,upgrade_costs[i],money_check)

                                    player.buy_upgrade(upgrade_costs[i])
                                    # upgrade_list = list(buy_menu[upgrade_menu[i+1][1]])
                                    
                                    upgrade_count = list(buy_menu[upgrade_menu[i+1][1]])
                                    upgrade_count[upgrade_menu[i+1][2]] +=1
                                    buy_menu[upgrade_menu[i+1][1]] = upgrade_count
                                    upgrade_costs[i]*=2
                                    for building in lists_of_buildings[ buy_menu[upgrade_menu[i+1][1]][1]]:
                                        building.upgrade_production()
                                    
                                    
    
                            else:
                                confirmation_window(not_enough_money_text,ok_text)
                                break


                    

                    # Place selected building on the grid turkey_grid
                # elif  selected_building != None and 0 < mouse_pos[0] < NUM_TILES_X*TILE_SIZE+move_x  and 0 < mouse_pos[1] <  NUM_TILES_Y*TILE_SIZE+move_y and grid[(mouse_pos[0]-move_x) // TILE_SIZE][(mouse_pos[1]-move_y) // TILE_SIZE] == TILE_EMPTY and state == "Buy" :
                #     # if dragging == True:
                #     #     print("dragging")
                #     # Place selected building on the grid
                #     grid_x = (mouse_pos[0]-move_x) // TILE_SIZE
                #     grid_y = (mouse_pos[1]-move_y) // TILE_SIZE
                #     print((mouse_pos[1]-current_offset)// TILE_SIZE)
                #                                              #BUY BUILDINGS 
                #     if 0 <= grid_x < NUM_TILES_X and 0 <= grid_y < NUM_TILES_Y :
                #         building_buildable = False

                #         # for i in range(len(menu_button_list)):
                #         #     # research_check_bool = research_check(selected_building,selected_building,(buy_menu[selected_building][5] if selected_building > 2 else True))
                #         research_check_bool = (buy_menu[selected_building][5] if selected_building > 1 else True)
                #         enough_money = player.enough_money(buy_menu[selected_building][1](buy_menu[selected_building][4],buy_menu[selected_building][3],buy_menu[selected_building][0]))
                #         #     print("res_check: ",research_check_bool,"/ money_check: ",enough_money)
                #         #     # print("mwenu",buy_menu[selected_building][5])

                #         if research_check_bool and enough_money :
                #             grid[grid_x][grid_y] = buy_menu[selected_building][1](buy_menu[selected_building][4],buy_menu[selected_building][3],buy_menu[selected_building][0])
                #             lists_of_buildings[buy_menu[selected_building][1]].append(grid[grid_x][grid_y])  
                #             player.buy_energy_generator(buy_menu[selected_building][1](buy_menu[selected_building][4],buy_menu[selected_building][3],buy_menu[selected_building][0]))
                #             print(buy_menu[selected_building][0],"bought")
                #             building_buildable = True
                #             if isinstance(grid[grid_x][grid_y],Battery):
                #                 player.max_energy += grid[grid_x][grid_y].battery_capacity
                            

                #         if not building_buildable:
                #             print("None",research_check_bool, enough_money)

                #             if  research_check_bool and not enough_money:
                #                 print("1",research_check_bool, enough_money)
                #                 confirmation_window(not_enough_money_text,ok_text)
                #             elif not research_check_bool and  enough_money:
                #                 print("2",research_check_bool, enough_money)
                #                 confirmation_window(not_researched_text,ok_text)

                #             elif not research_check_bool and not enough_money:
                #                 print("3",research_check_bool, enough_money)
                #                 confirmation_window(not_researched_text,ok_text)
                elif  selected_building != None and 0 < mouse_pos[0] < 50*TILE_SIZE+move_x  and 0 < mouse_pos[1] <  len(grid[selected_building])*TILE_SIZE+move_y and grid[(mouse_pos[0]-move_x) // TILE_SIZE][(mouse_pos[1]-move_y) // TILE_SIZE] == 1 and state == "Buy" :
                    print("testerterster")
                    # if dragging == True:
                    #     print("dragging")
                    # Place selected building on the grid
                    grid_x = (mouse_pos[0]-move_x) // TILE_SIZE
                    grid_y = (mouse_pos[1]-move_y) // TILE_SIZE
                    print((mouse_pos[1]-current_offset)// TILE_SIZE)
                                                             #BUY BUILDINGS 
                    if 0 <= grid_x < len(grid) and 0 <= grid_y < len(grid[grid_x]):
                        building_buildable = False

                        # for i in range(len(menu_button_list)):
                        #     # research_check_bool = research_check(selected_building,selected_building,(buy_menu[selected_building][5] if selected_building > 2 else True))
                        research_check_bool = (buy_menu[selected_building][5] if selected_building > 1 else True)
                        enough_money = player.enough_money(buy_menu[selected_building][1](buy_menu[selected_building][4],buy_menu[selected_building][3],buy_menu[selected_building][0]))
                        #     print("res_check: ",research_check_bool,"/ money_check: ",enough_money)
                        #     # print("mwenu",buy_menu[selected_building][5])

                        if research_check_bool and enough_money :
                            grid[grid_x][grid_y] = buy_menu[selected_building][1](buy_menu[selected_building][4],buy_menu[selected_building][3],buy_menu[selected_building][0])
                            lists_of_buildings[buy_menu[selected_building][1]].append(grid[grid_x][grid_y])  
                            player.buy_energy_generator(buy_menu[selected_building][1](buy_menu[selected_building][4],buy_menu[selected_building][3],buy_menu[selected_building][0]))
                            print(buy_menu[selected_building][0],"bought")
                            building_buildable = True
                            if isinstance(grid[grid_x][grid_y],Battery):
                                player.max_energy += grid[grid_x][grid_y].battery_capacity
                            

                        if not building_buildable:
                            print("None",research_check_bool, enough_money)

                            if  research_check_bool and not enough_money:
                                print("1",research_check_bool, enough_money)
                                confirmation_window(not_enough_money_text,ok_text)
                            elif not research_check_bool and  enough_money:
                                print("2",research_check_bool, enough_money)
                                confirmation_window(not_researched_text,ok_text)

                            elif not research_check_bool and not enough_money:
                                print("3",research_check_bool, enough_money)
                                confirmation_window(not_researched_text,ok_text)


            elif event.button == 3:  # Right click
                # Sell selected building on the grid
                grid_x = (mouse_pos[0]-move_x) // TILE_SIZE
                grid_y = (mouse_pos[1]-move_y) // TILE_SIZE
                if   0 < mouse_pos[0] < NUM_TILES_X*TILE_SIZE+move_x and 0 < mouse_pos[1] <  NUM_TILES_Y*TILE_SIZE+move_y and grid[grid_x][grid_y] != TILE_EMPTY and  grid[grid_x][grid_y] != TILE_OCEAN: 

                    if  0<= grid_x < NUM_TILES_X and 0 <= grid_y < NUM_TILES_Y:
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
                                
                else :
                    dragging = True
                   

                    x_offset=mouse_pos[0]-move_x
                    y_offset=mouse_pos[1]-move_y
                    

                    print("offset",x_offset,y_offset)
                
            elif event.button == 4 and scroll_bar_rect.collidepoint(mouse_pos)   :  # Mouse wheel up
               
                if current_offset > offsets[state][0]:
                    scroll_offset += scroll_speed
                    current_offset -= scroll_speed
                    # print("scroll up",scroll_offset,current_offset," ",max_offset_top)
                # menu_button1.rect.move(0, scroll_speed)
            elif event.button == 5 and scroll_bar_rect.collidepoint(mouse_pos):  # Mouse wheel down
               if current_offset < offsets[state][1]:
                    scroll_offset -= scroll_speed
                    current_offset += scroll_speed
                    # print("scroll up",scroll_offset,current_offset," ",max_offset_top)
                    
            elif event.button == 4 and 0<mouse_pos[0] < WINDOW_WIDTH-SIDEBAR_WIDTH and 0<mouse_pos[1] < WINDOW_HEIGHT  :  # Mouse wheel up,

                TILE_SIZE = TILE_SIZE+5
            
            elif event.button == 5 and 0<mouse_pos[0] < WINDOW_WIDTH-SIDEBAR_WIDTH and 0<mouse_pos[1] < WINDOW_HEIGHT  :
                TILE_SIZE = TILE_SIZE-5
                if TILE_SIZE < 20:
                    TILE_SIZE = 20
            
            
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                
                if mouse_pos[0]-x_offset < 400 and mouse_pos[0]-x_offset > -1300:
                    move_x = mouse_pos[0] - x_offset
                elif mouse_pos[0]-x_offset > 400:
                    move_x = 400
                elif mouse_pos[0]-x_offset < 900:
                    move_x = -1300
            
                if mouse_pos[1]-y_offset < 400 and mouse_pos[1]-y_offset > -300:
                    move_y = mouse_pos[1] - y_offset
                elif mouse_pos[1]-y_offset > 400:
                    move_y = 400
                elif mouse_pos[1]-y_offset < -300:
                    move_y = -300
                print("move",move_x,move_y)

                dragging = False
    font = pygame.font.Font(None, 24)



    total_energy_sold = 0

    # if not dragging:
    #     x_offset = mouse_pos[0] 
    #     y_offset = mouse_pos[1]
          
            
            
    for office in lists_of_buildings[Office]:
        office.sell_energy(player)
        total_energy_sold += office.energy_sell_rate
        # print("Energy sold",office.energy_sell_rate,"/ Tier",office.tier)
                
    for lab in lists_of_buildings[ResearchLab]:
        lab.research(player)       


    # Display game information
    
    # continent = pygame.Surface((WINDOW_WIDTH - SIDEBAR_WIDTH, WINDOW_HEIGHT))

    
    # pygame.draw.rect(window, (0, 105, 148), (0 , 0, WINDOW_WIDTH - SIDEBAR_WIDTH, WINDOW_HEIGHT)) 
    background_surface = pygame.Surface((WINDOW_WIDTH - SIDEBAR_WIDTH, WINDOW_HEIGHT))
    for x in range(0, WINDOW_WIDTH - SIDEBAR_WIDTH, 50):
        for y in range(0, WINDOW_HEIGHT, 50):
            background_surface.blit(background_image, (x, y))
    window.blit(background_surface, (0,0,WINDOW_WIDTH - SIDEBAR_WIDTH ,WINDOW_HEIGHT))


    tile_image = pygame.transform.scale(pygame.image.load('Data/tile2.jpg'), (TILE_SIZE, TILE_SIZE))
    


 
 
 
 
 
 

    if dragging :
       # Draw tiles and objects
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                rect = pygame.Rect(i * TILE_SIZE+(mouse_pos[0]-x_offset if mouse_pos[0]-x_offset< 400  and mouse_pos[0]-x_offset> -1300 else (400 if mouse_pos[0]-x_offset > -1300 else -1300)) , j * TILE_SIZE+(mouse_pos[1]-y_offset if mouse_pos[1]-y_offset < 400  and mouse_pos[1]-y_offset> -300 else (400 if mouse_pos[1]-y_offset > -300 else -300)), TILE_SIZE, TILE_SIZE)
                if grid[i][j] == 0:
                    pass
                elif isinstance(grid[i][j], EnergyConverter) or isinstance(grid[i][j], HeatGenerator) or isinstance(grid[i][j], Office) or isinstance(grid[i][j], ResearchLab) or isinstance(grid[i][j], Battery):
                    
                    for buildings in buy_menu:
                        if buy_menu[buildings][0] == grid[i][j].name:
                            window.blit(pygame.transform.scale(tile_images[buildings], (TILE_SIZE, TILE_SIZE)), rect)
                            # window.blit(tile_image, rect)
                            # window.blit(buy_menu[buildings][2],(i * TILE_SIZE+5, j * TILE_SIZE+5, TILE_SIZE, TILE_SIZE) )

                elif grid[i][j] == TILE_EMPTY:
                    window.blit(tile_image, rect)
                # else:
                #     # window.blit(background_image, rect)
    else:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                rect = pygame.Rect(i * TILE_SIZE+move_x, j * TILE_SIZE+move_y, TILE_SIZE, TILE_SIZE)
                if grid[i][j] == 0:
                    pass
                elif isinstance(grid[i][j], EnergyConverter) or isinstance(grid[i][j], HeatGenerator) or isinstance(grid[i][j], Office) or isinstance(grid[i][j], ResearchLab) or isinstance(grid[i][j], Battery):
                    
                    for buildings in buy_menu:
                        if buy_menu[buildings][0] == grid[i][j].name:
                            window.blit(pygame.transform.scale(tile_images[buildings], (TILE_SIZE, TILE_SIZE)), rect)
                            # window.blit(tile_image, rect)
                            # window.blit(buy_menu[buildings][2],(i * TILE_SIZE+5, j * TILE_SIZE+5, TILE_SIZE, TILE_SIZE) )

                elif grid[i][j] == TILE_EMPTY:
                    window.blit(tile_image, rect)
                # else:
                    
                #     # window.blit(background_image, rect)
    
    
    
    
        
    # window.blit(converter_menu_images[1], (5, 5,50,50))
    
    
    

    # if building_buildable:
    #     window.blit(buy_menu[selected_building][2],(mouse_x,mouse_y, TILE_SIZE, TILE_SIZE))




        # window.blit(scroll_bar, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 1 * SIDEBAR_ITEM_HEIGHT - 40))


    # window.blit(side_bar, (WINDOW_WIDTH - SIDEBAR_WIDTH, WINDOW_HEIGHT))
    # scroll_bar.convert_alpha()
    # window.blit(scroll_bar, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 1 * SIDEBAR_ITEM_HEIGHT - 40))
    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)) 


    # menu_button1.draw(window)
    # menu_button2.draw(window)
    # menu_button3.draw(window)
    # menu_button4.draw(window)
    # menu_button5.draw(window)
    button_drawer()


    #Draw sidebar
    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH, 0,10 , WINDOW_HEIGHT)) 
    
    #upper line
    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH , 1 * SIDEBAR_ITEM_HEIGHT - 40))
     
    # scroll tracker
    pygame.draw.rect(window, (GRAY), (WINDOW_WIDTH - SIDEBAR_WIDTH+460, 10,15 , WINDOW_HEIGHT)) 
    
    #bottom area
    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH, 9 * SIDEBAR_ITEM_HEIGHT - 40, SIDEBAR_WIDTH , WINDOW_HEIGHT-  SIDEBAR_ITEM_HEIGHT - 40)) 
    
    
    
    switch_view(state,current_tier)
    # pygame.draw.rect(window, (0, 105, 148), scroll_bar_rect)
    window.blit(menu_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 170, 9* SIDEBAR_ITEM_HEIGHT -30))



    
    scroll_tracker.draw(window)
    
    
    
    grid_rect.move_ip(0, -scroll_offset)
    # testbutton.draw(window)
    scroll_offset = 0
    

    # Display game information (money and power)
    money_text = font.render(f'Money: {number_format(int(player.money))}', True, (0, 0, 100))
    energy_text = font.render(f'Energy: {number_format(int(player.energy))}/{int(player.max_energy)}', True, (0, 0,100))
    research_text = font.render(f'Research: {number_format(int(player.research))}', True, (0, 0, 100))
    total_energy_text = font.render(f'Money Per Second: {number_format(int(total_energy_sold*60*2.5))}', True, (0, 0, 100))
    window.blit(money_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 80))
    window.blit(energy_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 175, WINDOW_HEIGHT - 80))
    window.blit(research_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 350, WINDOW_HEIGHT - 80))
    window.blit(total_energy_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 120))
    


    # Blit the bottom bar onto the main window
    # window.blit(bottom_bar, (0, WINDOW_HEIGHT - 50))

    #DRAW BUTTONS
    buy_button1.draw(window)
    upgrade_button1.draw(window)
    # forward_button.draw(window)
    # previous_button.draw(window) 
    delete_multiple_button.draw(window)
    research_button.draw(window)
    convert_button.draw(window)




    # Check if mouse is hovering over a placed building
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pos = pygame.mouse.get_pos()
    
    # coordinates hover
    test = font.render(f'Coordinates: {mouse_x,mouse_y}', True, (0, 0, 0))
    window.blit(test,( mouse_pos[0], mouse_pos[1]))


    grid_x = (mouse_pos[0]-move_x )// TILE_SIZE
    grid_y = (mouse_pos[1]-+move_y) // TILE_SIZE
    if 0 <= grid_x < len(grid) and 0 <= grid_y < len(grid[grid_x]):
        # if grid[grid_x][grid_y] != TILE_EMPTY and grid[grid_x][grid_y] != TILE_OCEAN:
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