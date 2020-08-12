# Standard Imports
import pygame, sys, os
import numpy as np

# Custom Class Imports
import player, wall, spritesheet

# World Class - Runs Simulations
class world():

    def __init__(self, xsize, ysize):

        # Dimensions of the board
        self.xsize = xsize
        self.ysize = ysize
        self.w = 25*xsize
        self.h = 25*ysize

        # Set episodic variables
        self.episode_count = 0
        self.timelimit = 10000
        self.current_time = 0

        # Penalties and Rewards
        self.goal_reward = 0
        self.goal_gradient_reward_factor = 0
        self.goal_caught_penalty = 0
        self.goal_player_repulsion_factor = 0
        self.team_goal_reward = 0
        self.opponent_goal_penalty = 0
        self.border_collide_penalty = 0
        self.wall_collide_penalty = 0
        self.teammate_collide_penalty = 0
        self.opponent_collide_penalty = 0
        self.timestep_penalty = 0
        self.timelimit_penalty = 0

        # Movable Goals Parameters
        self.movable_goals = False
        self.goal_movement_probability = 0

        # Initialize Arrays
        self.players = []
        self.goals = []
        self.goal_rewards_gradient = []
        self.goal_repulsion_gradient = []
        self.walls = []

        # Image Properties
        self.player_imgs = None
        self.goal_imgs = None
        self.wall_imgs = None

    def run_game(self):

        # Initialize game
        pygame.init()
        window = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("gridworld")
        self.set_images()

        # Initialize game state
        run = True

        # Calculate initial rewards gradient
        self.goal_rewards_gradient = self.get_goal_rewards_gradient()
        self.goal_repulsion_gradient = self.get_goal_repulsion_gradient()

        # Start the game loop
        while run:

            # Refresh window
            pygame.time.delay(10)
            pygame.draw.rect(window, (0, 0, 0), (0, 0, self.w, self.h))

            # Check if new rewards gradient is needed
            # If so, recalculate the gradient list
            if self.movable_goals:
                check_movement = False
                for g in self.goals:
                    if g.x != g.init_x or g.y != g.init_y:
                        check_movement = True

                if check_movement:
                    self.goal_rewards_gradient = self.get_goal_rewards_gradient()
                    self.goal_repulsion_gradient = self.get_goal_repulsion_gradient()

            # Perform learning functions and enact policy
            self.simulate_action(False)

            # Draw objects
            self.draw(window)

            # Update Display
            pygame.display.update()

            # Exit on Esc
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False

        pygame.quit()

    def train_agents(self, num_episodes):

        # Output info to command line:
        print("Training Agents...  ")
        print("Required Episode Completions:  " + str(num_episodes))

        # get initial rewards gradient
        self.goal_rewards_gradient = self.get_goal_rewards_gradient()
        self.goal_repulsion_gradient = self.get_goal_repulsion_gradient()

        self.episode_count = 0
        while self.episode_count < num_episodes:

            # Check if new rewards gradient is needed
            # If so, recalculate the gradient list
            if self.movable_goals:
                check_movement = False
                for g in self.goals:
                    if g.x != g.init_x or g.y != g.init_y:
                        check_movement = True

                if check_movement:
                    self.goal_rewards_gradient = self.get_goal_rewards_gradient()
                    self.goal_repulsion_gradient = self.get_goal_repulsion_gradient()

            # Simulate
            self.simulate_action(True)

    '''
    TODO TODO TODO TODO TODO
    Simplify this nonsense
     - functionalize penalties
     - better "get current state" interaction between classes
    '''
    def simulate_action(self, quickact):

        # Check if all moves have completed before taking an action
        if self.update_ready():

            # Count number of actions
            self.current_time = self.current_time + 1

            # Loop for player actions
            for p in self.players:

                # Initialize rewards for step
                player_rewards = 0

                # Store rewards gradient value of previous position
                prev_gradient_value = self.goal_rewards_gradient[p.x][p.y]

                # Call Learning Functions for Agents
                p_state = self.get_current_state(p.x, p.y)
                p.learn(p_state)
                p.act()

                # Border Collision Penalty
                if p.target_x < 0 or p.target_x >= self.xsize:
                    p.target_x = p.x
                    p.target_pos_x = p.pos_x
                    player_rewards = player_rewards + self.border_collide_penalty
                if p.target_y < 0 or p.target_y >= self.ysize:
                    p.target_y = p.y
                    p.target_pos_y = p.pos_y
                    player_rewards = player_rewards + self.border_collide_penalty

                for w in self.walls:
                    if p.target_x == w.x and p.target_y == w.y:
                        p.target_x = p.x
                        p.target_y = p.y
                        p.target_pos_x = p.pos_x
                        p.target_pos_y = p.pos_y
                        player_rewards = player_rewards + self.wall_collide_penalty

                # Player Collision Rewards and Penalties
                for pp in self.players:
                    if pp != p and p.target_x == pp.x:
                        if p.team == pp.team:
                            player_rewards = player_rewards + self.teammate_collide_penalty
                        else:
                            player_rewards = player_rewards + self.opponent_collide_penalty
                        p.target_x = p.x
                        p.target_pos_x = p.pos_x
                    if pp != p and p.target_y == pp.y:
                        if p.team == pp.team:
                            player_rewards = player_rewards + self.teammate_collide_penalty
                        else:
                            player_rewards = player_rewards + self.opponent_collide_penalty
                        p.target_y = p.y
                        p.target_pos_y = p.pos_y

                # Add rewards and penalties for completion of an episode
                for g in self.goals:
                    if p.x == g.x and p.y == g.y:
                        player_rewards = player_rewards + self.goal_reward
                        p.last_reward = player_rewards
                        for pp in self.players:
                            if pp != p and p.team == pp.team:
                                pp.last_reward = self.team_goal_reward
                            elif pp != p and p.team != pp.team:
                                pp.last_reward = self.opponent_goal_penalty

                        g.last_reward = self.goal_caught_penalty

                        self.reset()
                        self.episode_count = self.episode_count + 1
                        print("Completed Episodes:  " + str(self.episode_count))

                        return

                # Handle timelimit reached
                if self.current_time >= self.timelimit:
                    for pp in self.players: pp.last_reward = self.timelimit_penalty
                    for g in self.goals: g.last_reward = -self.timelimit_penalty
                    self.reset()
                    self.episode_count = self.episode_count + 1
                    print("Completed Episodes:  " + str(self.episode_count))

                    return

                # Add a reward based on improvement in position
                gradient_reward = self.goal_gradient_reward_factor * (self.goal_rewards_gradient[p.target_x][p.target_y] - prev_gradient_value)
                player_rewards = player_rewards + gradient_reward

                # Timestep penalty
                player_rewards = player_rewards + self.timestep_penalty

                # Update agent reward and previous state
                p.last_reward = player_rewards

            # Loop for Goal actions if goals are movable
            if self.movable_goals:
                for g in self.goals:

                    # Initialize rewards for step
                    goal_rewards = 0

                    # Store rewards gradient value of previous position
                    prev_goal_gradient_value = self.goal_repulsion_gradient[g.x][g.y]

                    # Call Learning Functions for Agents
                    g_state = self.get_current_state(g.x, g.y)
                    g.learn(g_state)
                    g.act()

                    # Player Targeted Penalty
                    for p in self.players:
                        if g.target_x == p.x and g.target_y == p.y:
                            goal_rewards = goal_rewards + self.goal_caught_penalty
                            g.target_x = g.x
                            g.target_y = g.y

                    # Border Collision Penalty
                    if g.target_x < 0 or g.target_x >= self.xsize:
                        g.target_x = g.x
                        g.target_pos_x = g.pos_x
                        goal_rewards = goal_rewards + self.border_collide_penalty
                    if g.target_y < 0 or g.target_y >= self.ysize:
                        g.target_y = g.y
                        g.target_pos_y = g.pos_y
                        goal_rewards = goal_rewards + self.border_collide_penalty

                    for w in self.walls:
                        if g.target_x == w.x and g.target_y == w.y:
                            g.target_x = g.x
                            g.target_y = g.y
                            g.target_pos_x = g.pos_x
                            g.target_pos_y = g.pos_y
                            goal_rewards = goal_rewards + self.wall_collide_penalty

                    # Goal Collision Rewards and Penalties
                    for gg in self.goals:
                        if gg != g and g.target_x == gg.x:
                            goal_rewards = goal_rewards + self.teammate_collide_penalty
                            g.target_x = g.x
                            g.target_pos_x = g.pos_x
                        if gg != g and g.target_y == gg.y:
                            goal_rewards = goal_rewards + self.teammate_collide_penalty
                            g.target_y = g.y
                            g.target_pos_y = g.pos_y

                    # Add a reward based on improvement in position
                    gradient_reward = self.goal_player_repulsion_factor * (prev_goal_gradient_value - self.goal_repulsion_gradient[g.target_x][g.target_y])
                    goal_rewards = goal_rewards + gradient_reward

                    # Timestep penalty ("reward")
                    goal_rewards = goal_rewards - self.timestep_penalty

                    # Update agent reward and previous state
                    g.last_reward = goal_rewards

        # Execute movement of player
        for p in self.players:
            if quickact: p.quick_move()
            else: p.animate_move()

        # Execute movement of goals
        if self.movable_goals:
            for g in self.goals:
                if quickact: g.quick_move()
                else: g.animate_move()

    # Check that animations have completed for "Run" mode
    def update_ready(self):
        for p in self.players:
            if p.target_x != p.x or p.target_y != p.y: return False
        for g in self.goals:
            if g.target_x != g.x or g.target_y != g.y: return False

        return True

    # Create 2D list representation of the current state
    def get_current_state(self, xx, yy):

        # Get 2d state list
        #     0 -> unoccupied space
        #     -1 -> player position
        #     -2 -> goal position
        #     -3 -> wall position
        #     Otherwise, space is team #
        state = np.zeros([self.xsize, self.ysize])
        for p in self.players:
            state[p.x][p.y] = p.team
        for g in self.goals:
            state[g.x][g.y] = -2
        for w in self.walls:
            state[w.x][w.y] = -3

        state[xx][yy] = -1

        return np.array(state).flatten().tolist()

    '''
    TODO TODO TODO - Consolidate  and Optimize Gradient Functions
    ACTUALLY ,, bump gradient functions to player class eventually
    '''
    # Create rewards gradient based on normalized inverse manhattan distance from each goal
    def get_goal_rewards_gradient(self):
        ness = np.zeros([self.xsize, self.ysize])
        onett = 0
        for i in np.arange(self.xsize):
            for j in np.arange(self.ysize):
                for g in self.goals:
                    if (np.abs(i - g.x) + np.abs(j - g.y)) != 0:
                        ness[i][j] = ness[i][j] + 1/(np.abs(i - g.x) + np.abs(j - g.y))
                        onett = onett + 1/(np.abs(i - g.x) + np.abs(j - g.y))
                    else:
                        ness[i][j] = 1

        for i in np.arange(self.xsize):
            for j in np.arange(self.ysize):
                ness[i][j] = ness[i][j]/onett

        return ness

    # Create repulsion gradient based on normalized inverse manhattan distance from each player
    def get_goal_repulsion_gradient(self):
        ness = np.zeros([self.xsize, self.ysize])
        onett = 0
        for i in np.arange(self.xsize):
            for j in np.arange(self.ysize):
                for p in self.players:
                    if (np.abs(i - p.x) + np.abs(j - p.y)) != 0:
                        ness[i][j] = ness[i][j] + 1 / (np.abs(i - p.x) + np.abs(j - p.y))
                        onett = onett + 1 / (np.abs(i - p.x) + np.abs(j - p.y))
                    else:
                        ness[i][j] = 1

        for i in np.arange(self.xsize):
            for j in np.arange(self.ysize):
                ness[i][j] = ness[i][j] / onett

        return ness

    # Start of a new episode - set everything back to original positions
    def reset(self):
        self.current_time = 0
        for p in self.players:
            p.x = p.init_x
            p.y = p.init_y
            p.target_x = p.init_x
            p.target_y = p.init_y
            p.pos_x = 25 * p.init_x
            p.pos_y = 25 * p.init_y
            p.target_pos_x = 25 * p.init_x
            p.target_pos_y = 25 * p.init_y
        for g in self.goals:
            g.x = g.init_x
            g.y = g.init_y
            g.target_x = g.init_x
            g.target_y = g.init_y
            g.pos_x = 25 * g.init_x
            g.pos_y = 25 * g.init_y
            g.target_pos_x = 25 * g.init_x
            g.target_pos_y = 25 * g.init_y

    '''
    BEGIN RENDERING FUNCTIONS
    '''

    # Draw world objects
    def draw(self, window):
        for p in self.players:
            window.blit(p.img, (p.pos_x, p.pos_y))
        for g in self.goals:
            window.blit(g.img, (g.pos_x, g.pos_y))
        for w in self.walls:
            window.blit(w.img, (w.pos_x, w.pos_y))

    # Import image data and set to variables (Cat / Mouse / Wall characters)
    def set_images(self):

        os.chdir(os.path.dirname(sys.argv[0]))
        self.player_imgs = spritesheet.make_sprite_array(spritesheet.spritesheet('../../../_img/cats.png'), 5, 25, 25)
        self.goal_imgs = spritesheet.make_sprite_array(spritesheet.spritesheet('../../../_img/mouse.png'), 1, 25, 25)
        self.wall_imgs = spritesheet.make_sprite_array(spritesheet.spritesheet('../../../_img/wall.png'), 1, 25, 25)

        for p in self.players:
            p.img = self.player_imgs[p.team - 1]
        for g in self.goals:
            g.img = self.goal_imgs[0]
        for w in self.walls:
            w.img = self.wall_imgs[0]

    '''
    BEGIN SET/GET FUNCTIONS
    '''

    def add_player(self, name, x, y):
        self.players.append(player.player(name, None, x, y))

    def add_goal(self, name, x, y):
        self.goals.append(player.player(name, None, x, y))

    def add_wall(self, x, y):
        self.walls.append(wall.wall(None, x, y))

    # Change team of player by player name (Team Default is 1; Options are 1 through 5)
    def set_player_team(self, name, team):
        if team > 5: team = 5  ## TODO - ACTUAL ERROR HANDLING
        for p in self.players:
            if p.name == name:
                p.team = team

    def set_global_learning_rate(self, val):
        for p in self.players:
            p.alpha = val
        for g in self.goals:
            g.alpha = val

    def set_global_discount_factor(self, val):
        for p in self.players:
            p.gamma = val
        for g in self.goals:
            g.gamma = val

    def set_agent_learning_rate(self, name, val):
        for p in self.players:
            if p.name == name:
                p.alpha = val
        for g in self.goals:
            if g.name == name:
                g.alpha = val

    def set_agent_discount_factor(self, name, val):
        for p in self.players:
            if p.name == name:
                p.gamma = val
        for g in self.goals:
            if g.name == name:
                g.gamma = val

    def set_goal_reward(self, val):
        self.goal_reward = val

    def set_goal_gradient_reward_factor(self, val):
        self.goal_gradient_reward_factor = val

    def set_goal_caught_penalty(self, val):
        self.goal_caught_penalty = val

    def set_goal_player_repulsion_factor(self, val):
        self.goal_player_repulsion_factor = val

    def set_team_goal_reward(self, val):
        self.team_goal_reward = val

    def set_opponent_goal_penalty(self, val):
        self.opponent_goal_penalty = val

    def set_border_collide_penalty(self, val):
        self.border_collide_penalty = val

    def set_wall_collide_penalty(self, val):
        self.wall_collide_penalty = val

    def set_teammate_collide_penalty(self, val):
        self.teammate_collide_penalty = val

    def set_opponent_collide_penalty(self, val):
        self.opponent_collide_penalty = val

    def set_timestep_penalty(self, val):
        self.timestep_penalty = val

    def set_timelimit_penalty(self, val):
        self.timelimit_penalty = val

    def set_movable_goals(self, val):
        self.movable_goals = val

    def set_goal_movement_probability(self, val):
        self.goal_movement_probability = val