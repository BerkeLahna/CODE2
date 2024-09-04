import pygame
class EnergyConverter:
    def __init__(self, tier, upgrade,name,upgrade2=1):
        self.cost = 2000 * (12 ** (tier - 1)) 
        self.tier = tier
        self.upgrade = upgrade

        self.max_heat = 1000*tier*(2**upgrade)*(100 ** (tier - 1))
        self.heat_conversion_per_second = 10*tier*(1.25**upgrade)*(1000 ** (tier - 1))
        self.stored_heat = 0
        self.name = name
      


    def convert_heat(self, heat,player,handle_destruction):

        if heat <= self.heat_conversion_per_second:
            player.generate_energy(heat)
            if self.stored_heat > 0:
                self.stored_heat -= self.heat_conversion_per_second-heat

        else:
            if self.stored_heat + heat < self.max_heat:
                player.generate_energy(self.heat_conversion_per_second)
                self.stored_heat += heat-self.heat_conversion_per_second
            else:
                handle_destruction(self)
        
    def upgrade_production(self):
        self.heat_conversion_per_second *= 1.25
        
    def upgrade_max_heat(self):
        self.max_heat *= 2
    # def update_bar(self, screen, bar_width, bar_height, bar_position, bar_color, bar_border_color):
        
    #     fill_ratio = max(1, self.stored_heat / self.max_heat)
    #     fill_width = int(bar_width * fill_ratio)
        
        
    def draw_bar(self, screen, bar_width, bar_height, bar_position, bar_color, bar_border_color):
       
        fill_ratio = min(1, (self.stored_heat / self.max_heat))
        fill_width = int(bar_width * fill_ratio)
        # Draw the bar outline
        pygame.draw.rect(screen, bar_border_color, (bar_position[0], bar_position[1], bar_width, bar_height), 2)
        
        # Draw the filled portion of the bar
        fill_rect = pygame.Rect(bar_position[0], bar_position[1], fill_width, bar_height)
        pygame.draw.rect(screen, bar_color, fill_rect)
