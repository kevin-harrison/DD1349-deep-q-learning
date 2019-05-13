import matplotlib.pyplot as plt
import numpy as np

from DeepLearner import DeepLearner
from AI_learning import CartPole

class ModelTrainer(object):
	"""Facilitates training of DeepLearner agents

	Holds a list of models and trains them to play a specific game. Feeds
	the actions of the DeepLearning agents into the game and gives the agents
	the state transition of that action to train on.

	Attributes
	----------
	game : CartPole
		An environment for the game CartPole. Given actions it can calculate
		the next state of the game as well as the rewards associated.
	state_size : int
		The length of the vector required to represent the game state
 	action_size : int
		The length of the vector required to represent all possible actions
		the agent can take
	models : list
		Holds DeepLearner agents
	training_data : list
		TODO
	"""

	def __init__(self):

		# Game attributes
		self.game = CartPole() # TODO: add more games
		self.state_size = 4
		self.action_size = 2

		# Training attributes
		self.models = []
		self.training_data = []

	def add_model(self):
		# Adds a DeepLearner agent to models

		self.models.append(DeepLearner(self.state_size, self.action_size))

	def get_training_data(self, num_episodes, batch_size):
		# Trains the agents on the game num_episodes times. Also
		# renders the game at each state

		agent = self.models[0] # TODO: Allow for training of multiple models at once

		for episode in range(num_episodes):
			state = self.game.reset() # Sets game to starting state
			state = np.reshape(state, [1, self.state_size])
			done = False

			for time in range(500):
				self.game.render() # Comment out to train faster

				# Get information about state change and remember it
				action = agent.act(state)
				next_state, reward, done = self.game.step(action)
				reward = reward if not done else -10
				next_state = np.reshape(next_state, [1, self.state_size])
				agent.remember(state, action, reward, next_state, done)
				state = next_state

				# If the game is lost print out some stats of the training session
				if done:
					agent.update_target_network()
					print("episode: {}/{}, score: {}, e: {:.2}"
						  .format(episode, num_episodes, time, agent.exploration_rate))
					break

				# Train on memories of from the game
				if len(agent.memory) > batch_size:
					agent.replay(batch_size)

			if not done:
				print("WON THE GAME!")

	'''
	def plot_data(self):
		num_models = len(self.models)
		for i in range(num_models):
			plt.subplot(num_models, 1, i+1)
			plt.plot(np.arange(len(self.training_data[0])), self.training_data[i], "o-")
			plt.xlabel("Episodes")
			plt.ylabel("Score")

		plt.show()
	'''


trainer = ModelTrainer()
for i in range(1):
	trainer.add_model()

trainer.get_training_data(1000, 32)