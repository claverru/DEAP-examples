import random
# import multiprocessing

from string import printable
from deap import creator, base, tools, algorithms


def evaluate(individual, obj):
	val = 0
	for i in range(len(individual)):
		if individual[i] == obj[i]:
			val += 1
	return val, 


def mutate(individual, indpb):
	individual[random.randrange(len(individual))] = random.choice(printable)
	return individual,


def generate(population, toolbox, ngen=1000):
	for gen in range(ngen):
		offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.4)
		fits = toolbox.map(toolbox.evaluate, offspring)
		for fit, ind in zip(fits, offspring):
			ind.fitness.values = fit
		population = toolbox.select(offspring, k=len(population))
		best = tools.selBest(population, k=1)[0]
		best_str = ''.join(best)
		fit_per = best.fitness.values[0]/len(objective)
		print("Generación {}/{}: {}\n{}".format(gen+1, ngen, fit_per, best_str))
		if best_str == objective:
			break


if __name__ == '__main__':

	objective = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
	
	creator.create("FitnessMax", base.Fitness, weights=(1.0,))
	creator.create("Individual", list, fitness=creator.FitnessMax)
	
	toolbox = base.Toolbox()

	# pool = multiprocessing.Pool()
	# toolbox.register('map', pool.map)
	
	toolbox.register("printable", random.choice, printable)
	toolbox.register(
			"individual", 
			tools.initRepeat, 
			creator.Individual, 
			toolbox.printable, 
			n=len(objective))
	
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	toolbox.register("evaluate", evaluate, objective)
	toolbox.register("mate", tools.cxTwoPoint)
	toolbox.register("mutate", mutate, indpb=0.2)
	toolbox.register("select", tools.selTournament, tournsize=3)

	generate(toolbox.population(n=300), toolbox)
