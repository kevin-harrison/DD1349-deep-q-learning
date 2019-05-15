import numpy as np
import random
from collections import deque

from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers

class DeepLearner(object):
    """Deep Q Learning agent

    Agent that uses deep q learning to interact with an environment(game)
    by giving it actions. When the environment returns the new state and
    reward agent should learn how to choose actions which maximize the
    reward returned.

    Attributes
    ----------
    memory : deque
        Stores information about the rewards actions taken during a certain
        state gave. Used to decorellate game trajectory with training
    discount_factor : double
        How much to discount the value of future rewards
    exporation_rate : double
        Percent chance that agents choose a random action instead of trying
        to choose the optimal action
    exploration_min : double
        min value exploration_rate can become
    exploration_decay : double
        multiplied to exploration_rate to decrease it over time
    learning_rate : double
        hyperparameter for neural networks
    q_network : keras.Sequential
        Neural network that takes a game state as an input and outputs the
        predicted rewards of each action for that state
    target_network : keras.Sequential
        A network used to create the TD-targets for Q learning. Used to
        stabilize the targets and therefore training
    """

    def __init__(self, state_size, action_size):
        """
        Parameters
        ----------
        state_size : int
            The length of the vector required to represent the game state
        action_size : int
            The length of the vector required to represent all possible actions
            the agent can take
        """

        # Set Q learning parameters
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.discount_factor = 0.95
        self.exploration_rate = 1.0
        self.exploration_min = 0.01
        self.exploration_decay = 0.995
        self.learning_rate = 0.001

        # Create Networks
        self.q_network = self.create_network()
        self.target_network = self.create_network()
        self.update_target_network()


    def create_network(self):
        # Creates a neural network using the keras module

        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=optimizers.Adam(lr=self.learning_rate))
        return model


    def update_target_network(self):
        # Sets target_network's weights equal to q_network's weights

        self.target_network.set_weights(self.q_network.get_weights())

    def load(self, filename):
        # Loads q and target network from file

        self.q_network.load_weights(filename)
        self.update_target_network()

    def save(self, filename):
        # Saves q and target network to file

        self.q_network.save_weights(filename)
        self.update_target_network()


    def remember(self, state, action, reward, next_state, is_done):
        # Adds a state transition to the agent's memory replay

        self.memory.append((state, action, reward, next_state, is_done))


    def act(self, state):
        # Consults the q_network to return the action with the best predicted
        # reward or with chance exploration_rate chooses a random action

        if np.random.rand() <= self.exploration_rate:
            return random.randrange(self.action_size)
        act_values = self.q_network.predict(state)
        return np.argmax(act_values[0])

    def play(self, state):
        # Consults the q_network to return the action with the best predicted
        # reward

        act_values = self.q_network.predict(state)
        return np.argmax(act_values[0])


    def replay(self, batch_size):
        # Selects a number of transistions from memory replay, creates TD-targets
        # and trains on the mean-squared error between the target and q_network
        # prediction. Also decreased exploration_rate

        #sample random transitions
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            # Create TD-target
            target = reward
            if not done:
                Q_next=self.target_network.predict(next_state)[0]
                target = reward + (self.discount_factor * np.amax(Q_next))
            target_f = self.q_network.predict(state)
            target_f[0][action] = target
            #train network
            self.q_network.fit(state, target_f, epochs=1, verbose=0)
        if self.exploration_rate > self.exploration_min:
            self.exploration_rate *= self.exploration_decay