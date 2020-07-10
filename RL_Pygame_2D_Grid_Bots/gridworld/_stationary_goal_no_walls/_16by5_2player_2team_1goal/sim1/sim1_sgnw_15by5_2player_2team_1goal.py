# Change system directory
import sys
sys.path.append("../../..")

# Import Game
from gridworld import world

# Create game instance
thisWorld = world(15, 5)
thisWorld.add_player("Player_1", 1, 2)
thisWorld.add_player("Player_2", 13, 2)
thisWorld.set_player_team("Player_2", 2)
thisWorld.add_goal(7, 2)

# Establish settings
thisWorld.set_timestep_penalty(-1)
thisWorld.set_border_collide_penalty(-1)
thisWorld.set_goal_gradient_reward_factor(1000)
thisWorld.set_goal_reward(20)
thisWorld.set_opponent_goal_penalty(-20)

# Run Pygame Simulation
thisWorld.train_agents(10)
thisWorld.run_game()