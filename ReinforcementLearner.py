import numpy as np
import random

class ReinforcementLearner:
    """Example of a simple Q learning implementations

    Learns to solve the problem explained here http://mnemstudio.org/path-finding-q-learning-tutorial.htm
    """

    def __init__(self):
        """
        learning_rate and discount_factor are hyperparameters whose values are not set in stone
        q_matrix is the current policy
        reward_matrix is hard coded rewards where -1 = no pathway
        goal_state is the hard coded goal of getting to room 5
        """
        self.learning_rate = 0.2
        self.discount_factor = 0.8
        self.goal_state = 5;
        self.reward_matrix = np.matrix([[-1, -1, -1,  -1,  0, -1],
                                       [-1, -1, -1,   0, -1, 100],
                                       [-1, -1, -1,   0, -1, -1],
                                       [-1,  0,  0,  -1,  0, -1],
                                       [ 0, -1, -1,   0, -1, 100],
                                       [-1,  0, -1,  -1,  0, 100]])
        self.q_matrix = np.zeros((6,6))
        

    def print(self):
        """Prints out classes fields"""
        print("Learning Rate: " + str(self.learning_rate))
        print("Discount Factor: " + str(self.discount_factor))
        print("Goal: " + str(self.goal_state))
        print("Rewards:")
        print(self.reward_matrix)
        print("Q-Table:")
        print(self.q_matrix)

    def episode(self):
        """Execute an episode of the Q learning algorithm

        Starts at a random state and ends when the goal state is reached. After calling this function many times
        the policy should be a "good" solution to the problem
        """
        state = random.randint(0,5) # choose random starting point
        
        while state != self.goal_state:
            # Use current policy (q_matrix) to get next action
            action = self.get_action(state) 

            # Update policy
            self.q_matrix[state, action] = self.reward_matrix[state, action] + (self.discount_factor * self.q_matrix[action, self.get_action(action)])

            # Go to next state
            state = action

    def get_action(self, state):
        """Chooses the best action given a state using the current policy"""
        actions = []
        best_reward = 0
        i = 0
        for reward in np.nditer(self.q_matrix[state]):
            if self.reward_matrix[state, i] != -1:
                if reward == best_reward:
                    actions.append(i)
                elif reward > best_reward:
                    actions = [i]
                    best_reward = reward
            i += 1
        return random.choice(actions)
    

# Example
rl = ReinforcementLearner()
rl.print()
for i in range(20):
    print("EPISODE", i+1)
    rl.episode()
    print("Current policy:")
    print(rl.q_matrix)
                            
                            
