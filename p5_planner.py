import json
from collections import namedtuple

import Queue
import heapq
from math import sqrt

with open('Crafting.json') as f:
	Crafting = json.load(f)
	
#print Crafting['Items']

#print Crafting['Initial']

#print Crafting['Goal']

#print Crafting['Recipes'].items

Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
t_limit = 20
Items = Crafting['Items']

def make_checker(rule):
	if 'Requires' in rule:
		requires = rule['Requires']
	else:
		requires = None
	if 'Consumes' in rule:
		consumes = rule['Consumes']
	else:
		consumes = None
	
	def check(state):
		for i,name in enumerate(Items):
			if requires != None and state.get(name, 0) < requires.get(name, 0):
				return False
			if consumes != None and state.get(name, 0) < consumes.get(name, 0):
				return False
		return True
	
	return check

def make_effector(rule):
	if 'Consumes' in rule:
		consumes = rule['Consumes']
	else:
		consumes = None
	produces = rule['Produces']
	def effect(state):
		if consumes != None:
			for i,name in enumerate(consumes):
				state[name] -= consumes[name]
		for i,name in enumerate(produces):
			state[name] += produces[name]
		return state
	return effect

def make_initial_state(inventory):
	state = {}
	for i,name in enumerate(Items):
		state[name] = inventory.get(name, 0)
	return state

initial_state = make_initial_state(Crafting['Initial'])	
def make_goal_checker(goal):
	goal_state = make_initial_state(Crafting['Goal'])
	def is_goal(state):
		for i,name in enumerate(Items):
			if goal_state.get(name, 0) > state.get(name, 0):
				return False
		return True
	return is_goal

is_goal = make_goal_checker(Crafting['Goal'])

def inventory_to_tuple(d):
	return tuple(d.get(name,0) for i,name in enumerate(Items))

def inventory_to_set(d):
	return frozenset(d.items())
	
def heuristic(state):
	state_score = 0
	if state["bench"] > 1 or state["cart"] > 1 or state["coal"] > 1 or state["cobble"] > 8 or state["furnace"] > 1 or state["ingot"] > 6 or state["iron_axe"] > 1 or state["iron_pickaxe"] > 1 or state["ore"] > 1 or state["plank"] > 4 or state["stick"] > 4 or state["stone_axe"] > 1 or state["stone_pickaxe"] > 1 or state["wood"] > 1 or state["wooden_axe"] > 1 or state["wooden_pickaxe"] > 1:
		state_score = float("inf")
	return state_score

for name,rule in Crafting['Recipes'].items():
	checker = make_checker(rule)
	effector = make_effector(rule)
	recipe = Recipe(name, checker, effector, rule['Time'])
	all_recipes.append(recipe)

def search(graph, initial, is_goal, limit, heuristic):
	frontier = Queue.PriorityQueue()
	initial_frozen = inventory_to_set(initial)
	frontier.put(initial, 0)
	came_from = {}
	cost_so_far = {}
	came_from[initial_frozen] = None
	cost_so_far[initial_frozen] = 0
	current = []
	
	visited = {}
	visited[initial_frozen] = True
	
	state_dict = initial
	
	while not frontier.empty():
		current = frontier.get()
		current_frozen = inventory_to_set(current)
		print(current)
		print ()
		
		if is_goal(current):
			break
		
		for name,next_state,cost in graph(current):
			new_cost = cost_so_far[current_frozen] + cost
			next_frozen = inventory_to_set(next_state)
			if next_frozen not in cost_so_far or new_cost < cost_so_far[next_frozen]:
				visited[next_frozen] = True
				cost_so_far[next_frozen] = new_cost
				priority = new_cost + heuristic(next_state)
				frontier.put(next_state, priority)
				came_from[next_frozen] = current
	
	total_cost = cost_so_far[current_frozen]
	
	plan = []
	this_state = current
	print(came_from)
	
	while this_state != None:
		#print(this_state)
		plan.append(this_state)
		this_state_frozen = inventory_to_set(this_state)
		this_state = came_from[this_state_frozen]
	
	plan.reverse()
	
	return total_cost, plan

def graph(state):
	for r in all_recipes:
		if r.check(state):
			yield (r.name, r.effect(state), r.cost)

"""
def t_graph(state):
	for next_state, cost in edges[state].items():
		yield ((state,next_state), next_state, cost)
		
def t_is_goal(state):
	return state == 'cake'
	
def t_heuristic(state):
	return 0
"""



print search(graph, initial_state, is_goal, t_limit, heuristic)

#print graph(t_initial)

