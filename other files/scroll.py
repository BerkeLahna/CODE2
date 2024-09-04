import pygame as py
import math

clock = py.time.Clock()

FrameHeight = 600
FrameWidth = 1200

# PYGAME FRAME WINDOW
py.display.set_caption("Endless Scrolling in pygame")
screen = py.display.set_mode((FrameWidth, FrameHeight))


bg = py.image.load("Data/windmill.png").convert()

# DEFINING MAIN VARIABLES IN SCROLLING
scroll = 0
# HERE 1 IS THE CONSTATNT FOR REMOVING BUFFERING
tiles = math.ceil(FrameWidth  /bg.get_width()) + 1   

while 1:
  clock.tick(100)

  # APPENDING THE IMAGE TO THE BACK OF THE SAME IMAGE
  i=0
  while(i<tiles):
    screen.blit(bg, (bg.get_width()*i + scroll, 0))
    i+=1
  # FRAME FOR SCROLLING
  scroll -= 6

  # RESET THE SCROLL FRAME
  if abs(scroll) > bg.get_width():
    scroll = 0
  # CLOSING THE FRAME OF SCROLLING
  for event in py.event.get():
    if event.type == py.QUIT:
        quit()

  py.display.update()

py.quit()