import pygame
import threading
import json
import random
from button_file import Button
from player import Player
from heatGenerator import HeatGenerator
from energyConverter import EnergyConverter
from office import Office
from researchLab import ResearchLab
from battery import Battery
from objects import *

# from turkey_grid import turkey_grid
def unlock_region(grid, region, region_cost):
    font = pygame.font.Font(None, 36)
    if player.money >= region_cost:
        
            confirmation_text = font.render(f"  Do you want to unlock this region for {number_format(region_cost)} money?  ", True, (0, 0, 0))
            
            yes_text = font.render("Yes", True, (0, 0, 0))
            no_text = font.render("No", True, (0, 0, 0))
                
            confirmation = confirmation_window(confirmation_text,yes_text,no_text)
            if confirmation:
                player.money -= region_cost
                new_region = (region[0], region[1], False)
                index = regions.index(region)
                regions[index] = new_region    
                for row in range(region[0].start, region[0].stop):
                    for col in range(region[1].start, region[1].stop):
                        if grid[row][col] == TILE_CLOUDY:
                            grid[row][col] = TILE_EMPTY
                return True
            else: 
                return False

    else:            
        confirmation_window(not_enough_money_text,ok_text)
        return False
   
    
   
        
        
    print("TESTING TESTINGGG")
    
def unlock_all_research():
    for i in range(len(buy_menu)):
        research = list(buy_menu[i+1])
        research[5] = True
        buy_menu[i+1] = research

                
def tab_change(current_offset):
    
    scroll_tracker.rect.y = 1 * SIDEBAR_ITEM_HEIGHT - 40
    for button in menu_button_list:
        button.rect.move_ip(0,current_offset)

    
def handle_destruction(building):
    explosion_sound.play()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == building:
                grid[i][j] = TILE_EMPTY
                x = i * TILE_SIZE + move_x
                y = j * TILE_SIZE + move_y
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
     


def confirmation_window(confirmation_text,yes_text=None,no_text=None):    
        
        
        
    confirmation_rect = confirmation_text.get_rect(center=(WINDOW_WIDTH // 2+10, WINDOW_HEIGHT // 2+10))
    confirmation_rect.inflate_ip(0, 15) # increase the size of the rectangle by 50 pixels in both directions
    
    # Draw the confirmation box
    pygame.draw.rect(window, (41, 196, 170), confirmation_rect,border_radius = 10)
    pygame.draw.rect(window, (0, 0, 0), confirmation_rect, 2,border_radius = 10)
    text_x = confirmation_rect.centerx - confirmation_text.get_width() // 2
    text_y = confirmation_rect.centery - confirmation_text.get_height() // 2
    window.blit(confirmation_text, (text_x, text_y))
    
    if  yes_text != None and no_text == None:
        yes_button_rect = pygame.Rect(WINDOW_WIDTH // 2 -30, WINDOW_HEIGHT // 2 +30, 80, 30)
        pygame.draw.rect(window, (0, 255, 0), yes_button_rect,border_radius = 10)
        text_x = yes_button_rect.centerx - yes_text.get_width() // 2
        text_y = yes_button_rect.centery - yes_text.get_height() // 2
        window.blit(yes_text,  (text_x, text_y))
        
        # yes_button = Button(WINDOW_WIDTH // 2 -25, WINDOW_HEIGHT // 2 +25, 80, 35, 'Yees', lambda: "test123",(0, 255, 0) ,border_radius = 10)
        # yes_button.draw(window,scroll_offset)

        
    elif yes_text != None:
        yes_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT // 2 + 40, 60, 40)
        pygame.draw.rect(window, (0, 255, 0), yes_button_rect,border_radius = 10)
        window.blit(yes_text, (yes_button_rect.x + 10, yes_button_rect.y + 5))
        # yes_button = Button(WINDOW_WIDTH // 2 -25, WINDOW_HEIGHT // 2 +25, 80, 35, 'Yees', lambda: "test123",(0, 255, 0),border_radius = 10)
        # yes_button.draw(window,scroll_offset)

    if no_text != None:
        no_button_rect = pygame.Rect(WINDOW_WIDTH // 2 + 20, WINDOW_HEIGHT // 2 + 40, 60, 40)
        pygame.draw.rect(window, (255, 0, 0), no_button_rect,border_radius = 10)
        window.blit(no_text, (no_button_rect.x + 15, no_button_rect.y + 5))

    
    
    # yes_text = font.render("Yes", True, (0, 0, 0))
    # no_text = font.render("No", True, (0, 0, 0))
    

    
    pygame.display.flip()  
    frame_count=0
    start_time = pygame.time.get_ticks()

    while True:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_button_rect.collidepoint(mouse_pos) :
                    print("Skipped ",int(elapsed_time/0.250)/4," seconds")
                    time_skip(int(elapsed_time/0.250))
                    return True
                elif no_text != None and no_button_rect.collidepoint(mouse_pos):
                    time_skip(int(elapsed_time/0.250))
                    return False
        
       
        frame_count += 1  # Increment the frame counter
        if frame_count >= 60 and no_text == None:  # Check if 60 frames have passed
            time_skip(4)
            return False
        pygame.time.delay(16)
        
def switch_view(state, tier):

    
    if state == "Buy":
    
        
        menu_text = font.render("Buy Menu",True,(255,255,255))
        window.blit(menu_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 210, 9* SIDEBAR_ITEM_HEIGHT -30))

        for i in buy_menu:
            if buy_menu[i][5] == False:
                menu_button_list[i-1].button_update(text=f'{buy_menu[i][0]} (${number_format(buy_menu[i][1](buy_menu[i][4],1,buy_menu[i][0]).cost)}) (Not Researched)',color=(0,80,120), image = pygame.transform.scale(tile_images[i],(40,40)))
            else:
                menu_button_list[i-1].button_update(text=f'{buy_menu[i][0]} (${number_format(buy_menu[i][1](buy_menu[i][4],1,buy_menu[i][0]).cost)})' ,image = pygame.transform.scale(tile_images[i],(40,40)))

 
         
         
                                                                        
        
    elif state == "Upgrade":


        building_index = []
        for key, value in buy_menu.items():
            if value[1] == HeatGenerator:
                building_index.append(key)
        

        # menu_button_list[0].button_update(text=f'{buy_menu[1][0]}: Increase Production by %50 (${number_format(upgrade_costs[0])})', image = pygame.transform.scale(tile_images[1],(40,40)))
        # menu_button_list[1].button_update(text=f'{buy_menu[1][0]}: Increase Lifetime by %100 (${number_format(upgrade_costs[1])})', image = pygame.transform.scale(tile_images[1],(40,40)))
        # menu_button_list[2].button_update(text=f'Research Center: Increase Research Rate by %25 (${number_format(upgrade_costs[2])})', image = pygame.transform.scale(tile_images[2],(40,40)))
        # menu_button_list[3].button_update(text=f'Office: Increase Sell Rate by %50 (${number_format(upgrade_costs[3])})', image = pygame.transform.scale(tile_images[4],(40,40)))
        # menu_button_list[4].button_update(text=f'Battery: Increase Max Energy by %100 (${number_format(upgrade_costs[4])})', image = pygame.transform.scale(tile_images[3],(40,40)))
        # menu_button_list[5].button_update(text=f'Generator: Increase Max Heat %100 (${number_format(upgrade_costs[5])})', image = pygame.transform.scale(tile_images[6],(40,40)))
        # menu_button_list[6].button_update(text=f'Generator: Increase Conversion Rate by %25 (${number_format(upgrade_costs[6])})', image = pygame.transform.scale(tile_images[6],(40,40)))
        menu_button_list[0].button_update(text=f'{buy_menu[1][0]}: Production +%50 (${number_format(upgrade_costs[0])})', image = pygame.transform.scale(tile_images[1],(40,40)))
        menu_button_list[1].button_update(text=f'{buy_menu[1][0]}: Lifetime +%100 (${number_format(upgrade_costs[1])})', image = pygame.transform.scale(tile_images[1],(40,40)))
        menu_button_list[2].button_update(text=f'Research Center: Research Rate +%25 (${number_format(upgrade_costs[2])})', image = pygame.transform.scale(tile_images[2],(40,40)))
        menu_button_list[3].button_update(text=f'Office: Sell Rate +%50 (${number_format(upgrade_costs[3])})', image = pygame.transform.scale(tile_images[4],(40,40)))
        menu_button_list[4].button_update(text=f'Battery: Max Energy +%100 (${number_format(upgrade_costs[4])})', image = pygame.transform.scale(tile_images[3],(40,40)))
        menu_button_list[5].button_update(text=f'Generator: Max Heat +%100 (${number_format(upgrade_costs[5])})', image = pygame.transform.scale(tile_images[6],(40,40)))
        menu_button_list[6].button_update(text=f'Generator: Conversion Rate +%25 (${number_format(upgrade_costs[6])})', image = pygame.transform.scale(tile_images[6],(40,40)))


        del building_index[0]

        i = 7
        for key in building_index:
            menu_button_list[i].button_update(text=f'{buy_menu[key][0]}: Production +%50 (${number_format(upgrade_costs[i])})', image = pygame.transform.scale(tile_images[key],(40,40)))
            menu_button_list[i+1].button_update(text=f'{buy_menu[key][0]}: Lifetime +%100 (${number_format(upgrade_costs[i+1])})', image = pygame.transform.scale(tile_images[key],(40,40)))
            

            i+=2
        menu_text = font.render("Upgrade Menu",True,(255,255,255))
        window.blit(menu_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 195, 9* SIDEBAR_ITEM_HEIGHT -30))

      
      
      
      
      
      
      
        


    elif state == "Research":
        
        menu_text = font.render("Research Menu",True,(255,255,255))
        window.blit(menu_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 195, 9* SIDEBAR_ITEM_HEIGHT -30))

        # menu_button_list[0].button_update(text=f'{buy_menu[2][0]} (${buy_menu[2][1](buy_menu[2][4],1,buy_menu[2][0]).cost*2})', image = pygame.transform.scale(tile_images[2],(40,40)))

        for i in range(len(buy_menu)-1):

            # menu_button_list[i-1].button_update(text=f'{buy_menu[i][0]} (${buy_menu[i][1](current_tier,1,buy_menu[i][0]).cost})', image = buy_menu[i][2])
            if buy_menu[i+2][5] == False:
                menu_button_list[i].button_update(text=f'{buy_menu[i+2][0]} ({number_format(research_costs[i])} Research Points)', image = pygame.transform.scale(tile_images[i+2],(40,40)))
            else:
                menu_button_list[i].button_update(text = f'Research Bought!')

        menu_button_list[31].button_update()
 
          
    # energy_gen_thread = threading.Thread(target=energy_gen)
    # energy_gen_thread.start()
# Create two threads
 
def energy_gen():
    if grid != None:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if isinstance(grid[i][j], HeatGenerator) and grid[i][j].tier != 1:
                    # Generate heat in adjacent tiles
                    if i+1 < 1200 and isinstance(grid[i+1][j], EnergyConverter):
                        grid[i+1][j].convert_heat(grid[i][j].generate_heat(player),player,handle_destruction)
                    if i-1 >= 0 and isinstance(grid[i-1][j], EnergyConverter):
                        grid[i-1][j].convert_heat(grid[i][j].generate_heat(player),player,handle_destruction)
                    if j+1 < 800 and isinstance(grid[i][j+1], EnergyConverter):
                        grid[i][j+1].convert_heat(grid[i][j].generate_heat(player),player,handle_destruction)
                    if  j-1 >= 0 and isinstance(grid[i][j-1], EnergyConverter):
                        grid[i][j-1].convert_heat(grid[i][j].generate_heat(player),player,handle_destruction)
                elif isinstance(grid[i][j], HeatGenerator) and grid[i][j].tier == 1 :
                    grid[i][j].generate_heat(player)


#     energy_gen_thread = threading.Thread(target=refresh_display)
#     energy_gen_thread.start()
# def refresh_display():
#     pygame.display.flip()


def sell_building(Building):
    
    font = pygame.font.Font(None, 36)
    confirmation_text = font.render(f"  Do you want to sell this building for {number_format(Building.cost)} money?  ", True, (0, 0, 0))
    
   
    yes_text = font.render("Yes", True, (0, 0, 0))
    no_text = font.render("No", True, (0, 0, 0))
    
    
    confirmation = confirmation_window(confirmation_text,yes_text,no_text)
    
    if confirmation:
        player.money += Building.cost
        if isinstance(Building, Battery):
            player.max_energy -= Building.battery_capacity
            Building.battery_capacity = 0
        return True
    else: 
        return False
    
    
def delete_mult():
    dragging2 = False        
    selected_tiles = []
    x_of_building =[]
    y_of_building =[]
    delete_multiple_mode = True
    font1 = pygame.font.Font(None, 40)
    label_text = font1.render('SELLING MULTIPLE BUILDINGS', True, (255, 0, 0), (0, 0, 0))
    window.blit(label_text, ((WINDOW_WIDTH - SIDEBAR_WIDTH)/3 ,0))

    label_text1 = font1.render('Select Buildings To Sell, Right Click To Sell Or Cancel', True, (255, 0, 0), (0, 0, 0))
    window.blit(label_text1, ((WINDOW_WIDTH - SIDEBAR_WIDTH)/5 , WINDOW_HEIGHT-label_text1.get_height() ))
    pygame.display.flip()

    while delete_multiple_mode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                delete_multiple_mode = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging2 = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:

                    dragging2 = False

                if event.button == 3:  # Right click
                    # Cancel selection
                    dragging2 = False
                    delete_multiple_mode = False
        if dragging2:
            mouse_pos = pygame.mouse.get_pos()
            grid_x = (mouse_pos[0]-move_x) // TILE_SIZE
            grid_y = (mouse_pos[1]-move_y) // TILE_SIZE
            if (0 <= grid_x < len(grid)*TILE_SIZE+move_x and 0 <= grid_y < len(grid[grid_x])*TILE_SIZE+move_y) and grid[grid_x][grid_y] != TILE_EMPTY and grid[grid_x][grid_y] != TILE_OCEAN and grid[grid_x][grid_y] != TILE_CLOUDY:  # Left click
                if (grid[grid_x][grid_y] not in selected_tiles):
                    x_of_building.append(grid_x)
                    print(grid_x, grid_y)
                    y_of_building.append(grid_y)
                    selected_tiles.append((grid[grid_x][grid_y]))
                    rect = pygame.Rect(grid_x * TILE_SIZE+move_x, grid_y * TILE_SIZE+move_y, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(window, HIGHLIGHT_COLOR, rect, 2,border_radius = 10) # the last parameter is the thickness of the border
                    pygame.display.flip()
                # pygame.display.update(rect)
                    
    confirmation_text_object = player.sell_multiple_buildings(selected_tiles)
    if(selected_tiles != [] and confirmation_window(confirmation_text_object[0],confirmation_text_object[1],confirmation_text_object[2]) ):
        print(selected_tiles)
        for i in range(len(selected_tiles)):
            player.money += selected_tiles[i].cost
            grid[x_of_building[i]][y_of_building[i]] = TILE_EMPTY

#delete_mult_thread = threading.Thread(target=delete_mult)


def button_creator():
    
    for i in range(35):
        if i < 32:
            menu_button_list.append(Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, (i+1) * SIDEBAR_ITEM_HEIGHT - 40, 450, 50, text=f'{buy_menu[i+1][0]} (${buy_menu[i+1][1](buy_menu[i+1][4],1,buy_menu[i+1][0]).cost})',image=buy_menu[i+1][2]))
        else :
            menu_button_list.append(Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, (i+1) * SIDEBAR_ITEM_HEIGHT - 40, 450, 50))

        print(menu_button_list[i].text,menu_button_list[i].rect)
        
def region_button_creator():
    
    for i in range(len(regions)-4):
        if i!=1:
            middle_of_region = find_middle_of_region(regions[i])
            region_button_list.append(Button(middle_of_region[0]*TILE_SIZE, middle_of_region[1]*TILE_SIZE, TILE_SIZE*4, TILE_SIZE*2, text=f'Region Cost: ${number_format(region_costs[i])}',command=lambda i=i: unlock_region(grid, regions[i], region_costs[i]),border_radius = 20))
            print(middle_of_region,"ADSAKDNASKJ")
            print(region_button_list[i].text,region_button_list[i].rect)
        else :
            region_button_list.append(Button(0, 0, 0, 0, text='NULL'))
            
        
def find_middle_of_region(region):
    row_start, row_stop = region[0].start, region[0].stop
    col_start, col_stop = region[1].start, region[1].stop

    middle_row = (row_start + row_stop) // 2
    middle_col = (col_start + col_stop) // 2

    return middle_row, middle_col

region_costs = [10000,10000*10 , 10000*100, 10000*1000, 10000*10000, 10000*100000, 10000*1000000, 10000*10000000]
region_button_coords = {
    0: (6, 5),
    1: (18, 15),
    2: (30, 5),
    3: (37, 5),
    4: (6, 12),
    5: (18, 12),
    6: (30, 12),
    7: (37, 12)
    # 8: (6, 25),
    # 9: (30, 25),
    # 10: (18, 25),
    # 11: (42, 25)
    
}
def button_drawer():
    for i,button in enumerate(region_button_list):
        if regions[i][2] == True:
            button.draw(window,x_offset = x_offset, y_offset = y_offset,move_x = move_x,move_y = move_y, dragging = dragging,TILE_SIZE =TILE_SIZE,x_coord = region_button_coords[i][0],y_coord = region_button_coords[i][1])
    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)) 

    for button in menu_button_list:

        button.draw(window,scroll_offset) 
   
def heat_bar_updater():
    if grid != None:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if isinstance(grid[i][j], EnergyConverter):
                    # Generate heat in adjacent tiles
                    if dragging:
                        grid[i][j].draw_bar(window,TILE_SIZE,8,(i*TILE_SIZE+(mouse_pos[0]-x_offset if mouse_pos[0]-x_offset< 400  and mouse_pos[0]-x_offset> -1300 else (400 if mouse_pos[0]-x_offset > -1300 else -1300)),(j+1)*TILE_SIZE-9+(mouse_pos[1]-y_offset if mouse_pos[1]-y_offset < 400  and mouse_pos[1]-y_offset > -300 else (400 if mouse_pos[1]-y_offset > -300 else -300))),(0,80,200),(100,180,120)) 
                    else:
                        grid[i][j].draw_bar(window,TILE_SIZE,8,(i*TILE_SIZE+move_x,(j+1)*TILE_SIZE+move_y-9),(0,80,200),(100,180,120)) 

                  
def life_cycle_updater():
    if grid != None:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if isinstance(grid[i][j], HeatGenerator):
                    if dragging:
                        grid[i][j].draw_bar(window,TILE_SIZE,8,(i*TILE_SIZE+(mouse_pos[0]-x_offset if mouse_pos[0]-x_offset< 400  and mouse_pos[0]-x_offset> -1300 else (400 if mouse_pos[0]-x_offset > -1300 else -1300)),(j+1)*TILE_SIZE-9+(mouse_pos[1]-y_offset if mouse_pos[1]-y_offset < 400  and mouse_pos[1]-y_offset > -300 else (400 if mouse_pos[1]-y_offset > -300 else -300))),(252, 186, 3),(100,180,120)) 
                    else:
                        grid[i][j].draw_bar(window,TILE_SIZE,8,(i*TILE_SIZE+move_x,(j+1)*TILE_SIZE+move_y-9),(252, 186, 3),(100,180,120)) 

                        
combined_dict = {}
def dict_combiner():
    for key, value in buy_menu.items():
        combined_dict[value[0]] = (value,) + (tile_images[key],)

    print(combined_dict)
                
    
def number_format(number):
    numbers = ["0","K","M","B","T","AA","AB","AC","AD","AE","AF","AG","AH","BA","BB","BC"]    
    for i in range(len(numbers)):
        if number < 1000**(i+1):
            if i > 0:
                return f"{number/1000**i:.2f}{numbers[i]}"
            else:
                return str(number)
    return f"{number/1000**(len(numbers)-1):.2f}{numbers[-1]}"
   
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


def build_building(grid_x,grid_y):
        print("test")
        building_buildable = False

        # for i in range(len(menu_button_list)):
        research_check_bool = (buy_menu[selected_building][5] if selected_building > 1 else True)
        enough_money = player.enough_money(buy_menu[selected_building][1](buy_menu[selected_building][4],buy_menu[selected_building][3],buy_menu[selected_building][0]))
        #     print("res_check: ",research_check_bool,"/ money_check: ",enough_money)
        #     # print("mwenu",buy_menu[selected_building][5])

        if research_check_bool and enough_money :
            click_sound.play()
            print(buy_menu[selected_building][0])
            grid[grid_x][grid_y] = buy_menu[selected_building][1](buy_menu[selected_building][4],buy_menu[selected_building][3],buy_menu[selected_building][0],buy_menu[selected_building][6])
            
            print(buy_menu[selected_building][3])
            lists_of_buildings[buy_menu[selected_building][1]].append((grid[grid_x][grid_y],grid_x*TILE_SIZE+move_x,grid_y*TILE_SIZE+move_y))  
            player.buy_energy_generator(buy_menu[selected_building][1](buy_menu[selected_building][4],buy_menu[selected_building][3],buy_menu[selected_building][0],buy_menu[selected_building][6]))
            print(buy_menu[selected_building][0],"bought")
            building_buildable = True
            if isinstance(grid[grid_x][grid_y],Battery):
                player.max_energy += grid[grid_x][grid_y].battery_capacity
            

        if not building_buildable:
            print("None",research_check_bool, enough_money)
            dragging2 = False
            if  research_check_bool and not enough_money:
                print("1",research_check_bool, enough_money)
                confirmation_window(not_enough_money_text,ok_text)
            elif not research_check_bool and  enough_money:
                print("2",research_check_bool, enough_money)
                confirmation_window(not_researched_text,ok_text)

            elif not research_check_bool and not enough_money:
                print("3",research_check_bool, enough_money)
                confirmation_window(not_researched_text,ok_text)
                
                
def quick_build():
        
    empty_tile_count = 0
    for sublist in grid:
        empty_tile_count += sublist.count(TILE_EMPTY)
            
            
    while True:
        
        row = random.choice(range(46))
        column = random.choice(range(30))
        if empty_tile_count == 0:
            break
        if grid[row][column] == TILE_EMPTY:
            build_building(row,column)
            break  
        
    
def quick_revive():
    found = False

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print(grid[i][j])

            if isinstance(grid[i][j], HeatGenerator) and grid[i][j].life_left == 0:
                grid[i][j].life_left = grid[i][j].life_cycle
                found = True
                break
        if found:
            break        
                
                
                
def time_skip(skip_amount):
    
    for i in range(skip_amount):
        previous_money = player.money
        for office in lists_of_buildings[Office]:
            office[0].sell_energy(player)
            total_energy_sold += office[0].energy_sell_rate
        new_money = player.money
        money_gen_per_second = new_money - previous_money
        previous_energy = player.energy
        energy_gen()
        new_energy = player.energy
        energy_gen_per_second = new_energy - previous_energy

            # print("Energy sold",office.energy_sell_rate,"/ Tier",office.tier)
        previous_research = player.research
        for lab in lists_of_buildings[ResearchLab]:
            lab[0].research(player) 
        new_research = player.research
        research_gen_per_second = new_research - previous_research
        
        for generator in lists_of_buildings[HeatGenerator]:
            generator[0].update_life_left()
            




















def convert_buy_menu_to_list():
     for i in range(len(buy_menu)):
        research = list(buy_menu[i+1])
        research[5] = research[5]
        buy_menu[i+1] = research

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
TILE_CLOUDY = 5






# Initialize pygame
pygame.init()


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


heat_grid = [[0 for _ in range(NUM_TILES_Y)] for _ in range(NUM_TILES_X)]  # Heat grid for generators


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

background_image = pygame.transform.scale(pygame.image.load('Data/background.jpg'), (50, 50))
# turkey_grid = pygame.transform.scale(pygame.image.load('Data/turkey_map.png'), (50, 50))


               # 1   2    3    4    5    6    7    8    9    10     11        12       13         14        15          16          17              18              19              20              21                       22                         23                  24                  25                      26                          27                                  28                      29                                       30                                       31                          32                          33                                  34                                    35
# upgrade_costs = [250,15,25000,1000,300,1000,400,1000,10000,125000,5000000,20000000,125000000,5000000000,50000000000,100000000000,500000000000,100000000000000,500000000000000,100000000000000000,500000000000000000,100000000000000000000,500000000000000000000,50000000000000000000000,250000000000000000000000,20000000000000000000000000,100000000000000000000000000,20000000000000000000000000000,100000000000000000000000000000,20000000000000000000000000000000,100000000000000000000000000000000,20000000000000000000000000000000000,100000000000000000000000000000000000,20000000000000000000000000000000000000,100000000000000000000000000000000000000]
upgrade_costs = []
for i in range(35):
    upgrade_costs.append(500*(i+1))
    
    
research_costs = []

for i in range(35):
    # research_costs.append(500*(i**8)+50)
    research_costs.append(500*(i**3)+50)


menu_button_list = []


buy_menu_tags= ["name","class","image","upgrade1","tier","research","upgrade2"]


region_button_list = []

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

buy_menu_item_types = {}

for key, value in buy_menu.items():
    if value[1] == HeatGenerator:
        buy_menu_item_types[key] = "HeatGenerator"
    if value[1] == EnergyConverter:
        buy_menu_item_types[key] = "Generator"
    if value[1] == Office:
        buy_menu_item_types[key] = "Office"
    if value[1] == ResearchLab:
        buy_menu_item_types[key] = "Research Center"
    if value[1] == Battery:
        buy_menu_item_types[key] = "Battery"
    

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

not_researched_text = font.render(f'   Not Researched Yet!    ', True, (0, 0, 0))
ok_text = font.render(f'Ok', True, (0, 0, 0))
not_enough_money_text = font.render(f'   Not Enough Money!    ', True, (0, 0, 0))
not_enough_research = font.render(f'   Not Enough Research Points!    ', True, (0, 0, 0))

menu_text = font.render("Buy Menu", True, (255, 255, 255))


dragging = False
dragging2 = False
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



# MENU BUTTONS



buy_button1 = Button(WINDOW_WIDTH - SIDEBAR_WIDTH +30, 10* SIDEBAR_ITEM_HEIGHT -45, 100, 30, 'Buy', lambda: print('Button clicked'),border_radius = 10)
testbutton = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, SIDEBAR_ITEM_HEIGHT , 100, 30, 'Buy')
delete_multiple_button = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 150, 11* SIDEBAR_ITEM_HEIGHT -55 , 200, 30, 'Delete Multiple Buildings',border_radius = 10)
research_button = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 200, 10* SIDEBAR_ITEM_HEIGHT -45, 100, 30, 'Research',border_radius = 10)
upgrade_button1  = Button(WINDOW_WIDTH - SIDEBAR_WIDTH +370, 10* SIDEBAR_ITEM_HEIGHT -45, 100, 30, 'Upgrade', lambda: click_sound.play(),border_radius = 10)

convert_button = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 200, 220 , 30, 'Convert Energy To Money (M)', lambda: print('Button clicked'),(125, 200, 125),border_radius = 10)
quickplace_button = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 150, 220 , 30, 'Quickly Place a Building (Q)', lambda: print('Button clicked'),(125, 200, 125),border_radius = 10)
quickrevive_button = Button(WINDOW_WIDTH - SIDEBAR_WIDTH + 255, WINDOW_HEIGHT - 150, 230 , 30, 'Quickly Revive a Generator (R)', lambda: print('Button clicked'),(125, 200, 125),border_radius = 10)

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
coords_of_buildings = []

scroll_bar = pygame.Surface((WINDOW_WIDTH - SIDEBAR_WIDTH, 5 * SIDEBAR_ITEM_HEIGHT - 40),pygame.SRCALPHA)
scroll_bar_rect = pygame.Rect(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 1 * SIDEBAR_ITEM_HEIGHT - 40, 450, 400)
# side_bar = pygame.Surface((WINDOW_WIDTH - SIDEBAR_WIDTH, WINDOW_HEIGHT))
# side_bar.fill((200, 200, 200))
# side_bar_rect = pygame.Rect(side_bar.get_rect())

grid_rect = pygame.Rect(0, 0, NUM_TILES_X * TILE_SIZE, NUM_TILES_Y * TILE_SIZE)





click_sound =   pygame.mixer.Sound("Data/click_sound.mp3")
click_sound.set_volume(0.4)
explosion_sound = pygame.mixer.Sound("Data/explosion_sound.mp3")
explosion_sound.set_volume(0.4)

button_creator()
region_button_creator()

x_offset = 0
y_offset = 0
move_x=0
move_y=0
mouse_pos = pygame.mouse.get_pos()
map_x_max = 300
map_y_max = 300

energy_gen2 = pygame.USEREVENT + 1
pygame.time.set_timer(energy_gen2, 250)

energy_gen_per_second= 0
money_gen_per_second= 0
research_gen_per_second = 0
switch_view("Buy",current_tier)
# grid = load_grid("save.json",player,grid)
save_buildings= []
dict_combiner()
convert_buy_menu_to_list()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #when m is pressed press the convert_button
        elif event.type == energy_gen2:
            # print("this should be printed every second")
            previous_money = player.money
            for office in lists_of_buildings[Office]:
                office[0].sell_energy(player)
                total_energy_sold += office[0].energy_sell_rate
            new_money = player.money
            money_gen_per_second = new_money - previous_money
            previous_energy = player.energy
            energy_gen()
            new_energy = player.energy
            energy_gen_per_second = new_energy - previous_energy

                # print("Energy sold",office.energy_sell_rate,"/ Tier",office.tier)
            previous_research = player.research
            for lab in lists_of_buildings[ResearchLab]:
                lab[0].research(player) 
            new_research = player.research
            research_gen_per_second = new_research - previous_research
            
            for generator in lists_of_buildings[HeatGenerator]:
                generator[0].update_life_left()
            
            #lifetime decrease
            
            
        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_m:
                player.sell_energy(player.energy) 
                
            if event.key == pygame.K_r:
                # while True:
                quick_revive()
                # found = False

                # for i in range(len(grid)):
                #     for j in range(len(grid[i])):
                #         print(grid[i][j])

                #         if isinstance(grid[i][j], HeatGenerator) and grid[i][j].life_left == 0:
                #             grid[i][j].life_left = grid[i][j].life_cycle
                #             found = True
                #             break
                #     if found:
                #         break

                    # row = random.choice(range(46))
                    # column = random.choice(range(30))
                    # print(grid[row][column])

                    # if revive_iteration_count == 50:
                    #     break
                    # revive_iteration_count += 1
                    # if isinstance(grid[row][column],HeatGenerator) and grid[row][column].life_left==0:
                    #     grid[row][column].life_left = grid[row][column].life_cycle
                    #     break
                    
            if event.key == pygame.K_q:
                # build_building()
                # empty_tile_count = 0
                # for sublist in grid:
                #     empty_tile_count += sublist.count(TILE_EMPTY)
                        
                        
                # while True:
                    
                #     row = random.choice(range(46))
                #     column = random.choice(range(30))
                #     if empty_tile_count == 0:
                #         break
                #     if grid[row][column] == TILE_EMPTY:
                #         build_building(row,column)
                #         break
                quick_build()

                
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
                # if 0<mouse_pos[0]<1200 and 0<mouse_pos[1]<800:
                #     player.generate_energy(1)
                
                
                if research_button.rect.collidepoint(mouse_pos):
                    state = "Research"
                    #unlocks_all_research
                    #unlock_all_research()
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
                    
                    #delete_mult_thread.start()
                    delete_mult()
                                  
                    
                elif convert_button.rect.collidepoint(mouse_pos):
                        # Convert energy to money
                        print("Energy converted to money")
                        player.sell_energy(player.energy)  # Sell all available energy

                        # Update money display after successful conversion
                        money_text = font.render(f'Money: {int(player.money)}', True, (0, 0, 0))
                        
                elif quickplace_button.rect.collidepoint(mouse_pos):
                    quick_build()
                  
                elif quickrevive_button.rect.collidepoint(mouse_pos):
                    quick_revive()
                       
                       
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




                  # upgrade logic      
                elif scroll_bar_rect.collidepoint(mouse_pos) and state == "Upgrade":
                    
                    
                      for i, button in enumerate(menu_button_list):
                        if button.rect.collidepoint(mouse_pos):
                            money_check = player.money > upgrade_costs[i]
                            if money_check:
                                if 1 < i < 7:
                                    for key, value in buy_menu.items():
                                        if buy_menu_item_types[key] == button.text.split(":")[0]:
                                            

                                            buy_menu[key][3] +=1
                                    player.buy_upgrade(upgrade_costs[i])
                                    upgrade_costs[i]*=(int(button.text.split("%")[1].split(" ")[0])*2/100)+1
                                    print((int(button.text.split("%")[1].split(" ")[0])*2/100)+1)
                                    # upgrade_menu_2[i-2]+=1
                                    # upgrade_costs[i]*=2
                                    # print(buy_menu[i+1])
                                    # buy_menu[f'{button.text.split(":")[0]}'][3] +=1
                                    # print(buy_menu[f'{button.text.split(":")[0]}'])
                                    # print("eww",lists_of_buildings[f'{upgrade_menu[button.text.split(":")[0]][2]}'])
                                    # print(button.text.split(":")[0])
                                   
                                    for building in lists_of_buildings[upgrade_menu[i+1][2]]:
                                        if button.text.split(":")[0] == "Battery":
                                            player.max_energy -= building[0].battery_capacity
                                            building[0].upgrade_production()
                                            player.max_energy += building[0].battery_capacity
                                        elif button.text.split(":")[0] == "Generator":
                                            if "Heat" in button.text:
                                                print("building",building[0].name)
                                                building[0].upgrade_max_heat()
                                            elif "Conversion" in button.text:
                                                print("building",building[0].name)

                                                building[0].upgrade_production()
                                                
                                        else: 
                                            building[0].upgrade_production()

                                    break
                                else :
                                    print("money check ",player.money,upgrade_costs[i],money_check)

                                    player.buy_upgrade(upgrade_costs[i])
                                    # # upgrade_list = list(buy_menu[upgrade_menu[i+1][1]])
                                    
                                    upgrade_count = list(buy_menu[upgrade_menu[i+1][1]])
                                    upgrade_count[upgrade_menu[i+1][2]] +=1
                                    buy_menu[upgrade_menu[i+1][1]] = upgrade_count
                                    upgrade_costs[i]*=(int(button.text.split("%")[1].split(" ")[0])*2/100)+1
                                    print((int(button.text.split("%")[1].split(" ")[0])*2/100)+1)
                                    # for building in lists_of_buildings[ buy_menu[upgrade_menu[i+1][1]][1]]:
                                    #     building[0].upgrade_production()
                                    # 
                                    # print(buy_menu[upgrade_menu[i+1][1]][0])
                                    # print(lists_of_buildings[buy_menu[upgrade_menu[i+1][1]][1]][0][0].name)
                                    if "Lifetime" in button.text:
                                        for building in lists_of_buildings[ buy_menu[upgrade_menu[i+1][1]][1]]:
                                            print(building[0].name, buy_menu[upgrade_menu[i+1][1]][0],"TESTİNGTESTİNG")
                                            if building[0].name == buy_menu[upgrade_menu[i+1][1]][0]:
                                                building[0].upgrade_life()
                                    elif "Production" in button.text:
                                        for building in lists_of_buildings[ buy_menu[upgrade_menu[i+1][1]][1]]:
                                            if building[0].name == buy_menu[upgrade_menu[i+1][1]][0]:
                                                building[0].upgrade_production()
                                   
                                    
    
                            else:
                                confirmation_window(not_enough_money_text,ok_text)
                                break


                    
               
               
                                
                
                            
                
                        
                if 0<mouse_pos[0] < 1200 and 0 <mouse_pos[1] < 800 :
                    dragging2 = True

            elif event.button == 3:  # Right click
                # # Sell selected building on the grid
                # print("test")
                # grid_x = (mouse_pos[0]-move_x) // TILE_SIZE
                # grid_y = (mouse_pos[1]-move_y) // TILE_SIZE
                # print("Coordinates",grid_x,grid_y)
                # if   (0 <= grid_x < len(grid)*TILE_SIZE and 0 <= grid_y < len(grid[grid_x])*TILE_SIZE) and grid[grid_x][grid_y] != TILE_EMPTY and grid[grid_x][grid_y] != TILE_OCEAN and grid[grid_x][grid_y] != TILE_CLOUDY: 
                #     print("inside if 1")

                #     if isinstance(grid[grid_x][grid_y], (EnergyConverter, HeatGenerator, Office, ResearchLab,Battery)):
                #         print("inside if 2")

                #         if sell_building(grid[grid_x][grid_y]):
                #             print("inside if 3")

                #             # explosion_thread = threading.Thread(target=handle_destruction,args=(grid[grid_x][grid_y],))
                #             # explosion_thread.start()
                #             grid[grid_x][grid_y] = TILE_EMPTY

                                
               
                dragging = True
                
                print("dragging")
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
                if TILE_SIZE < 70:
                    TILE_SIZE = TILE_SIZE+5
                    print(TILE_SIZE)
              
            elif event.button == 5 and 0<mouse_pos[0] < WINDOW_WIDTH-SIDEBAR_WIDTH and 0<mouse_pos[1] < WINDOW_HEIGHT  : # Mouse wheel down
                TILE_SIZE = TILE_SIZE-5
                if TILE_SIZE < 20:
                    TILE_SIZE = 20
                print(TILE_SIZE)
            
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                
                dragging2 = False
                
                # unlocking region logic
                if 0<mouse_pos[0] < 1200 and 0 <mouse_pos[1] < 800:
                        for buttons in region_button_list:
                            if buttons.rect.collidepoint(mouse_pos):
                                is_region_gone = buttons.execute_command()
                                print(is_region_gone,"is region gone")
                                if is_region_gone:
                                    buttons.rect = pygame.Rect(0, 0, 0, 0)
                                    break
                                print("Region button clicked")
                                break
            if event.button == 3:
                # Sell selected building on the grid
               
                grid_x = (mouse_pos[0]-move_x) // TILE_SIZE
                grid_y = (mouse_pos[1]-move_y) // TILE_SIZE
                if   (0 <= grid_x < len(grid)*TILE_SIZE and 0 <= grid_y < len(grid[grid_x])*TILE_SIZE) and grid[grid_x][grid_y] != TILE_EMPTY and grid[grid_x][grid_y] != TILE_OCEAN and grid[grid_x][grid_y] != TILE_CLOUDY: 
                    if isinstance(grid[grid_x][grid_y], (EnergyConverter, HeatGenerator, Office, ResearchLab,Battery)):
                        if sell_building(grid[grid_x][grid_y]):
                            grid[grid_x][grid_y] = TILE_EMPTY
                            
                # moving logic
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
          
            
            
    # for office in lists_of_buildings[Office]:
    #     office.sell_energy(player)
    #     total_energy_sold += office.energy_sell_rate
    #     # print("Energy sold",office.energy_sell_rate,"/ Tier",office.tier)
                
    # for lab in lists_of_buildings[ResearchLab]:
    #     lab.research(player)       

    # energy_gen_thread = threading.Thread(target=energy_gen)
    # energy_gen_thread.start()

    # Display game information
    
    # continent = pygame.Surface((WINDOW_WIDTH - SIDEBAR_WIDTH, WINDOW_HEIGHT))

    if dragging2: 
        if 0<mouse_pos[0] < 1200// TILE_SIZE and 0 <mouse_pos[1] < 800// TILE_SIZE:
                    grid_x = (mouse_pos[0]-move_x) // TILE_SIZE
                    grid_y = (mouse_pos[1]-move_y) // TILE_SIZE
                    # for generator in lists_of_buildings[HeatGenerator]:
                    #     if generator[0].rect.collidepoint(mouse_pos):
                    #         print("Generator clicked")
                    #         generator[0].upgrade_production()
                    #         break
                    if isinstance(grid[grid_x][grid_y],HeatGenerator) and grid[grid_x][grid_y].life_left == 0:
                        grid[grid_x][grid_y].life_left = grid[grid_x][grid_y].life_cycle
                        
        if  selected_building != None and 0 < mouse_pos[0] < 1200  and 0 < mouse_pos[1] <  len(grid[selected_building])*TILE_SIZE+move_y and grid[(mouse_pos[0]-move_x) // TILE_SIZE][(mouse_pos[1]-move_y) // TILE_SIZE] == 1 and state == "Buy" :
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
                research_check_bool = (buy_menu[selected_building][5] if selected_building > 1 else True)
                enough_money = player.enough_money(buy_menu[selected_building][1](buy_menu[selected_building][4],buy_menu[selected_building][3],buy_menu[selected_building][0]))
                #     print("res_check: ",research_check_bool,"/ money_check: ",enough_money)
                #     # print("mwenu",buy_menu[selected_building][5])

                if research_check_bool and enough_money :
                    click_sound.play()
                    print(buy_menu[selected_building][0])
                    grid[grid_x][grid_y] = buy_menu[selected_building][1](buy_menu[selected_building][4],buy_menu[selected_building][3],buy_menu[selected_building][0],buy_menu[selected_building][6])
                    
                    print(buy_menu[selected_building][3])
                    lists_of_buildings[buy_menu[selected_building][1]].append((grid[grid_x][grid_y],grid_x*TILE_SIZE+move_x,grid_y*TILE_SIZE+move_y))  
                    player.buy_energy_generator(buy_menu[selected_building][1](buy_menu[selected_building][4],buy_menu[selected_building][3],buy_menu[selected_building][0],buy_menu[selected_building][6]))
                    print(buy_menu[selected_building][0],"bought")
                    building_buildable = True
                    if isinstance(grid[grid_x][grid_y],Battery):
                        player.max_energy += grid[grid_x][grid_y].battery_capacity
                    

                if not building_buildable:
                    print("None",research_check_bool, enough_money)
                    dragging2 = False
                    if  research_check_bool and not enough_money:
                        print("1",research_check_bool, enough_money)
                        confirmation_window(not_enough_money_text,ok_text)
                    elif not research_check_bool and  enough_money:
                        print("2",research_check_bool, enough_money)
                        confirmation_window(not_researched_text,ok_text)

                    elif not research_check_bool and not enough_money:
                        print("3",research_check_bool, enough_money)
                        confirmation_window(not_researched_text,ok_text)
                        
    # pygame.draw.rect(window, (0, 105, 148), (0 , 0, WINDOW_WIDTH - SIDEBAR_WIDTH, WINDOW_HEIGHT)) 
    background_surface = pygame.Surface((WINDOW_WIDTH - SIDEBAR_WIDTH, WINDOW_HEIGHT))
    for x in range(0, WINDOW_WIDTH - SIDEBAR_WIDTH, 50):
        for y in range(0, WINDOW_HEIGHT, 50):
            background_surface.blit(background_image, (x, y))
    window.blit(background_surface, (0,0,WINDOW_WIDTH - SIDEBAR_WIDTH ,WINDOW_HEIGHT))


    tile_image = pygame.transform.scale(pygame.image.load('Data/tile2.jpg'), (TILE_SIZE, TILE_SIZE))
    cloud_image = pygame.transform.scale(pygame.image.load('Data/cloud_tile.png'), (TILE_SIZE, TILE_SIZE)) 


 
 
 
    
                
                            
 
 

    if dragging:
    # Draw tiles and objects
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                rect = pygame.Rect(
                    i * TILE_SIZE + (mouse_pos[0] - x_offset if -1300 < mouse_pos[0] - x_offset < 400 else (400 if mouse_pos[0] - x_offset > -1300 else -1300)),
                    j * TILE_SIZE + (mouse_pos[1] - y_offset if -300 < mouse_pos[1] - y_offset < 400 else (400 if mouse_pos[1] - y_offset > -300 else -300)),
                    TILE_SIZE, TILE_SIZE
                )
                if grid[i][j] == 0:
                    pass
                elif isinstance(grid[i][j], EnergyConverter) or isinstance(grid[i][j], Office) or isinstance(grid[i][j], ResearchLab) or isinstance(grid[i][j], Battery):
                    for buildings in buy_menu:
                        if buy_menu[buildings][0] == grid[i][j].name:
                            window.blit(pygame.transform.scale(tile_images[buildings], (TILE_SIZE, TILE_SIZE)), rect)
                elif isinstance(grid[i][j], HeatGenerator):
                    # Draw the tile image first
                    window.blit(tile_image, rect)
                    # Then draw the HeatGenerator image on top
                    image_surface = pygame.transform.scale(combined_dict[grid[i][j].name][1], (TILE_SIZE, TILE_SIZE))
                    if grid[i][j].life_left == 0:
                        image_surface.set_alpha(100)
                    else:
                        image_surface.set_alpha(255)  # Fully opaque when not life_left
                    window.blit(image_surface, rect)
                elif grid[i][j] == TILE_EMPTY:
                    window.blit(tile_image, rect)
                elif grid[i][j] == TILE_CLOUDY:
                    window.blit(cloud_image, rect)
    else:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                rect = pygame.Rect(i * TILE_SIZE + move_x, j * TILE_SIZE + move_y, TILE_SIZE, TILE_SIZE)
                if grid[i][j] == 0:
                    pass
                elif isinstance(grid[i][j], EnergyConverter) or isinstance(grid[i][j], Office) or isinstance(grid[i][j], ResearchLab) or isinstance(grid[i][j], Battery):
                    for buildings in buy_menu:
                        if buy_menu[buildings][0] == grid[i][j].name:
                            window.blit(pygame.transform.scale(tile_images[buildings], (TILE_SIZE, TILE_SIZE)), rect)
                elif grid[i][j] == TILE_EMPTY:
                    window.blit(tile_image, rect)
                elif isinstance(grid[i][j], HeatGenerator):
                    # Draw the tile image first
                    window.blit(tile_image, rect)
                    # Then draw the HeatGenerator image on top
                    image_surface = pygame.transform.scale(combined_dict[grid[i][j].name][1], (TILE_SIZE, TILE_SIZE))
                    if grid[i][j].life_left == 0:
                        image_surface.set_alpha(100)
                    else:
                        image_surface.set_alpha(255)  # Fully opaque when not life_left
                    window.blit(image_surface, rect)
                elif grid[i][j] == TILE_CLOUDY:
                    window.blit(cloud_image, rect)

        
    
    
    
    
        
    # window.blit(converter_menu_images[1], (5, 5,50,50))
    
    
    

    # if building_buildable:
    #     window.blit(buy_menu[selected_building][2],(mouse_x,mouse_y, TILE_SIZE, TILE_SIZE))




        # window.blit(scroll_bar, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 1 * SIDEBAR_ITEM_HEIGHT - 40))


    # window.blit(side_bar, (WINDOW_WIDTH - SIDEBAR_WIDTH, WINDOW_HEIGHT))
    # scroll_bar.convert_alpha()
    # window.blit(scroll_bar, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, 1 * SIDEBAR_ITEM_HEIGHT - 40))


    heat_bar_updater()
    life_cycle_updater()
    button_drawer()

    # Draw sidebar
    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH, 0, 10, WINDOW_HEIGHT))

    # Upper line
    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, 1 * SIDEBAR_ITEM_HEIGHT - 40))

    # Scroll tracker
    pygame.draw.rect(window, (180, 180, 255), (WINDOW_WIDTH - SIDEBAR_WIDTH + 460, 10, 15, WINDOW_HEIGHT))

    # Bottom area
    pygame.draw.rect(window, (0, 105, 148), (WINDOW_WIDTH - SIDEBAR_WIDTH, 9 * SIDEBAR_ITEM_HEIGHT - 40, SIDEBAR_WIDTH, WINDOW_HEIGHT - SIDEBAR_ITEM_HEIGHT - 40))

    
    
    switch_view(state,current_tier)
    # pygame.draw.rect(window, (0, 105, 148), scroll_bar_rect)
    #window.blit(menu_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 210, 9* SIDEBAR_ITEM_HEIGHT -30))


    
    scroll_tracker.draw(window,scroll_offset,SIDEBAR_ITEM_HEIGHT)
    
    
    
    grid_rect.move_ip(0, -scroll_offset)
    # testbutton.draw(window)
    scroll_offset = 0
    
    font = pygame.font.Font(None, 21)
    # Display game information (money and power)
    money_text = font.render(f'Money: {number_format(int(player.money))}', True, (0, 0, 100))
    money_persec_text = font.render(f'Money/Second: {number_format(money_gen_per_second*4)}', True, (0, 0, 100))
    energy_text = font.render(f'Energy: {number_format(int(player.energy))}/{number_format(int(player.max_energy))}', True, (0, 0,100))
    energy_persec_text = font.render(f'Energy/Second: {number_format(int(energy_gen_per_second*4))}', True, (0, 0,100))
    research_text = font.render(f'Research: {number_format(int(player.research))}', True, (0, 0, 100))
    research_persec_text = font.render(f'Research/Second: {number_format(int(research_gen_per_second*4))}', True, (0, 0, 100))

    window.blit(money_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 80))
    window.blit(money_persec_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 10, WINDOW_HEIGHT - 40))
    window.blit(energy_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 155, WINDOW_HEIGHT - 80))
    window.blit(energy_persec_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 155, WINDOW_HEIGHT - 40))
    window.blit(research_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 310, WINDOW_HEIGHT - 80))
    window.blit(research_persec_text, (WINDOW_WIDTH - SIDEBAR_WIDTH + 310, WINDOW_HEIGHT - 40))



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
    quickplace_button.draw(window)
    quickrevive_button.draw(window)



    # Check if mouse is hovering over a placed building
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pos = pygame.mouse.get_pos()
    
    # coordinates hover
    # test = font.render(f'Coordinates: {mouse_x,mouse_y}', True, (0, 0, 0))
    # window.blit(test,( mouse_pos[0], mouse_pos[1]))
    
    #fps hover
    #test = font.render(f'FPS: {clock}', True, (0, 0, 0))
    #window.blit(test,( mouse_pos[0], mouse_pos[1]))

    grid_x = (mouse_pos[0]-move_x )// TILE_SIZE
    grid_y = (mouse_pos[1]-+move_y) // TILE_SIZE
    if 0 <= grid_x < len(grid) and 0 <= grid_y < len(grid[grid_x]):
        # if grid[grid_x][grid_y] != TILE_EMPTY and grid[grid_x][grid_y] != TILE_OCEAN:
        info_text = None
        if isinstance(grid[grid_x][grid_y], EnergyConverter):
            info_text = font.render(f'Energy per heat: {number_format(grid[grid_x][grid_y].heat_conversion_per_second*4)}, Stored Energy: { number_format(grid[grid_x][grid_y].stored_heat)}, Max Energy: {number_format( grid[grid_x][grid_y].max_heat)}', True, (255, 255, 255))

        elif isinstance(grid[grid_x][grid_y], HeatGenerator):
            info_text = font.render(f'Heat per second: {number_format(grid[grid_x][grid_y].heat_per_tick*4)}, Total Lifecyle: { number_format(grid[grid_x][grid_y].life_cycle)}, Lifecyle Left: {number_format( grid[grid_x][grid_y].life_left)}', True, (255, 255, 255))

        elif isinstance(grid[grid_x][grid_y], Office):
            info_text = font.render(f'Energy sell rate: {number_format( grid[grid_x][grid_y].energy_sell_rate*4)} per second tier {number_format( grid[grid_x][grid_y].tier)} Level {number_format( grid[grid_x][grid_y].upgrade)}', True, (255, 255, 255))
        
        elif isinstance(grid[grid_x][grid_y], ResearchLab):
            info_text = font.render(f'Research Per Second: {number_format( grid[grid_x][grid_y].research_rate*4)} per second tier {number_format( grid[grid_x][grid_y].tier)} Level {number_format( grid[grid_x][grid_y].upgrade)}', True, (255, 255, 255))
        
        elif isinstance(grid[grid_x][grid_y], Battery):
            info_text = font.render(f'Increased Energy Cap: {number_format( grid[grid_x][grid_y].battery_capacity)}', True, (255, 255, 255))

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