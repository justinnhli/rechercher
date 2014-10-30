#!/usr/bin/env python3

from ast import literal_eval
from collections import Counter, defaultdict, namedtuple
from os.path import exists as file_exists

from search import Domain

class CarSeating(Domain):
    people = ("Alex", "Anda", "Anna", "Emily", "Genia", "Jiyin", "John", "Justin", "Luke", "Patrick", "Phil", "Rachel", "Rung", "Ryan", "Sam", "Sarah", "Suet", "Thomas", "Yuanjin")
    relationships = {
        ("Rung", "Suet"): 1,
        ("Emily", "Rachel"): 1,
        ("Emily", "Phil"): 1,
        ("Alex", "Anda"): 1,
        ("Genia", "Phil"): 1,
        ("Anda", "Genia"): 1,
        ("Genia", "Sam"): 1,
        ("Genia", "John"): 1,
        ("Genia", "Ryan"): 1,
        ("Genia", "Luke"): 1,
        ("Justin", "Ryan"): 1,
        ("Luke", "Ryan"): 1,
        ("Justin", "Luke"): 1,
        ("John", "Justin"): 1,
        ("Justin", "Sam"): 1,
        ("Justin", "Patrick"): 1,
        ("Anda", "Justin"): 1,
        ("Luke", "Sarah"): 1,
        ("Patrick", "Sam"): 1,
        ("Jiyin", "Ryan"): 2,
        ("Anna", "Jiyin"): 2,
        ("Genia", "Patrick"): 3,
        ("Genia", "Justin"): 3,
        ("Anna", "Ryan"): 3,
        ("Anda", "Phil"): 3,
        ("Anna", "Sam"): 3,
        ("Thomas", "Yuanjin"): 4,
    }
    def __init__(self):
        self.costs = defaultdict(int)
        for k, v in CarSeating.relationships.items():
            p1, p2 = k
            self.costs[(p1, p2)] = v
            self.costs[(p2, p1)] = v
    def get_initial_state(self):
        return tuple(len(CarSeating.people) * [None])
    def get_successors(self, state):
        counter = [(car, count) for car, count in Counter(state).most_common() if car is not None]
        assigned = sum(count for car, count in counter)
        if assigned == len(CarSeating.people):
            return []
        if any(i >= j for i, j in zip((count for car, count in counter), (7, 6, 6))):
            return []
        successors = []
        for car in range(3):
            successor = list(state)
            successor[assigned] = car
            successor = tuple(successor)
            successors.append(((assigned, car), successor, self.cost(state, (assigned, car), successor)))
        return successors
    def cost(self, cur_state, action, next_state):
        cost = 0
        person = CarSeating.people[action[0]]
        for index, car in enumerate(cur_state):
            if car == action[1]:
                other = CarSeating.people[index]
                cost -= self.costs[(person, other)]
        return cost
    def fitness(self, state):
        fitness = 0
        for i, person_car in enumerate(state):
            if person_car == None:
                continue
            person = CarSeating.people[i]
            for j, other_car in enumerate(state[i+1:], start=i+1):
                if other_car == None:
                    continue
                if person_car == other_car:
                    other = CarSeating.people[j]
                    fitness += self.costs[(person, other)]
        return fitness

class GridWorld(Domain):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    @staticmethod
    def get_state_class():
        return namedtuple("State", ("x", "y"))
    def get_successors(self, state):
        successors = []
        if state.x - 1 > 0:
            successors.append(("left", GridWorld.get_state_class()(x=state.x-1, y=state.y), 1))
        if state.y - 1 > 0:
            successors.append(("down", GridWorld.get_state_class()(x=state.x, y=state.y-1), 1))
        if state.x + 1 <= self.width:
            successors.append(("right", GridWorld.get_state_class()(x=state.x+1, y=state.y), 1))
        if state.y + 1 <= self.width:
            successors.append(("right", GridWorld.get_state_class()(x=state.x, y=state.y+1), 1))
        return successors

class WordLadder(Domain):
    @staticmethod
    def get_state_class():
        return str
    def __init__(self, fixed_length=True):
        self.links = {}
        assert file_exists("links")
        with open("links") as fd:
            self.links = literal_eval("{" + fd.read() + "}")
        self.fixed_length = fixed_length
    def get_successors(self, state):
        successors = []
        for next_word in self.links[state]:
            if self.fixed_length and len(state) != len(next_word):
                continue
            cost = 1
            successors.append((None, next_word, cost))
        return successors
