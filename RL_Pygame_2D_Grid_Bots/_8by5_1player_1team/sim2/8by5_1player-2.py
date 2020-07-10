# Import game
from gridworld import world

# Create game instance
thisWorld = world(8, 5)
thisWorld.add_player("Player_1", 1, 2)
thisWorld.add_goal(6, 2)

# Establish settings
thisWorld.set_timestep_penalty(-1)
thisWorld.set_goal_reward(20)

# Run Pygame Simulation
thisWorld.run_game()