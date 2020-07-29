import numpy as np

'''
STANDARDIZED POLICY FUNCTIONS
'''

# Heuristic policy for exploration when using a value-table learning method
def normalized_q_table_soft_policy(action_values, percent_of_range):

    # Initialize an equally-distributed policy
    policy = np.ones(len(action_values))
    np.true_divide(policy, len(action_values))

    # Add heuristics to create reasonable nondeterministic policies
    exploration_threshold = percent_of_range * np.abs(max(action_values) - min(action_values))
    normalized_Q = np.zeros(len(action_values))
    for a in np.arange(len(action_values)):
        normalized_Q[a] = action_values[a] - min(action_values) + exploration_threshold

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