Energy Tycoon Game
Overview
Energy Tycoon is a strategy game where players manage resources, build various types of buildings, and upgrade their infrastructure to generate energy, money, and research points. The game is built using Python and Pygame.

Features
Building Management: Players can build different types of buildings such as Heat Generators, Energy Converters, Offices, Research Labs, and Batteries.
Resource Management: Manage resources like money, energy, and research points.
Upgrades: Upgrade buildings to improve their efficiency and output.
Research: Unlock new technologies and buildings through research.
Region Unlocking: Unlock new regions on the map by spending money.
Multiple Building Deletion: Delete multiple buildings at once.
Quick Actions: Quickly place or revive buildings using dedicated buttons.
Key Components
Main Game Loop
The main game loop handles events, updates the game state, and renders the game screen. It includes:

Event handling for mouse clicks and other interactions.
Updating the game state based on player actions.
Rendering the game screen, including the grid, sidebar, and various UI elements.
Building Placement
Players can place buildings on a grid. The placement logic checks if the player has enough resources and if the building can be placed at the selected location.

Upgrades and Research
Players can upgrade buildings to improve their performance. Research points can be used to unlock new buildings and technologies.

Resource Management
The game tracks the player's money, energy, and research points. These resources are updated based on the buildings' performance and player actions.

UI Elements
The game includes various UI elements such as buttons, menus, and information displays. These elements are used to interact with the game and display important information to the player.

How to Play
Start the Game: Run the game using Python and Pygame.
Build Structures: Use the sidebar to select and place buildings on the grid.
Manage Resources: Keep an eye on your money, energy, and research points.
Upgrade Buildings: Upgrade your buildings to improve their efficiency.
Conduct Research: Unlock new buildings and technologies through research.
Expand Your Territory: Unlock new regions by spending money.
Quick Actions: Use quick action buttons to place or revive buildings rapidly.
Installation
Install Python: Make sure you have Python installed on your machine.
Install Pygame: Install Pygame using pip:
pip install pygame
Run the Game: Execute the game script:
python gametest.py
File Structure
gametest.py: Main game script containing the game loop, event handling, and core game logic.
button_file.py: Contains the Button class used for creating interactive buttons.
player.py: Contains the Player class that manages player resources.
heatGenerator.py, energyConverter.py, office.py, researchLab.py, battery.py: Scripts for different building types.
objects.py: Contains additional game objects and utilities.

Enjoy playing Energy Tycoon!