import pygame

class Player:
    def __init__(self):
        self.energy = 0
        self.money = 10000000000
        self.research = 50
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
    
  
    def sell_multiple_buildings(self, Building_grid):
        total_cost = 0
        for Building in Building_grid:
                if Building is not None:
                    total_cost += Building.cost
        
        font = pygame.font.Font(None, 36)
        confirmation_text = font.render(f"  Do you want to sell these buildings for {(total_cost if total_cost != None else None)} money?  ", True, (0, 0, 0))
        yes_text = font.render("Yes", True, (0, 0, 0))
        no_text = font.render("No", True, (0, 0, 0))
      
      
      
      

        return confirmation_text,yes_text,no_text
