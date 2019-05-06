import numpy as np
import random

from NeuralNetwork import Network
from AI_learning import CartPole

class DeepLearner(object):

    def __init__(self):
        """
        learning_rate and discount_factor are hyperparameters whose values are not set in stone
        """
        self.learning_rate = 0.2
        self.discount_factor = 0.8
        self.num_actions = 2
        self.num_state_variables = 4
        self.q_network = Network([self.num_state_variables, 5, self.num_actions])
        self.environment = CartPole()
        self.replay_memory = [] # TODO: find a better data structure that can pop first element in O(1) and access in O(1)
        

    def print(self):
        """Prints out classes fields"""
        print("Learning Rate: " + str(self.learning_rate))
        print("Discount Factor: " + str(self.discount_factor))
        print("Q-Network:")
        print(self.q_network)

    def episode(self):
        """Execute an episode of the Q learning algorithm

        Starts at a random state and ends when the goal state is reached. After calling this function many times
        the policy should be a "good" solution to the problem
        """
        # Get starting state
        state = self.environment.random_state()
        
        for i in range(100): # 100? # TODO: train more if we break before 100?

            # Populate memory replay
            while(len(self.memory_replay) < 2000):
                state_transistion = get_state_transition(state, i)
                self.memory_replay.append(state_transition)
                if state_transition[4] == True:
                    state = self.environment.random_state()
                else:
                    state = state_transition[3]
                    
            # Add transition to memory
            state_transistion = get_state_transition(state, i)
            self.memory_replay.append(state_transistion)
            self.memory_replay.pop(0) # INEFFICIENT
            
            # Train minibatch
            minibatch = random.sample(self.memory_replay, 64)
            for state, action, reward, next_state, is_end_state in minibatch:
                target = reward
                prediction = self.q_network.feedforward(next_state) # TODO: use frozen network for prediction
                if not is_end_state:
                    target = reward + self.discount_factor * max(prediction)

                target_vector = prediction
                target_vector[action] = target
                self.q_network.train(state, target_vector)
                    
            # Go to next state
            if state_transition[4] == True:
                state = self.environment.random_state()
            else:
                state = state_transition[3]


    def get_state_transition(self, state, i):
        # Select an action
        actions = self.q_network.feedforward(state)        
        exploration_factor = 1 / sqrt(i + 1)
        if random.uniform(0,1) > exploration_factor: 
            action = random.randint(0, len(actions)-1)
        else:
            action, estimated_reward = max(actions)

        # Create state transition tuple
        next_state, reward, is_end_state = self.environment.get_state(state, action)
        return [state, action, reward, next_state, is_end_state]
        

# Example
rl = DeepLearner()
rl.print()
for i in range(1):
    print("EPISODE", i+1)
    rl.episode()
    print("Current policy:")
    print(rl.q_matrix)
                            
                            
