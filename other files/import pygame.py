import pygame

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

class Button:
    def __init__(self, pos, size, text, signal):
        self.rect = pygame.Rect(pos, size)
        self.text = text
        self.signal = signal

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 1)
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.signal()

def buy_button_signal():
    print("Buy button clicked")

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

buy_button = Button((WINDOW_WIDTH - 100, WINDOW_HEIGHT - 40), (80, 30), "Buy", buy_button_signal)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif buy_button.rect.collidepoint(pygame.mouse.get_pos()):
            buy_button.handle_event(event)

    window.fill((255, 255, 255))
    buy_button.draw(window)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()