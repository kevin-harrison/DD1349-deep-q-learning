import matplotlib.pyplot as plt
import numpy as np

from DeepLearner import DeepLearner
from AI_learning import CartPole

class ModelTrainer(object):
	def __init__(self):

		self.game = CartPole()
		self.state_size = 4
		self.action_size = 2

		self.models = []
		self.training_data = []

	def add_model(self):
		self.models.append(DeepLearner(self.state_size, self.action_size))

	def get_training_data(self, num_episodes, batch_size):
		agent = self.models[0] # TODO: Allow for training of multiple models at once

		for episode in range(num_episodes):
			state = self.game.reset()
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
				if done:
					agent.update_target_network()
					print("episode: {}/{}, score: {}, e: {:.2}"
						  .format(episode, num_episodes, time, agent.exploration_rate))
					break

				# Train on memories gained from the game
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