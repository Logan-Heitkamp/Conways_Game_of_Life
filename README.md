# Conways Game of Life
 
 A Python implementation of Conways Game of Life using Pygame, featuring an interactive grid editor with camera controls and simulation features.
 
 ## Features
 
 - Interactive grid editing
 - Camera pan and zoom controls
 - Real-time simulation with play/pause
 - Grid randomization
 - Adjustable simulation speed
 - Dynamic grid visualization
 
 ## Controls
 
 - WASD - Pan camera
 - Mouse Wheel - Zoom in/out
 - Left Click - Toggle cell state
 - Space - Play/pause simulation
 - R - Randomize grid
 - Shift - Increase movement speed
 
 ## Running the Game
 
 bash
 python source/main.py
 
 
 ## Game Rules
 
 Conways Game of Life follows these rules:
 
 1. Any live cell with fewer than two live neighbors dies (underpopulation)
 2. Any live cell with two or three live neighbors lives (survival)
 3. Any live cell with more than three live neighbors dies (overpopulation)
 4. Any dead cell with exactly three live neighbors becomes alive (reproduction)
 
 ## Development
 
 The project uses pytest for testing. Run tests with:
 
 bash
 pytest test/main_test.py
