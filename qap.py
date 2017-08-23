import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import monitor
import itertools


def get_random_matrix(rows, columns):
    return np.random.rand(rows, columns)


def get_random_assignment(size):
    return np.random.choice(range(size), size=size, replace=False)


def get_next_assignment(assignment):
    choices = range(len(assignment))
    first_variable, second_variable = np.random.choice(choices, size=2, replace=False)

    next_assignment = list(assignment)
    next_assignment[first_variable], next_assignment[second_variable] = next_assignment[second_variable], next_assignment[first_variable]
    
    return next_assignment


def get_cost(assignment, weights, distances):
    pairs = itertools.permutations(range(len(assignment)), 2)
    return np.sum([weights[loc_1, loc_2] * distances[assignment[loc_1], assignment[loc_2]] for loc_1, loc_2 in pairs])


def anytime_simulated_annealing(size, weights, distances, memory, temperature=1, iterations=1000):
    assignment = get_random_assignment(size)

    best_assignment = assignment 
    best_assignments = [best_assignment]

    for i in range(1, iterations+1):
        next_assignment = get_next_assignment(assignment)

        cost = get_cost(assignment, weights, distances)
        next_cost = get_cost(next_assignment, weights, distances)

        energy_change = cost - next_cost

        if min(1, np.exp(energy_change / temperature)) >= random.random():
            assignment = next_assignment

            best_cost = get_cost(best_assignment, weights, distances)
            if best_cost > next_cost:
                best_assignment = next_assignment

            best_assignments.append(best_assignment)

            memory["solution"] = best_assignment
            memory["cost"] = get_cost(best_assignment, weights, distances)

        temperature = temperature / i
            
    return best_assignments


def main():
    size = 30

    weights = np.matrix( """ 0 27 56 28 64 98 69 69 93 35 41 67 12 33  1 71 72 26 86 67 67 24 10 46 56 56 69 53 48 74;
 27  0 43 94 29 64 97 38 12 99 51 87 76 71 47 47  9 71 20 81 99 45 56 15 99 64 57 84 83 61;
 56 43  0 25 41  8 46 52 22 33 68 52 28 75 99  6 85 65 47 90 24 79 70 28 19 87 80  4 21 34;
 28 94 25  0 12 20 67 24 94 10 64 52 92 49 68 65 66 28 81 17 58 99 90 70 17 57 37  2 37  3;
 64 29 41 12  0 43 20 68 35 60 23 48 40 10 42 83 82 27 49 15 34 50 42 26 33 23 16 69 97 13;
 98 64  8 20 43  0 35 80 40 55 30 22 76 55 56 91 74 82 96  2 13  4  4 35 48 29 42 56  3 30;
 69 97 46 67 20 35  0 60 81 37 42  3 17 25 37 26 88 95 55 53 62 22 44 86 43 43 40 36 53 34;
 69 38 52 24 68 80 60  0 59 43 50 58 62 43  9 22 64 46 68 53  8 30 30 92  6 13 95 76 81 91;
 93 12 22 94 35 40 81 59  0 37 78 90 64 49 46 19 60 93 35 47 69 54 87 12 39 33 54 12 10  4;
 35 99 33 10 60 55 37 43 37  0 88 54 46 82 84  8 29 10 92 62 62 74 48 22 85 23  3 30 12 98;
 41 51 68 64 23 30 42 50 78 88  0 69 29 61 34 53 98 94 33 77 31 54 71 78  8 78 50 76 56 80;
 67 87 52 52 48 22  3 58 90 54 69  0 72 26 20 57 39 68 55 71 19 32 87 41 94 21 21 20 61 13;
 12 76 28 92 40 76 17 62 64 46 29 72  0  5 46 97 61  8 92 33 73  0 16 73 74 44 55 96 67 94;
 33 71 75 49 10 55 25 43 49 82 61 26  5  0 83 28 22 78 55 89 11 99 84 56 30 90 87 80 20 66;
  1 47 99 68 42 56 37  9 46 84 34 20 46 83  0 59 93 79 80 28 68 99 54 69 99  1 49 63 23 33;
 71 47  6 65 83 91 26 22 19  8 53 57 97 28 59  0 99 40 29 60 95 28 44 30 88 66  9 41  3  4;
 72  9 85 66 82 74 88 64 60 29 98 39 61 22 93 99  0 63 61 87 34 28 55 63 10 78 17 90  0 66;
 26 71 65 28 27 82 95 46 93 10 94 68  8 78 79 40 63  0 62 30 76  0 91 62 73 38 49 85 86 88;
 86 20 47 81 49 96 55 68 35 92 33 55 92 55 80 29 61 62  0 13 71 46 75 98 53 52 10 84 70 44;
 67 81 90 17 15  2 53 53 47 62 77 71 33 89 28 60 87 30 13  0  8 52 59 48 85 29 94 79  4 85;
 67 99 24 58 34 13 62  8 69 62 31 19 73 11 68 95 34 76 71  8  0 31 54 95 75 81 11 56 38 95;
 24 45 79 99 50  4 22 30 54 74 54 32  0 99 99 28 28  0 46 52 31  0 37 67 54 88 93 53 44 68;
 10 56 70 90 42  4 44 30 87 48 71 87 16 84 54 44 55 91 75 59 54 37  0 58 98 55 84 76 19 46;
 46 15 28 70 26 35 86 92 12 22 78 41 73 56 69 30 63 62 98 48 95 67 58  0 89 89  5 23 63 19;
 56 99 19 17 33 48 43  6 39 85  8 94 74 30 99 88 10 73 53 85 75 54 98 89  0 53 20 47 17 66;
 56 64 87 57 23 29 43 13 33 23 78 21 44 90  1 66 78 38 52 29 81 88 55 89 53  0 60 86 14 52;
 69 57 80 37 16 42 40 95 54  3 50 21 55 87 49  9 17 49 10 94 11 93 84  5 20 60  0 27 77  5;
 53 84  4  2 69 56 36 76 12 30 76 20 96 80 63 41 90 85 84 79 56 53 76 23 47 86 27  0 37 27;
 48 83 21 37 97  3 53 81 10 12 56 61 67 20 23  3  0 86 70  4 38 44 19 63 17 14 77 37  0 53;
 74 61 34  3 13 30 34 91  4 98 80 13 94 66 33  4 66 88 44 85 95 68 46 19 66 52  5 27 53  0""")
    distances = np.matrix("""  0 21 95 82 56 41  6 25 10  4 63  6 44 40 75 79  0 89 35  9  1 85 84 12  0 26 91 11 35 82;
 21  0 26 69 56 86 45 91 59 18 76 39 18 57 36 61 36 21 71 11 29 82 82  6 71  8 77 74 30 89;
 95 26  0 76 76 40 93 56  1 50  4 36 27 85  2  1 15 11 35 11 20 21 61 80 58 21 76 72 44 85;
 82 69 76  0 94 90 51  3 48 29 90 66 41 15 83 96 74 45 65 40 54 83 14 71 77 36 53 37 26 87;
 56 56 76 94  0 76 91 13 29 11 77 32 87 67 94 79  2 10 99 56 70 99 60  4 56  2 60 72 74 46;
 41 86 40 90 76  0 13 20 86  4 77 15 89 48 14 89 44 59 22 57 63  6  0 62 41 62 46 25 75 76;
  6 45 93 51 91 13  0 40 66 58 30 68 78 91 13 59 49 85 84  8 38 41 56 39 53 77 50 30 58 55;
 25 91 56  3 13 20 40  0 19 85 52 34 53 40 69 12 85 72  7 49 46 87 58 17 68 27 21  6 67 26;
 10 59  1 48 29 86 66 19  0 82 44 35  3 62  8 51  1 91 39 87 72 45 96  7 87 68 33  3 21 90;
  4 18 50 29 11  4 58 85 82  0 45 47 25 30 43 97 33 35 61 42 36 43  7 84  6  0  0 48 62 59;
 63 76  4 90 77 77 30 52 44 45  0 29 94 82 29  3  3 51 67 39 15 66 42 23 62 62 28 76 66 82;
  6 39 36 66 32 15 68 34 35 47 29  0 98 35 15 17 77 44 26 76 86 60 62 62 83 91 57 62 36  2;
 44 18 27 41 87 89 78 53  3 25 94 98  0  2 43 65 37 49 61  5 34 53 96 82 48 28 31 75  1 95;
 40 57 85 15 67 48 91 40 62 30 82 35  2  0  7 92 69 62 32 97  5 39 50 82 93 71 35 14 20 74;
 75 36  2 83 94 14 13 69  8 43 29 15 43  7  0 49 50 37 79 19 51 70 42 26 79 98 60 35  9 96;
 79 61  1 96 79 89 59 12 51 97  3 17 65 92 49  0 70 21 37 37 67 93 93 39  2 52 26 90 26  1;
  0 36 15 74  2 44 49 85  1 33  3 77 37 69 50 70  0 68 93  7 94 19 54 37  0 20 12 11 66 84;
 89 21 11 45 10 59 85 72 91 35 51 44 49 62 37 21 68  0 80  1 55  9 21 12 65  7 17 51 84 87;
 35 71 35 65 99 22 84  7 39 61 67 26 61 32 79 37 93 80  0  2 27 82 71 71 40 93 27 93 92 34;
  9 11 11 40 56 57  8 49 87 42 39 76  5 97 19 37  7  1  2  0 39 31 26  1 87 72 59 97 46 62;
  1 29 20 54 70 63 38 46 72 36 15 86 34  5 51 67 94 55 27 39  0 12 91 63 70  1 22 49 24 58;
 85 82 21 83 99  6 41 87 45 43 66 60 53 39 70 93 19  9 82 31 12  0 62 49 94 92 63 13 45 22;
 84 82 61 14 60  0 56 58 96  7 42 62 96 50 42 93 54 21 71 26 91 62  0 69 70 18  1 44 32  3;
 12  6 80 71  4 62 39 17  7 84 23 62 82 82 26 39 37 12 71  1 63 49 69  0 72 99 34 45 18 96;
  0 71 58 77 56 41 53 68 87  6 62 83 48 93 79  2  0 65 40 87 70 94 70 72  0 82 79 75 83 43;
 26  8 21 36  2 62 77 27 68  0 62 91 28 71 98 52 20  7 93 72  1 92 18 99 82  0 26 81 39 66;
 91 77 76 53 60 46 50 21 33  0 28 57 31 35 60 26 12 17 27 59 22 63  1 34 79 26  0 22 71 58;
 11 74 72 37 72 25 30  6  3 48 76 62 75 14 35 90 11 51 93 97 49 13 44 45 75 81 22  0 42 91;
 35 30 44 26 74 75 58 67 21 62 66 36  1 20  9 26 66 84 92 46 24 45 32 18 83 39 71 42  0 56;
 82 89 85 87 46 76 55 26 90 59 82  2 95 74 96  1 84 87 34 62 58 22  3 96 43 66 58 91 56  0""")

    model = lambda x, a, b, c: a * np.arctan(x + b) + c

    plt.figure()
    plt.xlabel('Time')
    plt.ylabel('Solution Quality')


    costs = monitor.recorder(anytime_simulated_annealing, size, weights, distances)
    qualities = [1504688 / cost for cost in costs]
    plt.plot(range(len(qualities)), qualities)

    qualities = [1818146 / cost for cost in costs]
    plt.plot(range(len(qualities)), qualities)

    # axes = plt.gca()
    # axes.set_ylim([0, 1])
    # steps = range(len(qualities))

    # for end in steps[5:]:
    #     try:
    #         params, _ = curve_fit(model, steps[:end], qualities[:end])
    #         projection = model(steps, params[0], params[1], params[2])
    #         plt.plot(steps, projection)
    #     except:
    #         pass

    plt.show()


if __name__ == '__main__':
    main()

