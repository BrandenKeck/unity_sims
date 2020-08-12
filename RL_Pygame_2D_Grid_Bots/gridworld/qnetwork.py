# Library Imports
from copy import deepcopy
import numpy as np

# Custom Imports
from neural_network import neural_network

# Create a Q-Learning Setup for Deep Q Learning
class qnetwork():

    def __init__(self, num_actions, hidden_layer_sizes):

        # Init number of possible actions per state (network output layer)
        # Init hidden layer sizes
        self.num_actions = num_actions
        self.hidden_layer_sizes = hidden_layer_sizes

        # Init Empty Learning objects
        self.replay_memory = replay_memory()
        self.Q = []
        self.Q_target = []
        self.action_values = np.ones(num_actions)

        # DQN Parameters
        self.replay_memory_capacity = 5000
        self.network_reset_frequency = 50
        self.network_minibatch_size = 30
        self.network_training_delay = 0
        self.network_training_iter = 20
        self.state_queue_length = 3

        # Init counters
        self.network_training_delay_counter = 0
        self.network_reset_counter = 0


    # Run basic function approximation
    def q_approximater(self, state, prev_reward, prev_action, alpha, gamma):

        # Initialize Neural Network Object if first pass
        if self.Q == []:
            self.initialize_q_network(state, alpha)
            return

        # Update Standard Replay Memory Queues
        self.update_replay_memory(state, prev_reward, prev_action)
        if len(self.replay_memory.preprocessed_states) < 2: return

        # Get target labels from Q network predictions
        predicted_Q = []
        for q in self.Q:
            predicted_Q.append(q.classify_data(self.replay_memory.preprocessed_states[len(self.replay_memory.preprocessed_states)-1]))
        target_label = (prev_reward + gamma * max(predicted_Q))
        self.update_queue(self.replay_memory.q_target_labels, target_label, self.replay_memory_capacity)

        # Set action-value label from previous state Q action
        label = np.array(self.action_values[prev_action]).reshape(-1, 1)
        self.update_queue(self.replay_memory.q_labels, label, self.replay_memory_capacity)

        # Train the Q networks
        self.train_q_networks()

        # Set current action values from the action-value network
        self.action_values = []
        for i in np.arange(len(predicted_Q)):
            self.action_values.append(predicted_Q[0][0][0])


    # Run the DQN method
    def dqn(self, state, prev_reward, prev_action, alpha, gamma):

        # Initialize DQN Neural Network Objects if first pass
        if self.Q == [] or self.Q_target == []:
            self.initialize_q_network(state, alpha)
            self.Q_target = deepcopy(self.Q)
            return

        # Update Standard Replay Memory Queues
        self.update_replay_memory(state, prev_reward, prev_action)
        if len(self.replay_memory.preprocessed_states) < 2: return

        # Get target labels from Q network predictions
        predicted_Q = []
        for q in self.Q_target:
            predicted_Q.append(q.classify_data(self.replay_memory.preprocessed_states[len(self.replay_memory.preprocessed_states) - 1]))

        target_label = (prev_reward + gamma * max(predicted_Q))
        self.update_queue(self.replay_memory.q_target_labels, target_label, self.replay_memory_capacity)

        # Set action-value label from previous state Q action
        label = np.array(self.action_values[prev_action]).reshape(-1, 1)
        self.update_queue(self.replay_memory.q_labels, label, self.replay_memory_capacity)

        # Train the Q networks
        self.train_q_networks()

        # If a reset step has been reached, set the target network equal to the current action-value network
        self.network_reset_counter = self.network_reset_counter + 1
        if self.network_reset_counter >= self.network_reset_frequency:
            self.Q_target = deepcopy(self.Q)
            self.network_reset_counter = 0

        # Set current action values from the action-value network
        self.action_values = []
        for q in self.Q:
            self.action_values.append(q.classify_data(self.replay_memory.preprocessed_states[len(self.replay_memory.preprocessed_states) - 1])[0][0])


    # Training function to be enacted on a collection of neural networks used to predict the value of each possible action
    def train_q_networks(self):

        # If the training delay has been met, train the action-value network
        self.network_training_delay_counter = self.network_training_delay_counter + 1
        if self.network_training_delay_counter > self.network_training_delay:
            for iter in np.arange(self.network_training_iter):
                for i in np.arange(self.num_actions):
                    batch = [i for i, x in enumerate(self.replay_memory.actions) if x == i]
                    minibatch_size = min(len(batch), self.network_minibatch_size)
                    batch_idx = np.random.choice(len(batch), size=minibatch_size, replace=False)
                    minibatch = np.array(batch)[batch_idx]

                    X = np.concatenate(self.replay_memory.preprocessed_states, axis=1)[:, minibatch]
                    Y = np.concatenate(self.replay_memory.q_target_labels, axis=1)[:, minibatch]

                    self.Q[i].predict(X)
                    self.Q[i].y_hat = np.concatenate(self.replay_memory.q_labels, axis=1)[:, minibatch]
                    self.Q[i].learn(Y)

                    self.network_training_delay_counter = 0

    # Function to update universally-used state, action, and reward queues
    def update_replay_memory(self, state, prev_reward, prev_action):
        # Create a queue of last states to be concatenated for the Q learning network input
        # If the state queue has not been initialized to the required length, return to parent function
        self.update_queue(self.replay_memory.state_queue, state, self.state_queue_length)
        if len(self.replay_memory.state_queue) < self.state_queue_length: return

        # Concatenate state queue to create network input
        # If the previous concatenated state is blank return to parent function
        preprocessed_state = [state for s in self.replay_memory.state_queue for state in s]
        preprocessed_state = np.array(preprocessed_state).reshape((len(preprocessed_state), 1))
        self.update_queue(self.replay_memory.preprocessed_states, preprocessed_state, self.replay_memory_capacity)
        if len(self.replay_memory.preprocessed_states) < 2: return

        # Update action and reward to the appropriate queues
        self.update_queue(self.replay_memory.actions, prev_action, self.replay_memory_capacity)
        self.update_queue(self.replay_memory.rewards, prev_reward, self.replay_memory_capacity)

    # Create Q using external Neural Network class
    def initialize_q_network(self, state, alpha):

        # Create a list of layer sizes from network settings
        layer_sizes = [self.state_queue_length * np.size(state)]
        for hl in self.hidden_layer_sizes:
            layer_sizes.append(hl)
        layer_sizes.append(1)

        # Create the Q neural networks (one for each action) and init basic settings
        for i in np.arange(self.num_actions):
            self.Q.append(neural_network(layer_sizes))
            self.Q[i].learning_rates = alpha * np.ones(len(layer_sizes))
            self.Q[i].use_sigmoid[len(self.Q[i].use_sigmoid) - 1] = False
            self.Q[i].use_linear[len(self.Q[i].use_linear) - 1] = True

    # Function for updating rolling queues
    def update_queue(self, queue, obj, length):
        queue.append(obj)
        if length > 0:
            while(len(queue) > length): queue.pop(0)

# Create a separate class structure for replay memory lists
class replay_memory():

    def __init__(self):
        self.state_queue = []
        self.preprocessed_states = []
        self.actions = []
        self.rewards = []
        self.q_labels = []
        self.q_target_labels = []