
# LOCAL SEARCH

def steepest_descent(state, successor_fn):
    lowest_state = None
    lowest_cost = None
    for i in range(25):
        for j in range(i+1, 25):
            cur_state = successor_fn(state, i, j)
            cur_cost = cost(cur_state)
            if lowest_cost is None or cur_cost < lowest_cost:
                lowest_state = cur_state
                lowest_cost = cur_cost
    return lowest_state, lowest_cost

def descend(state, successor_fn, iterations):
    terminate = None
    if iterations is None:
        terminate = (lambda x: False)
    else:
        terminate = (lambda x: x == iterations)
    cur_state = state
    cur_cost = cost(cur_state)
    index = 0
    while True:
        if terminate(index):
            break
        next_state, next_cost = steepest_descent(cur_state, successor_fn)
        if next_cost < cur_cost:
            cur_state = next_state
            cur_cost = next_cost
        else:
            break
        index += 1
    return (cur_state, cur_cost)

def beam_search(successor_fn, iterations, beams):
    states = []
    costs = []
    for i in range(iterations):
        lowest_state = None
        lowest_cost = None
        for b in range(beams):
            cur_state = shuffle(initial_state())
            cur_state, cur_cost = descend(cur_state, successor_fn, None)
            if lowest_cost is None or cur_cost < lowest_cost:
                lowest_state = cur_state
                lowest_cost = cur_cost
        states.append(lowest_state)
        costs.append(lowest_cost)
    return zip(states, costs)

