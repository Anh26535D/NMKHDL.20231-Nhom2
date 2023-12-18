import time

import numpy as np

class Deep_Evolution_Strategy:

    def __init__(
        self, 
        weights, 
        reward_function, 
        population_size, 
        sigma, 
        learning_rate
    ) -> None:
        self.weights = weights
        self.reward_function = reward_function
        self.population_size = population_size
        self.sigma = sigma
        self.learning_rate = learning_rate

    def _get_weights_from_individual(self, weights, individual):
        weights_population = []
        for index, i in enumerate(individual):
            jittered = self.sigma * i
            weights_population.append(weights[index] + jittered)
        return weights_population

    def get_weights(self):
        return self.weights
    
    def init_population(self):
        population = []
        for _ in range(self.population_size):
            x = []
            for w in self.weights:
                x.append(np.random.randn(*w.shape))
            population.append(x)
        return population
    
    def train(self, epoch=100, print_every=1):
        start_time = time.time()
        for i in range(epoch):
            population = self.init_population()

            # Calculate reward for each solution
            rewards = np.zeros(self.population_size)
            for idx, individual in enumerate(population):
                weights_population = self._get_weights_from_individual(self.weights, individual)
                rewards[idx] = self.reward_function(weights_population)
            rewards = (rewards - np.mean(rewards)) / (np.std(rewards) + 1e-7) # Normalize reward

            # Update weights
            for idx, W in enumerate(self.weights):
                A = np.array([individual[idx] for individual in population])
                self.weights[idx] = (
                    W + self.learning_rate / (self.population_size * self.sigma) * np.dot(A.T, rewards).T
                )

            if (i + 1) % print_every == 0:
                print('iter %d. reward: %f' % (i + 1, self.reward_function(self.weights)))
        print('time taken to train:', time.time() - start_time, 'seconds')