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

# find max negative

last_row = tableau[tableau.shape[0]-1:]
print('last row', last_row)

a_min = np.argmin(last_row)
print('min ind', a_min)
