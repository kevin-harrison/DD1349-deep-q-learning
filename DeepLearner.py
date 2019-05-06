import numpy as np
import random
import queue
from NeuralNetwork.py import Network

class DeepLearner:

    def __init__(self):
        """
        learning_rate and discount_factor are hyperparameters whose values are not set in stone
        """
        self.learning_rate = 0.2
        self.discount_factor = 0.8
        self.num_actions = 2
        self.num_state_variables = 4
        self.q_network = Network([num_state_variables, 5, num_actions])
        self.environment = Cartpol()
        self.replay_memory = queue.Queue(10000)
        

    def print(self):
        """Prints out classes fields"""
        print("Learning Rate: " + str(self.learning_rate))
        print("Discount Factor: " + str(self.discount_factor))
        print("Q-Network:")
        print(self.q_network)

    def episode(self, replay_memory, state):
        """Execute an episode of the Q learning algorithm

        Starts at a random state and ends when the goal state is reached. After calling this function many times
        the policy should be a "good" solution to the problem
        """
        # get random starting state
        
        for i in range(50): # 50?
            actions = self.q_network.feedforward(state)
            
            exploration_factor = 1 / sqrt(i + 1)
            if random.uniform(0,1) > exploration_factor: # choose random action
                action = random.randint(0, len(actions)-1)
                #est_reward = actions[choice]
            else: # choose best action
                action, estimated_reward = max(actions)
        
            next_state, reward, end_state = self.environment.get_state(state, action)
            replay_memory.append([state, action, reward, next_state])

            if end_state:
                break
            else:
                state = next_state
                
            
            
                
            

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
rl = DeepLearner()
rl.print()
for i in range(100):
    print("EPISODE", i+1)
    rl.episode()
    print("Current policy:")
    print(rl.q_matrix)
                            
                            
