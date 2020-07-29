# Change system directory
import sys
sys.path.append("../../..")

# Import Game
from gridworld import world

# Create game instance
thisWorld = world(2, 2)
thisWorld.add_player("Player_1", 0, 0)
thisWorld.add_goal("Goal_1", 1, 1)

# Establish settings
thisWorld.set_timestep_penalty(-1)
thisWorld.set_goal_reward(20)
thisWorld.set_goal_gradient_reward_factor(10)

# Increased Learning Rate
thisWorld.set_global_learning_rate(0.1)

# Run Pygame Simulation
#thisWorld.train_agents(1000)
thisWorld.run_game()