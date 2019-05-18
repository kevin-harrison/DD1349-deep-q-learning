import matplotlib.pyplot as plt
import numpy as np

from DeepLearner import DeepLearner
from AI_learning import CartPole
from SnakeGame import SnakeGame
from car_game import Car


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
		self.game = Car(0,0) # TODO: add more games
		self.state_size = self.game.state_size
		self.action_size = self.game.action_size

		# Training attributes
		self.model = DeepLearner(self.state_size, self.action_size)
		self.training_rewards = []
		self.training_times = []

	def get_training_data(self, num_episodes, batch_size):
		# Trains the agents on the game num_episodes times. Also
		# renders the game at each state

		agent = self.model

		for episode in range(num_episodes):
			state = self.game.reset() # Sets game to starting state
			state = np.reshape(state, [1, self.state_size])
			done = False
			total_reward = 0

			for time in range(1000):
				self.game.render() # Comment out to train faster

				# Get information about state change and remember it
				action = agent.act(state)
				next_state, reward, done = self.game.step(action)
				reward = reward if not done else -10
				total_reward += reward
				next_state = np.reshape(next_state, [1, self.state_size])
				agent.remember(state, action, reward, next_state, done)
				state = next_state

				# If the game is lost print out some stats of the training session
				if done:
					self.training_rewards.append(total_reward)
					self.training_times.append(time)
					agent.update_target_network()
					print("episode: {}/{}, time: {}, reward: {}, e: {:.2}"
						  .format(episode, num_episodes, time, total_reward, agent.exploration_rate))
					break

				# Train on memories of from the game
				if len(agent.memory) > batch_size:
					agent.replay(batch_size)

			if not done:
				self.training_rewards.append(total_reward)
				self.training_times.append(time)
				agent.update_target_network()
				print("episode: {}/{}, time: {}, reward: {}, e: {:.2}"
						  .format(episode, num_episodes, time, total_reward, agent.exploration_rate))


	def plot_data(self):
		plt.subplot(2, 1, 1)
		plt.plot(np.arange(len(self.training_rewards)), self.training_rewards, "-")
		#plt.xlabel("Episodes")
		plt.ylabel("Score")
		plt.subplot(2, 1, 2)
		plt.plot(np.arange(len(self.training_times)), self.training_times, "-")
		plt.xlabel("Episodes")
		plt.ylabel("Time alive")
		plt.show()


trainer = ModelTrainer()
trainer.get_training_data(1000, 32)
trainer.plot_data()
