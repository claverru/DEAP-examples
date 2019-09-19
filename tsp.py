import random

import numpy as np
from deap import creator, base, tools, algorithms


def evaluate(individual):
	return np.sum(distances[individual[:-1], individual[1:]]), 


def generate(population, toolbox, ngen=1000):
	for gen in range(ngen):
		offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.4)
		fits = toolbox.map(toolbox.evaluate, offspring)
		for fit, ind in zip(fits, offspring):
			ind.fitness.values = fit
		population = toolbox.select(offspring, k=len(population))
		best = tools.selBest(population, k=1)[0]
		best_fit = best.fitness.values[0]
		print('Generation {}/{}: {} miles'.format(gen+1, ngen, best_fit))
	# top10 = tools.selBest(population, k=10)


if __name__ == '__main__':

	distances = np.loadtxt('kn57_dist.txt')
	n_cities = len(distances)
	
	creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
	creator.create("Individual", list, fitness=creator.FitnessMin)
	
	toolbox = base.Toolbox()
	
	toolbox.register("order_gen", random.sample, range(n_cities), n_cities)
	toolbox.register(
			"individual", 
			tools.initIterate, 
			creator.Individual, 
			toolbox.order_gen)

	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	toolbox.register("evaluate", evaluate)
	toolbox.register("mate", tools.cxPartialyMatched)
	toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1/n_cities)
	toolbox.register("select", tools.selTournament, tournsize=3)
	
	population = toolbox.population(n=300)
	
	generate(toolbox.population(n=300), toolbox)
