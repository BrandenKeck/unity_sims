# Change system directory
import sys
sys.path.append("../../..")

# Import Game
from gridworld import world

# Create game instance
thisWorld = world(8, 5)
thisWorld.add_player("Player_1", 1, 2)
thisWorld.add_goal("Goal_1", 6, 2)

# Establish settings
thisWorld.set_timestep_penalty(-1)
thisWorld.set_goal_reward(200)
thisWorld.set_goal_gradient_reward_factor(1000)

# Learning Params
thisWorld.set_global_learning_rate(0.05)
thisWorld.set_global_discount_factor(0.75)

# Run Pygame Simulation
thisWorld.train_agents(1000)
thisWorld.run_game()