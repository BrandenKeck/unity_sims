# Change system directory
import sys
sys.path.append("../../..")

# Import Game
from gridworld import world

# Create game instance
thisWorld = world(20, 18)
thisWorld.add_player("Player_1", 4, 2)
thisWorld.add_goal(15, 15)

# Establish settings
thisWorld.set_timestep_penalty(-1)
thisWorld.set_border_collide_penalty(-1)
thisWorld.set_goal_gradient_reward_factor(10000)
thisWorld.set_goal_reward(20)

# Run Pygame Simulation
thisWorld.train_agents(100)
thisWorld.run_game()