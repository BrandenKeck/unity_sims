# Change system directory
import sys
sys.path.append("../../..")

# Import Game
from gridworld import world

# Create game instance
thisWorld = world(9, 7)
thisWorld.add_player("Player_1", 1, 3)
thisWorld.add_player("Player_2", 7, 3)
thisWorld.add_goal("Goal_1", 5, 3)

# Establish settings
thisWorld.set_timestep_penalty(-100)

# Establish settings - Player
thisWorld.set_goal_gradient_reward_factor(1000)
thisWorld.set_goal_reward(200)
thisWorld.set_team_goal_reward(100)

# Establish settings - Goal
thisWorld.set_goal_player_repulsion_factor(1000)
thisWorld.set_goal_caught_penalty(-200)

# Run Pygame Simulation
thisWorld.set_movable_goals(True)
#thisWorld.train_agents(500)
thisWorld.run_game()