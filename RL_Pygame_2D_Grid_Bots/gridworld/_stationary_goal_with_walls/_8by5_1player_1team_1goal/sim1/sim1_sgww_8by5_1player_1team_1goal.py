# Change system directory
import sys
sys.path.append("../../..")

# Import Game
from gridworld import world

# Create game instance
thisWorld = world(8, 5)
thisWorld.add_player("Player_1", 1, 2)
thisWorld.add_goal("Goal_1", 6, 2)
thisWorld.add_wall(2, 2)
thisWorld.add_wall(4, 1)
thisWorld.add_wall(4, 3)

# Set parameters
thisWorld.set_learning_rate(0.25)
thisWorld.set_discount_factor(0.75)

# Establish settings
thisWorld.set_timestep_penalty(-10)
#thisWorld.set_border_collide_penalty(-10)
#thisWorld.set_wall_collide_penalty(-10)
#thisWorld.set_goal_gradient_reward_factor(10)
thisWorld.set_goal_reward(20)

# Run Pygame Simulation
thisWorld.train_agents(100)
#thisWorld.set_greedy_policy(True)
thisWorld.run_game()