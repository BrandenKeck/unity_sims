# Library Imports
import numpy as np

# Create a Q-Learning Setup for Tabular Reinforcement Learning
class qtable():

    def __init__(self, num):

        # Init number of possible actions per state
        self.num = num

        # Init lists
        self.states = []
        self.action_values = []

        # Init counters
        self.prev_state_idx = -1
        self.curr_state_idx = -1

    # Define a function for the Q Learning (value-table) method
    def q_learning(self, current_state, last_reward, last_action, alpha, gamma):

        # Attempt to find q table for the current state
        next_values = []
        for idx, s in enumerate(self.states):
            if s.tolist() == current_state.tolist():
                next_values = self.action_values[idx]
                self.curr_state_idx = idx

        # Create a new q table and policy for the current state if one doesn't exist
        if next_values == []:
            # Set Default Q Table
            next_values = np.zeros(self.num)

            # Add new state, policy, and q table
            self.states.append(np.copy(current_state))
            self.action_values.append(np.zeros(self.num))
            self.curr_state_idx = len(self.states) - 1

        # Update Q table for prev state, handle first pass:
        if self.prev_state_idx != -1:
            max_next_values = max(next_values)
            self.action_values[self.prev_state_idx][last_action] = self.action_values[self.prev_state_idx][last_action] + alpha * (
                    last_reward + gamma * max_next_values - self.action_values[self.prev_state_idx][last_action])

        self.prev_state_idx = self.curr_state_idx