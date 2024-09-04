import pygame
class Battery:
    def __init__(self,tier,upgrade,name,upgrade2=None):
        self.battery_capacity = 200*2**upgrade
        self.cost = 5000
        self.name = name
        self.tier = tier
        self.upgrade = upgrade
        
    def upgrade_production(self):
        self.battery_capacity *= 2
    