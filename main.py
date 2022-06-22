#!/opt/homebrew/bin/python3

import numpy as np

eq = '4x1 + 6x2'

constraints = [
    '-1x1 + 1x2 <= 11',
    '1x1 + 1x2 <= 27',
    '2x1 + 5x2 <= 90',
]

tableau = []

offset = 0
for i,c in enumerate(constraints):
    tableau.append([])
    terms = c.split(' ')
    print(terms)
    r = 0
    for i_t,t in enumerate(terms):
        if 'x' in t:
            tableau[len(tableau)-1].append(
                -int(t[1]) if t[0] == '-' else int(t[0])
            )
        if i_t == len(terms) - 1:
            r = t
    for j, _ in enumerate(constraints):
        tableau[len(tableau)-1].append(
            1 if offset == j else 0
        )
    offset += 1

    tableau[len(tableau)-1].append(int(t))

# add obj function
row = []
eq_s = eq.split(' ')
xs = [x for x in eq_s if 'x' in x]
print(xs)
for i in range(len(tableau[0])):
    if i < len(xs):
        row.append(-(int(xs[i][1]) if xs[i][0] == '-' else int(xs[i][0])))
    else:
        row.append(0)
tableau.append(row)
print('tab:')
tableau = np.array(tableau)
print(tableau)
print('-----------')

import math

def step(tableau):
    # find max negative
    last_row = tableau[tableau.shape[0]-1:]
    last_row = last_row[last_row.shape[0] - 1]

    a_min = np.argmin(last_row)

    exiting_row = tableau.T[a_min]

    last_col = tableau.T[tableau.shape[0] + 1]

    rmInf = lambda a : [0 if x == math.inf or not x or x == -math.inf else x for x in a]
    div = rmInf(np.divide(last_col[0:last_col.shape[0] - 1], exiting_row[0:exiting_row.shape[0] - 1]))

    blowup = lambda arr : [x * -100000 if x < 0 else x for x in arr]

    blow_div = blowup(div)

    exit_var_i = np.argmin(blow_div)

    return tableau, exit_var_i, a_min

def get_pivot(tableau, i, j):
    pivot = tableau[i][j]
    tableau[i] = [(element or 0) / (pivot or 1) for element in tableau[i]]
    for index, row in enumerate(tableau):
       if index != i:
          row_scale = [y * tableau[index][j] for y in tableau[i]]
          tableau[index] = [x - y for x,y in zip(tableau[index], row_scale)]
    return tableau

def find_negatives(row):
        for elem in row:
            if elem < 0:
                return True

has_negatives = True
while has_negatives:
    tableau, i, j = step(tableau)
    tableau = get_pivot(tableau, i, j)
    has_negatives = find_negatives(tableau[tableau.shape[0] - 1])
print(tableau)
