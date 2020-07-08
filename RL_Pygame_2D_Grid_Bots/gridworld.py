import pygame
import numpy as np

'''
---------------------------
ENVIRONMENT CLASS
To be called by Run file
---------------------------
'''

class world():

    def __init__(self, w, h):

        # Dimensions of the board
        self.w = w
        self.h = h
        self.xsize = int(w/25)
        self.ysize = int(h/25)
        
        # Reinforcement Learning Parameters
        self.alpha = 0.1 ## Learning rate / step size
        self.gamma = 0.1 ## Discount Factor on Returns
        self.epsilon = 0.1 ## e-greedy probability

        # Penalties and Rewards
        self.goal_reward = 0
        self.goal_gradient_reward = 0
        self.team_goal_reward = 0
        self.opponent_goal_penalty = 0
        self.wall_collide_penalty = 0
        self.teammate_collide_penalty = 0
        self.opponent_collide_penalty = 0
        self.timestep_penalty = 0

        # Initialize Arrays
        self.players = []
        self.goals = []
    
    def run_game(self):
        
        # Initialize game
        pygame.init()
        window = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("gridworld")
        
        # Initialize game state
        run = True
        
        # Start the game loop
        while run:

            # Refresh window
            pygame.time.delay(10)
            pygame.draw.rect(window, (0, 0, 0), (0, 0, self.w, self.h))

            # Perform policy functions
            self.take_action()
            self.draw(window)

            # Update Display
            pygame.display.update()

            # Exit on Esc
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False

        pygame.quit()
        
    def train_agents(self, num_episodes):
        pass;
    
    def take_action(self):
        if self.update_ready():
            for p in self.players:
            
                # Initialize rewards for step
                player_rewards = 0

                # Call Learning Function for Agent
                p.decide_move(self.get_current_state(p.x, p.y), self.epsilon)

                # Wall Collision
                if p.target_x < 0 or p.target_x >= self.xsize:
                    p.target_x = p.x
                    p.target_pos_x = p.pos_x
                    player_rewards = player_rewards + self.wall_collide_penalty
                if p.target_y < 0 or p.target_y >= self.ysize:
                    p.target_y = p.y
                    p.target_pos_y = p.pos_y
                    player_rewards = player_rewards + self.wall_collide_penalty

                # Player Collision
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
                
                for g in self.goals:
                    if p.x == g.x and p.y == g.y:
                        player_rewards = player_rewards + self.goal_reward
                        p.rewards.append(player_rewards)
                        for pp in self.players:
                            if pp != p and p.team == pp.team:
                                pp.rewards.append(self.team_goal_reward)
                            elif pp != p and p.team != pp.team: 
                                pp.rewards.append(self.opponent_goal_penalty)
                        self.reset()
                        return
                        
                # REVISE FOR ACTUAL TIMESTEPS:
                player_rewards = player_rewards + self.timestep_penalty
                
                # Update agent reward and return functions
                p.rewards.append(player_rewards)
                

        # Execute movement animation
        for p in self.players:
            p.animate_move()
    
    def update_ready(self):
        for p in self.players:
            if p.target_x != p.x or p.target_y != p.y:
                return False
                
        return True
    
    def get_current_state(self, xx, yy):
        
        # Get 2d state list
        #     0 -> unoccupied space
        #     -1 -> player position
        #     999 -> goal position
        #     Otherwise, space is team #
        state = np.zeros([self.xsize, self.ysize])
        for p in self.players:
            state[p.x][p.y] = p.team
        for g in self.goals:
            state[g.x][g.y] = 999
        state[xx][yy] = -1
        return state
        
    def get_goal_rewards_gradient(self):
        pass
    
    def draw(self, window):
        for p in self.players:
            p.draw(window)
        for g in self.goals:
            g.draw(window)
    
    def reset(self):
        for p in self.players:
            p.reset()
    
    def add_player(self, x, y):
        self.players.append(player(x, y))

    def add_goal(self, x, y):
        self.goals.append(goal(x, y))
        
    def set_learning_rate(self, val):
        self.alpha = val
    
    def set_discount_factor(self, val):
        self.gamma = val
        
    def set_greedy_probability(self, val):
        self.epsilon = val
    
    def set_goal_reward(self, val):
        self.goal_reward = val
    
    def set_goal_gradient_reward(self, val):
        self.goal_gradient_reward = val
        
    def set_team_goal_reward(self, val):
        self.team_goal_reward = val
        
    def set_opponent_goal_penalty(self, val):
        self.opponent_goal_penalty = val
    
    def set_wall_collide_penalty(self, val):
        self.wall_collide_penalty = val

    def set_teammate_collide_penalty(self, val):
        self.teammate_collide_penalty = val

    def set_opponent_collide_penalty(self, val):
        self.opponent_collide_penalty = val

    def set_timestep_penalty(self, val):
        self.timestep_penalty = val

'''
-------------------------------
AGENT CLASS
To be called by "world" class
-------------------------------
'''

class player():

    def __init__(self, x, y):

        # Initial Position - Episode Memory
        self.init_x = x
        self.init_y = y

        # Position Attributes
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.pos_x = 25*x
        self.pos_y = 25*y
        self.target_pos_x = 25*x
        self.target_pos_y = 25*y

        # Agent Attributes
        # For each policy:
        #    0 -> North Probability
        #    1 -> East Probability
        #    2 -> South Probability
        #    3 -> West Probability
        self.team = 1
        self.states = []
        self.policies = []
        self.rewards = []
        self.returns = []
    
    def decide_move(self, current_state, epsilon):
    
        # Handle initial case of no states reached
        if self.states == []:
            self.states.append(current_state)
            self.policies.append([0.25, 0.25, 0.25, 0.25])
        
        # Check for an existing policy for the given state
        policy = []
        for idx, s in enumerate(self.states):
            if s.all() == current_state.all():
                policy = self.policies[idx]
        
        # Create a new policy for the current state if one doesn't exist
        if policy == []:
            self.states.append(current_state)
            policy = [0.25, 0.25, 0.25, 0.25]
            self.policies.append(policy)
        
        # Decide move based on e-greedy policy
        # Equal probability given to multiple greedy options
        # Equal probability given to all non-greedy options
        usemaxs = True
        m = max(policy)
        maxs = [i for i, j in enumerate(policy) if j == m]
        nonmaxs = [i for i, j in enumerate(policy) if j != m]
        if np.random.random(1)[0] > epsilon:
            nummaxs = len(maxs)
            if nummaxs > 0:
                cumprobs = [(i+1)/nummaxs for i in np.arange(nummaxs)]
            else:
                usemaxs = False
                numnonmaxs = len(nonmaxs)
                cumprobs = [(i+1)/numnonmaxs for i in np.arange(numnonmaxs)]
        else:
            numnonmaxs = len(nonmaxs)
            if numnonmaxs > 0:
                usemaxs = False
                cumprobs = [(i+1)/numnonmaxs for i in np.arange(numnonmaxs)]
            else:
                nummaxs = len(maxs)
                cumprobs = [(i+1)/nummaxs for i in np.arange(nummaxs)]
        
        # Randomly (uniformly) chose an action if more than one possibility exists
        diceroll = np.random.random(1)[0]
        for idx, c in enumerate(cumprobs):
            if diceroll <= c:
                if usemaxs:
                    action = maxs[idx]
                else:
                    action = nonmaxs[idx]
                break
        
        # Take the decided action
        if action == 0:
            self.set_target(0, -1)
        elif action == 1:
            self.set_target(1, 0)
        elif action == 2:
            self.set_target(0, 1)
        elif action == 3:
            self.set_target(-1, 0)
    
    # Purely asthetic function for animating the move of each agent
    def animate_move(self):
        if (self.pos_x != self.target_pos_x or self.pos_y != self.target_pos_y):
            self.pos_x = self.pos_x + np.sign(self.target_pos_x - self.pos_x)
            self.pos_y = self.pos_y + np.sign(self.target_pos_y - self.pos_y)
        else:
            self.x = self.target_x
            self.y = self.target_y
    
    # Set new position based on agent actions
    def set_target(self, dx, dy):
        self.target_x = self.x + 1 * dx
        self.target_y = self.y + 1 * dy
        self.target_pos_x = self.pos_x + 25 * dx
        self.target_pos_y = self.pos_y + 25 * dy  

    # Draw the agent on the board
    def draw(self, window):
        pygame.draw.rect(window, (0,0,255), (self.pos_x, self.pos_y, 25, 25))
    
    # Set agent position to initial value
    def reset(self):
        self.x = self.init_x
        self.y = self.init_y
        self.target_x = self.init_x
        self.target_y = self.init_y
        self.pos_x = 25*self.init_x
        self.pos_y = 25*self.init_y
        self.target_pos_x = 25*self.init_x
        self.target_pos_y = 25*self.init_y

'''
-------------------------------
GOAL CLASS
To be called by "world" class
-------------------------------
'''

class goal():
    
    # Goal takes on a basic position only
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.pos_x = 25*x
        self.pos_y = 25*y
        self.target_pos_x = 25*x
        self.target_pos_y = 25*y
    
    # Draw the goal
    def draw(self, window):
        pygame.draw.rect(window, (50, 255, 50), (self.pos_x, self.pos_y, 25, 25))