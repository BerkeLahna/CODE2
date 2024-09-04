import pygame
import threading
import json
class Button():
    def __init__(self, x, y, width,height, text='', command=None, color=(0,80,200), image=None, border_radius = 0, font_size=22):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)
        self.command = command
        self.color = color
        self.image = image
        self.width = width
        self.height = height
        self.y = y
        self.border_radius = border_radius
        self.hovered = False
        self.clicked = False


        
                
    def draw(self, surface,scroll_offset=0,SIDEBAR_ITEM_HEIGHT=50,x_offset = 0, y_offset = 0,move_x=0,move_y=0, dragging = False,TILE_SIZE = 50,x_coord = 0,y_coord = 0):
        
        
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False

            
        border_rect = self.rect.inflate(2, 2) 
        border_surface = pygame.Surface(border_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(border_surface, (100, 100, 255), border_surface.get_rect(), border_radius=self.border_radius)
        surface.blit(border_surface, border_rect.topleft) 

        
        if self.hovered:
            pygame.draw.rect(surface, (100, 100, 255), self.rect, border_radius =  self.border_radius)
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius =  self.border_radius)

        if self.text and not self.image and not self.text == "Tracker":
            text = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        

        elif self.text and self.image:
            text = self.font.render(self.text, True, (255, 255, 255))
            new_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            new_surface.blit(self.image, (5, 5))
            new_surface.blit(text, (self.image.get_width() + 20, 16))
            pygame.draw.rect(new_surface, (0, 0, 0), (0, 0, self.width, self.height), 1)
            surface.blit(new_surface, (self.rect.x, self.rect.y))

        if self.text == "Tracker":
            if 10 <= self.rect.y <= 400:
                self.rect.move_ip(0, 0.334 * -scroll_offset)
            elif self.rect.y < 10:
                self.rect.y = 1 * SIDEBAR_ITEM_HEIGHT - 40
            elif self.rect.y > 400:
                self.rect.y = 400
        else:
            self.rect.move_ip(0, scroll_offset)
            
        if self.text and self.text.startswith("Region"):
            self.font = pygame.font.Font(None, TILE_SIZE//2)

            mouse_pos = pygame.mouse.get_pos()
            if dragging:
                self.rect = pygame.Rect(x_coord*TILE_SIZE+(mouse_pos[0]-x_offset if mouse_pos[0]-x_offset< 400  and mouse_pos[0]-x_offset> -1300 else (400 if mouse_pos[0]-x_offset > -1300 else -1300)), y_coord*TILE_SIZE+(mouse_pos[1]-y_offset if mouse_pos[1]-y_offset < 400  and mouse_pos[1]-y_offset > -300 else (400 if mouse_pos[1]-y_offset > -300 else -300)), TILE_SIZE*4, TILE_SIZE*2)
            else:
                self.rect = pygame.Rect(x_coord*TILE_SIZE+move_x, y_coord*TILE_SIZE+move_y, TILE_SIZE*4, TILE_SIZE*2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.command:
                self.command()
                
    def execute_command(self):
        if self.command:
            return self.command()
    # def handle_event(self, event):
    #     if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
    #         if self.command:
    #             self.command()
    #             self.clicked = True
    #     else:
    #         self.clicked = False
                
    def button_update(self, text=None, image=None,color=(0,80,200)):



        self.text = text
        self.image = image
        self.color = color
