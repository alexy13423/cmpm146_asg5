import json
from collections import namedtuple

with open('Crafting.json') as f:
	Crafting = json.load(f)
	
print Crafting['Items']

print Crafting['Initial']

print Crafting['Goal']

print Crafting['Recipes']['craft stone_pickaxe at bench']

Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
for name,rule in Crafting['Recipes'].items:
	checker = make_checker(rule)
	effector = make_effector(rule)
	recipe = Recipe(name, checker, effector, rule['Time'])
	all_recipes.append(recipe)

def make_checker(rule):
	def check(state):
		
	return check
		

def make_effector(rule):
	def effect(state):
		return next_state
	return check
	
