from gridworld import world
    
# Board size
width = 800
height = 500

# Initialize player
thisWorld = world(width, height)
thisWorld.add_player(2, 6)
thisWorld.add_player(4, 6)
thisWorld.add_player(4, 12)
thisWorld.add_goal(8, 8)
thisWorld.add_goal(4, 8)
thisWorld.add_goal(8, 4)

# Show Pygame Simulation
thisWorld.run_game()