import pygame
class ResearchLab:
    def __init__(self,tier,upgrade,name,upgrade2=None):
        self.research_rate = 5*tier*(1.5**(upgrade-1))  *(100 ** (tier - 1))/4
        # self.cost = 500 * (160 ** (tier - 1))  
        self.cost = 100 * (160 ** (tier - 1))  

        self.tier = tier
        self.name = name
        self.upgrade = upgrade

    def research(self, player):
        player.research += self.research_rate
            
    def upgrade_production(self):
        self.research_rate *= 1.5