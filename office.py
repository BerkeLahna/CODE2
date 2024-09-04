import pygame
class Office:
    def __init__(self,tier,upgrade,name,upgrade2=None):
        self.energy_sell_rate = 20*tier*(1.5**upgrade) *(100 ** (tier - 1))/4 # Energy selling rate for the office (per second)
        # self.cost = 10000 * (4 ** (tier - 1)) 
        self.cost = 100 * (16 ** (tier - 1)) 

        self.tier = tier
        self.name = name
        self.upgrade = upgrade

    def sell_energy(self, player):
        # Sell energy at the defined rate
        if player.energy >= self.energy_sell_rate:
            player.energy -= self.energy_sell_rate 
            player.money += self.energy_sell_rate * 2
        elif player.energy > 0:
            player.money += player.energy *2
            player.energy = 0
            
            
    def upgrade_production(self):
        self.energy_sell_rate *= 1.5
