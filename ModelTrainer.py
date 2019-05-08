import matplotlib.pyplot as plt
import numpy as np

# temp libraries
from collections import deque
import random

from DeepLearner import DeepLearner

class ModelTrainer(object):
	def __init__(self):
		self.models = []
		self.training_data = []

	def add_model(self):
		self.models.append(DeepLearner())

	def get_training_data(self, num_episodes):
		self.training_data = [ [self.models[i].play_game()] for i in range(len(self.models))]

		for episode in range(num_episodes):
			for i in range(len(self.models)):
				model = self.models[i]
				model.episode()
				self.training_data[i].append(model.play_game())

	def plot_data(self):
		num_models = len(self.models)
		for i in range(num_models):
			plt.subplot(num_models, 1, i+1)
			plt.plot(np.arange(len(self.training_data[0])), self.training_data[i], "o-")
			plt.xlabel("Episodes")
			plt.ylabel("Score")

		plt.show()


trainer = ModelTrainer()
for i in range(1):
	trainer.add_model()

trainer.get_training_data(10)
trainer.plot_data()