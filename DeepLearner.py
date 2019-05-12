import numpy as np
import random
from collections import deque

from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers

class DeepLearner(object):

    def __init__(self, state_size, action_size):

        # Set Q learning parameters
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.discount_factor = 0.95
        self.exploration_rate = 1
        self.exploration_decay = 0.001
        self.learning_rate = 0.001

        # Create Networks
        self.q_network = self.create_network()
        self.target_network = self.create_network()
        self.update_target_network()


    def create_network(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=optimizers.Adam(lr=self.learning_rate))
        return model


    def update_target_network(self):
        self.target_network.set_weights(self.q_network.get_weights())


    def remember(self, state, action, reward, next_state, is_done):
        self.memory.append((state, action, reward, next_state, is_done))


    def act(self, state):
        if np.random.rand() <= self.exploration_rate:
            self.exploration_rate -= self.exploration_decay
            return random.randrange(self.action_size)
        act_values = self.q_network.predict(state)
        return np.argmax(act_values[0])


    def replay(self, batch_size):
        #sample random transitions
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                Q_next=self.target_network.predict(next_state)[0]
                target = reward + (self.discount_factor * \
                    np.amax(Q_next))

            target_f = self.q_network.predict(state)
            target_f[0][action] = target
            #train network
            self.q_network.fit(state, target_f, epochs=1, verbose=0)