import pygame, pickle
import numpy as np

'''
---------------------------
ENVIRONMENT CLASS
To be called by Run file
---------------------------
'''

class world():

    def __init__(self, xsize, ysize):

        # Dimensions of the board
        self.xsize = xsize
        self.ysize = ysize
        self.w = 25*xsize
        self.h = 25*ysize
        
        # Reinforcement Learning Parameters
        self.alpha = 0.1 ## Learning rate / step size
        self.gamma = 0.1 ## Discount Factor on Returns

        # Penalties and Rewards
        self.goal_reward = 0
        self.goal_gradient_reward_factor = 0
        self.team_goal_reward = 0
        self.opponent_goal_penalty = 0
        self.border_collide_penalty = 0
        self.wall_collide_penalty = 0
        self.teammate_collide_penalty = 0
        self.opponent_collide_penalty = 0
        self.timestep_penalty = 0

        ''' TODO '''
        # Movable Goals Parameters
        self.movable_goals = False
        self.goal_movement_probability = 0

        # Initialize Arrays
        self.players = []
        self.goals = []
        self.goal_rewards_gradient = []
    
    def run_game(self):
        
        # Initialize game
        pygame.init()
        window = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("gridworld")
        
        # Initialize game state
        run = True

        # Calculate initial rewards gradient
        self.goal_rewards_gradient = self.get_goal_rewards_gradient()

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

            # Perform learning functions and enact policy
            self.simulate_action()

            # Draw objects
            self.draw(window)

            # Update Display
            pygame.display.update()

            # Exit on Esc
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False

        pygame.quit()

    '''
    Major TODO
    Agents should be trainable outside of pygame sim
    '''
    def train_agents(self, num_episodes):
        ticker = -1
        pass

    def simulate_action(self):
        if self.update_ready():
            for p in self.players:
            
                # Initialize rewards for step
                player_rewards = 0

                # Store rewards gradient value of previous position
                prev_gradient_value = self.goal_rewards_gradient[p.x][p.y]

                # Call Learning Functions for Agent
                p.learn(self.get_current_state(p.x, p.y), self.alpha, self.gamma)
                p.act(self.get_current_state(p.x, p.y))

                '''DEBUG - REMOVE'''
                if len(p.rewards) > 0:
                    print(p.policies[p.prev_state])

                # Border Collision Penalty
                if p.target_x < 0 or p.target_x >= self.xsize:
                    p.target_x = p.x
                    p.target_pos_x = p.pos_x
                    player_rewards = player_rewards + self.border_collide_penalty
                if p.target_y < 0 or p.target_y >= self.ysize:
                    p.target_y = p.y
                    p.target_pos_y = p.pos_y
                    player_rewards = player_rewards + self.border_collide_penalty

                '''
                TODO
                Penalty for "Wall" collisions
                '''

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
                        p.rewards.append(player_rewards)
                        for pp in self.players:
                            if pp != p and p.team == pp.team:
                                pp.rewards.append(self.team_goal_reward)
                            elif pp != p and p.team != pp.team: 
                                pp.rewards.append(self.opponent_goal_penalty)

                        self.reset()
                        return

                # Add a reward based on improvement in position
                gradient_reward = self.goal_gradient_reward_factor * (self.goal_rewards_gradient[p.target_x][p.target_y] - prev_gradient_value)
                player_rewards = player_rewards + gradient_reward

                # Timestep penalty
                player_rewards = player_rewards + self.timestep_penalty
                
                # Update agent reward and previous state
                p.rewards.append(player_rewards)

        # Execute movement animation
        for p in self.players:
            p.animate_move()

    # Check that animations have completed for "Run" mode
    def update_ready(self):
        for p in self.players:
            if p.target_x != p.x or p.target_y != p.y:
                return False
                
        return True

    # Create 2D list representation of the current state
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

    # Draw world objects
    def draw(self, window):
        for p in self.players:
            p.draw(window)
        for g in self.goals:
            g.draw(window)
    
    def reset(self):
        for p in self.players:
            p.reset()
    
    def add_player(self, name, x, y):
        self.players.append(player(name, x, y))

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
    
    def set_goal_gradient_reward_factor(self, val):
        self.goal_gradient_reward_factor = val
        
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

    def set_movable_goals(self, val):
        self.movable_goals = val

    def set_goal_movement_probability(self, val):
        self.goal_movement_probability = val

'''
-------------------------------
PLAYER CLASS
To be called by "world" class
-------------------------------
'''

class player():

    def __init__(self, name, x, y):

        # Initialize player name
        self.name = name

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
        self.prev_state = 0
        self.prev_action = 0
        self.curr_state = -1
        self.rewards = []
        self.states, self.policies, self.Q = self.get_player_data()

    def act(self, current_state):
        
        # Check for an existing policy for the given state
        policy = [0.25, 0.25, 0.25, 0.25]
        if self.curr_state == -1:
            for idx, s in enumerate(self.states):
                if s.tolist() == current_state.tolist():
                    policy = self.policies[idx]
                    self.prev_state = idx
        else:
            policy = self.policies[self.curr_state]
            self.prev_state = self.curr_state

        pol_sum = 0
        cumprobs = []
        for p in policy:
            pol_sum = pol_sum + p
            cumprobs.append(pol_sum)
        
        # Randomly (uniformly) chose an action if more than one possibility exists
        diceroll = np.random.random(1)[0]
        for idx, c in enumerate(cumprobs):
            if diceroll <= c:
                action = idx
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

        # Store previous action
        self.prev_action = action

    def learn(self, current_state, alpha, gamma):

        # Handle first pass
        if self.prev_state == [] or len(self.rewards) == 0:
            return

        # Get policy for the current state and q table for the current state
        Q_next = []
        for idx, s in enumerate(self.states):
            if s.tolist() == current_state.tolist():
                Q_next = self.Q[idx]
                self.curr_state = idx

        # Create a new q table and policy for the current state if one doesn't exist
        if Q_next == []:
            # Set Default Q Table
            Q_next = [1, 1, 1, 1]

            # Add new state, policy, and q table
            self.states.append(np.copy(current_state))
            self.policies.append([0.25, 0.25, 0.25, 0.25])
            self.Q.append([1, 1, 1, 1])
            self.curr_state = len(self.states) - 1

        # Update Q table for prev state:
        max_Q_next = max(Q_next)
        rewards_last = self.rewards[len(self.rewards) - 1]
        self.Q[self.prev_state][self.prev_action] = self.Q[self.prev_state][self.prev_action] + alpha * (rewards_last + gamma * max_Q_next - self.Q[self.prev_state][self.prev_action])

        # Add heuristics to create reasonable nondeterministic policies
        one_percent_of_range = 0.01*np.abs(max(self.Q[self.prev_state]) - min(self.Q[self.prev_state]))
        normalized_Q = [0,0,0,0]
        for a in np.arange(len(self.Q[self.prev_state])):
            normalized_Q[a] = self.Q[self.prev_state][a] - min(self.Q[self.prev_state]) + one_percent_of_range

        # Create an E-soft-ish policy
        normalized_sum = sum(normalized_Q)
        for a in np.arange(len(self.policies[self.prev_state])):
            self.policies[self.prev_state][a] = normalized_Q[a]/normalized_sum

        # Write to player file to save learned states, policies, and Q functions
        with open(self.name + ".txt", 'wb') as file:
            pickle.dump((self.states, self.policies, self.Q), file)

    # Search for stored state/policy file
    def get_player_data(self):
        try:
            # Read stored player information if it exists
            with open(self.name + ".txt", 'rb') as file: states, policies, Q = pickle.load(file)
            return states, policies, Q
        except:
            # Initialize empty player information if no file found
            return [], [], []

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
To be used by "world" class
-------------------------------
'''

class goal():
    
    # Initialize goal properties
    def __init__(self, x, y):
        self.init_x = x
        self.init_y = y

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

    '''TODO - Goal Movement'''

'''
TODO
EVERYTHING
Add Walls to game
'''
class wall():

    # Initialize wall properties
    def __init__(self, x, y):
        self.init_x = x
        self.init_y = y

        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.pos_x = 25 * x
        self.pos_y = 25 * y
        self.target_pos_x = 25 * x
        self.target_pos_y = 25 * y

    # Draw the wall
    def draw(self, window):
        pygame.draw.rect(window, (100, 100, 100), (self.pos_x, self.pos_y, 25, 25))