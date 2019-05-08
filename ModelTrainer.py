import matplotlib.pyplot as plt

class ModelTrainer(object):
	def __init__(self, n):
		self.models = []
		self.training_data = []

	def add_model():
		self.models.append(DeepLearner())

	def get_training_data(self, num_episodes):
		self.training_data = [ [self.models[i].play_game()] for i in range(len(self.models))]

		for episode in range(num_episodes):
			for i in range(len(self.models):
				model = self.models[i]
				model.episode()
				self.training_data[i].append(model.play_game())
