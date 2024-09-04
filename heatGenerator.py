import pygame
class HeatGenerator:
    def __init__(self, tier,upgrade,name,upgrade2=1):
        self.cost = 1000 * (4 ** (tier - 1)) * (tier - 1) + (10 if tier == 1 else 0)
        self.heat_per_tick = 1*(1.5**(upgrade-1)) *(10 ** (tier - 1))/4
        self.tier = tier
        self.name = name
        self.upgrade = upgrade
        self.life_cycle = ((10 ** (tier))*2**upgrade2)/2
        self.life_left = self.life_cycle
        self.upgrade2 = upgrade2
        
    def generate_heat(self,player):
        
        
          
        if (self.tier > 1) and self.life_left > 0:
            
            return self.heat_per_tick
        elif self.life_left > 0:
            
            # player.generate_energy(self.heat_per_tick)
            if player.energy + self.heat_per_tick <= player.max_energy:
                player.energy += self.heat_per_tick
            else :
                player.energy = player.max_energy
            return 0
        else: 
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
        print("upgraded")

        
    def upgrade_life(self):
        print("upgraded")
        self.life_cycle *= 2
        if self.life_left > 0:
            self.life_left = self.life_cycle - (self.life_cycle/2 - self.life_left)
            

        
    def update_life_left(self):
        
        if self.life_left > 0:
            self.life_left -= 1/4
        else :
            self.life_left = 0
        
    
    def draw_bar(self, screen, bar_width, bar_height, bar_position, bar_color, bar_border_color):
       
        fill_ratio = min(1, (self.life_left / self.life_cycle))
        fill_width = int(bar_width * fill_ratio)
        # Draw the bar outline
        pygame.draw.rect(screen, bar_border_color, (bar_position[0], bar_position[1], bar_width, bar_height), 2)
        
        # Draw the filled portion of the bar
        fill_rect = pygame.Rect(bar_position[0], bar_position[1], fill_width, bar_height)
        pygame.draw.rect(screen, bar_color, fill_rect)