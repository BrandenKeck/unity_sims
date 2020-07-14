# Change system directory
import sys
sys.path.append("../../..")

# Import Game
from gridworld import world

# Create game instance
thisWorld = world(20, 16)
thisWorld.add_player("Player_1", 4, 2)
thisWorld.add_goal("Goal_1", 15, 13)

for i in range(20):
    for j in range(16):
        if i%2 == 0 and j%3 == 0:
            thisWorld.add_wall(i, j)
        if i%3 == 0 and j%2 == 0:
            thisWorld.add_wall(i, j)

# Establish settings
thisWorld.set_timestep_penalty(-1)
thisWorld.set_border_collide_penalty(-1)
thisWorld.set_wall_collide_penalty(-1)
thisWorld.set_goal_gradient_reward_factor(100)
thisWorld.set_goal_reward(20)

# Simulation Settings
thisWorld.set_learning_rate(0.7)
thisWorld.set_discount_factor(0.8)

# Run Pygame Simulation
thisWorld.set_movable_goals(True)
#thisWorld.train_agents(100)
thisWorld.run_game()