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
        self.Q = None
        self.Q_target = None
        self.action_values = np.ones(num_actions)

        # DQN Parameters
        self.replay_memory_capacity = 1000000
        self.network_reset_frequency = 100000
        self.network_minibatch_size = 1000
        self.network_training_delay = 0
        self.state_queue_length = 3

        # Init counters
        self.network_training_delay_counter = 0
        self.network_reset_counter = 0

    # Run the DQN method
    def dqn(self, state, prev_reward, prev_action, alpha, gamma):

        # Initialize DQN Neural Network Objects if first pass
        if self.Q == None or self.Q_target == None:

            # Create a list of layer sizes from network settings
            layer_sizes = [self.state_queue_length * np.size(state)]
            for hl in self.hidden_layer_sizes:
                layer_sizes.append(hl)
            layer_sizes.append(self.num_actions)

            # Create the Q and Q_target neural networks, init basic settings
            self.Q = neural_network(layer_sizes)
            self.Q.learning_rates = alpha * np.ones(len(layer_sizes))
            self.Q.use_sigmoid[len(self.Q.use_sigmoid) - 1] = False
            self.Q.use_linear[len(self.Q.use_linear) - 1] = True
            self.Q_target = deepcopy(self.Q)
            return

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

        # Get target Q value from the target network and set target labels
        tQ = self.Q_target.classify_data(preprocessed_state)
        tLabels = (prev_reward + gamma * max(tQ)) * np.ones(self.num_actions).reshape(-1, 1)
        self.update_queue(self.replay_memory.q_target_labels, tLabels, self.replay_memory_capacity)

        # Set action-value labels from previous state Q prediction
        avLabels = self.action_values[prev_action] * np.ones(self.num_actions).reshape(-1, 1)
        self.update_queue(self.replay_memory.q_labels, avLabels, self.replay_memory_capacity)

        # If the training delay has been met, train the action-value network
        self.network_training_delay_counter = self.network_training_delay_counter + 1
        if self.network_training_delay_counter > self.network_training_delay and len(self.replay_memory.preprocessed_states) > self.network_minibatch_size:
            batch_idx = np.random.choice((len(self.replay_memory.preprocessed_states)-1), size=self.network_minibatch_size, replace=False)
            X = np.concatenate(self.replay_memory.preprocessed_states, axis=1)[:, batch_idx]
            Y = np.concatenate(self.replay_memory.q_target_labels, axis=1)[:, batch_idx]
            self.Q.predict(X)
            self.Q.y_hat = np.concatenate(self.replay_memory.q_labels, axis=1)[:, batch_idx]
            self.Q.learn(Y)
            self.network_training_delay_counter = 0

        # If a reset step has been reached, set the target network equal to the current action-value network
        self.network_reset_counter = self.network_reset_counter + 1
        if self.network_reset_counter >= self.network_reset_frequency:
            self.Q_target = deepcopy(self.Q)
            self.network_reset_counter = 0

        # Set current action values from the action-value network
        self.action_values = self.Q.classify_data(preprocessed_state)

        return


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