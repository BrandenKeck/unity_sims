import pickle
import numpy as np

class player():

    def __init__(self, name, img, x, y):

        # Initialize player name
        self.name = name
        self.img = img

        # Initial Position - Episode Memory
        self.init_x = x
        self.init_y = y

        # Position Attributes
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.pos_x = 25 * x
        self.pos_y = 25 * y
        self.target_pos_x = 25 * x
        self.target_pos_y = 25 * y

        # Agent Attributes
        # For each policy:
        #    0 -> Do Nothing
        #    1 -> North Probability
        #    2 -> East Probability
        #    3 -> South Probability
        #    4 -> West Probability
        self.team = 1
        self.prev_state = 0
        self.prev_action = 0
        self.curr_state = -1
        self.rewards = []
        self.states, self.policies, self.Q = self.get_player_data()

    def act(self, current_state):

        # Check for an existing policy for the given state
        policy = [0.2, 0.2, 0.2, 0.2, 0.2]
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

        # Randomly chose an action based on policy
        action = policy.index(max(policy))
        diceroll = np.random.random(1)[0]
        for idx, c in enumerate(cumprobs):
            if diceroll <= c:
                action = idx
                break

        # Take the decided action
        if action == 1:
            self.set_target(0, -1)
        elif action == 2:
            self.set_target(1, 0)
        elif action == 3:
            self.set_target(0, 1)
        elif action == 4:
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
            Q_next = [0, 0, 0, 0, 0]

            # Add new state, policy, and q table
            self.states.append(np.copy(current_state))
            self.policies.append([0.2, 0.2, 0.2, 0.2, 0.2])
            self.Q.append([0, 0, 0, 0, 0])
            self.curr_state = len(self.states) - 1

        # Update Q table for prev state:
        max_Q_next = max(Q_next)
        rewards_last = self.rewards[len(self.rewards) - 1]
        self.Q[self.prev_state][self.prev_action] = self.Q[self.prev_state][self.prev_action] + alpha * (
                    rewards_last + gamma * max_Q_next - self.Q[self.prev_state][self.prev_action])

        # Add heuristics to create reasonable nondeterministic policies
        one_percent_of_range = 0.01 * np.abs(max(self.Q[self.prev_state]) - min(self.Q[self.prev_state]))
        normalized_Q = [0, 0, 0, 0, 0]
        for a in np.arange(len(self.Q[self.prev_state])):
            normalized_Q[a] = self.Q[self.prev_state][a] - min(self.Q[self.prev_state]) + one_percent_of_range

        # Create an E-soft-ish policy
        normalized_sum = sum(normalized_Q)
        if normalized_sum == 0:
            self.policies[self.prev_state] = [0.2, 0.2, 0.2, 0.2, 0.2]
        else:
            for a in np.arange(len(self.policies[self.prev_state])):
                self.policies[self.prev_state][a] = normalized_Q[a] / normalized_sum

        # Write to player file to save learned states, policies, and Q functions
        with open(self.name + ".txt", 'wb') as file:
            pickle.dump((self.states, self.policies, self.Q), file)

    # Search for stored state/policy file
    def get_player_data(self):
        try:
            # Read stored player information if it exists
            with open(self.name + ".txt", 'rb') as file:
                states, policies, Q = pickle.load(file)
            return states, policies, Q
        except:
            # Initialize empty player information if no file found
            return [], [], []

    # Purely asthetic function for animating the move of each agent
    def quick_move(self):
        self.x = self.target_x
        self.y = self.target_y
        self.pos_x = self.target_pos_x
        self.pos_y = self.target_pos_y

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