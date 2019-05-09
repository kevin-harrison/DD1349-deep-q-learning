import numpy as np
import random
import math
import copy
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
import tensorflow

from NeuralNetwork import Network
from AI_learning import CartPole

class DeepLearner(object):

    def __init__(self):

        # Create game environment
        self.environment = CartPole()
        self.num_actions = 2
        self.num_state_variables = 4

        # Create Networks
        #self.learning_rate = 0.02
        self.q_network = self.create_model()
        self.target_network = self.create_model()
        self.update_target_model()
        tf.logging.set_verbosity(tf.logging.ERROR)

        # Set Q learning parameters
        self.memory_replay = deque(maxlen=200) # TODO: find a better data structure that can pop first element in O(1) and access in O(1)
        self.discount_factor = 0.8
        self.iterations = 500000
        self.exploration_rate = 1


    def create_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.num_state_variables, activation="softmax"))
        model.add(Dense(24, activation="softmax"))
        model.add(Dense(self.num_actions, activation="softmax"))
        model.compile(loss="mean_squared_error", optimizer="adam")
        return model


    def update_target_model(self):
        self.target_network.set_weights(self.q_network.get_weights())


    def print(self):
        """Prints out classes fields"""
        print("Memories:", len(self.memory_replay))
        print("Q-Network:")
        print(self.q_network)


    def episode(self):
        """Execute an episode of the Q learning algorithm

        Starts at a random state and ends when the goal state is reached. After calling this function many times
        the policy should be a "good" solution to the prob5lem
        """
        # Get starting state
        #state = self.environment.random_state()
        state = self.environment.get_start_state()

        for i in range(1000):

            # Populate memory replay
            while(len(self.memory_replay) < 200):
                state_transition = self.get_state_transition(state, i)
                self.memory_replay.append(state_transition)
                if state_transition[4] == True:
                    state = self.environment.random_state()
                else:
                    state = state_transition[3]

            # Add transition to memory
            state_transition = self.get_state_transition(state, i)
            self.memory_replay.append(state_transition)

            # Train on memories
            self.replay()

            # Go to next state
            if state_transition[4] == True:
                state = self.environment.random_state()
            else:
                state = state_transition[3]


    def replay(self):
        # Get minibatch targets
        minibatch = random.sample(self.memory_replay, 50)

        for state, action, reward, next_state, is_end_state in minibatch:
            # Reshape state to fit in network
            state_vector = state.reshape((1,4))
            next_state_vector = next_state.reshape((1,4))

            target = reward
            if not is_end_state:
                prediction = self.target_network.predict(next_state_vector)
                target = reward + (self.discount_factor * np.amax(prediction))

            target_vector = self.q_network.predict(state_vector)
            target_vector[0][action] = target
            self.q_network.fit(state_vector, target_vector, epochs=1, verbose=0)

            # TEMPORARY
            if self.exploration_rate > 0:
                self.iterations -= 1
                self.exploration_rate -= 1 / self.iterations

        self.update_target_model()


    def get_state_transition(self, state, i):
        # Select an action
        actions = self.q_network.predict(state.reshape((1,4)))
        #exploration_factor = 1 / math.sqrt(i + 1)
        #if random.uniform(0,1) > exploration_factor:
        if random.random() > self.exploration_rate:
            action = random.randint(0, len(actions)-1)
        else:
            action = np.argmax(actions)

        # Create state transition tuple
        next_state, reward, is_end_state = self.environment.get_next_state(state, action)
        return [state, action, reward, next_state, is_end_state]


    def play_game(self):
        state = self.environment.get_start_state()
        is_end_state = False
        total_reward = 0

        while not is_end_state:
            action = np.argmax(self.q_network.predict(state.reshape((1,4))))
            state, reward, is_end_state = self.environment.get_next_state(state, action)
            total_reward += reward

        print(total_reward)
        return total_reward

# Example
'''
rl = DeepLearner()

for i in range(5):
    print("EPISODE", i+1)
    rl.episode()
    rl.play_game()
'''
state = np.array([[1],[2],[3],[4]])
state2 = np.array([1,2,3,4]).reshape((4,1))

print(state.shape)
print(state2.shape)