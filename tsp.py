import random
from deap import creator, base, tools, algorithms
from string import printable
from fuzzywuzzy import fuzz
import numpy as np

distances = np.loadtxt('kn57_dist.txt')

n_cities = len(distances)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

random.sample(range(n_cities), n_cities)

toolbox.register("attr_bool", random.sample, range(n_cities), n_cities)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_bool)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
	d = 0
	for i in range(len(individual)-1):
		d += distances[individual[i]][individual[i+1]]
	return d, 

# TODO: Mirar sus funciones de mutacion para cambiarla por esta
def mutate(individual):
	idx = range(len(individual))
	i1, i2 = random.sample(idx, 2)
	individual[i1], individual[i2] = individual[i2], individual[i1]
	return individual,


toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", mutate)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=300)

print(population[0])
NGEN=1000
for gen in range(NGEN):
	offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.4)
	fits = toolbox.map(toolbox.evaluate, offspring)
	for fit, ind in zip(fits, offspring):
		ind.fitness.values = fit
	population = toolbox.select(offspring, k=len(population))
	best = tools.selBest(population, k=1)[0]
	print('Generacion {}/{} ({} ciudades): {} millas'.format(gen+1, NGEN, len(set(best)), evaluate(best)))
top10 = tools.selBest(population, k=10)


