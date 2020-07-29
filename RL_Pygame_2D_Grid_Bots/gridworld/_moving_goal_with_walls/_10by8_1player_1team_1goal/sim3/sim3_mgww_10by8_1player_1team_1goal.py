# Change system directory
import sys
sys.path.append("../../..")

# Import Game
from gridworld import world

# Create game instance
thisWorld = world(10, 8)
thisWorld.add_player("Player_1", 2, 2)
thisWorld.add_goal("Goal_1", 7, 5)

# Make Walls
for i in range(10):
    for j in range(8):
        if i%2 == 0 and j%3 == 0:
            thisWorld.add_wall(i, j)
        if i%3 == 0 and j%2 == 0:
            thisWorld.add_wall(i, j)

# Establish settings
thisWorld.set_timestep_penalty(-25)
thisWorld.set_border_collide_penalty(-50)
thisWorld.set_wall_collide_penalty(-50)
thisWorld.set_goal_gradient_reward_factor(10000)
thisWorld.set_goal_player_repulsion_factor(10000)
thisWorld.set_goal_reward(5000)
thisWorld.set_goal_caught_penalty(-5000)

# Simulation Settings
thisWorld.set_global_learning_rate(0.15)
thisWorld.set_global_discount_factor(0.1)

# Run Pygame Simulation
thisWorld.set_movable_goals(True)
#thisWorld.train_agents(100000)
thisWorld.run_game()