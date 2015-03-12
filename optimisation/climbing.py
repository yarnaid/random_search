__author__ = 'yarnaid'


def hillclimb(
    init_function,
    move_operator,
    objective_function,
    max_evaluations):
    '''
    hillclimb until either max_evaluations
    is reached or we are at a local optima
    '''
    best = init_function()
    best_score = objective_function(best)

    num_evaluations = 1

    while num_evaluations < max_evaluations:
        # examine moves around our current position
        move_made = False
        for next in move_operator(best):
            if num_evaluations >= max_evaluations:
                break

            # see if this move is better than the current
            next_score = objective_function(next)
            num_evaluations += 1
            if next_score > best_score:
                best = next
                best_score = next_score
                move_made = True
                break # depth first search

        if not move_made:
            break # we couldn't find a better move
                     # (must be at a local maximum)

    return (num_evaluations, best_score, best)

def hillclimb_and_restart(
    init_function,
    move_operator,
    objective_function,
    max_evaluations):
    '''
    repeatedly hillclimb until max_evaluations is reached
    '''
    best = []
    best_score = [0]

    num_evaluations = [0]
    while num_evaluations[-1] < max_evaluations:
        remaining_evaluations = max_evaluations - num_evaluations[-1]

        evaluated, score, found = hillclimb(
            init_function,
            move_operator,
            objective_function,
            remaining_evaluations)

        best_score.append(score)
        best.append(found)

        num_evaluations.append(num_evaluations[-1] + evaluated)

    return (num_evaluations, best_score, best)