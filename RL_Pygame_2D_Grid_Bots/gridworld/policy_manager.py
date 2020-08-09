# Import external libraries
import numpy as np

'''
STANDARDIZED POLICY FUNCTIONS
'''

def e_greedy_policy(action_values):

    n = len(action_values)
    policy = np.zeros(n)

    e = 0.1
    if np.random.rand() < e:
        policy[np.random.randint(n)] = 1
    else:
        policy[action_values.index(max(action_values))] = 1

    return policy



# Heuristic policy for exploration when using a value-table learning method
def normalized_q_table_soft_policy(action_values):

    # Initialize an equally-distributed policy
    policy = np.ones(len(action_values))
    np.true_divide(policy, len(action_values))

    # Calculate Normalized Q
    normalized_Q = np.zeros(len(action_values))
    for a in np.arange(len(action_values)):
        normalized_Q[a] = action_values[a] - min(action_values) + 0.1

    # Create an E-soft-ish policy
    normalized_sum = sum(normalized_Q)
    if normalized_sum == 0:
        return policy
    else:
        for a in np.arange(len(action_values)):
            policy[a] = normalized_Q[a] / normalized_sum

    # return the policy
    return policy

'''
TODO - ADD MORE POLICIES
'''