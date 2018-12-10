import pandas as pd
import random

clients = 100
samples = 7
values = 50

clients = []
for i in range(100):
    for j in range(7):
        clients.append('c'+str(i))

cohort = random.choices(list(range(64)), k=700000)

true_vals = random.choices(list(range(50)), k=700000)
vals = list(map(lambda x: 'v'+str(x), true_vals))

input_vals = pd.DataFrame(list(zip(clients, cohort, vals)), columns=['clients', 'cohort', 'true_values'])

input_vals.to_csv('/Users/Michael/PycharmProjects/untitled1/data/input.csv')