# write basic setting of the game into the json file

import json
import numpy as np

path = "config.json"

N = 10
choice = [0, 1]
pattern = np.random.choice(choice, N*N, p = [0.2, 0.8]).reshape(N, N)
pattern = pattern.tolist()
#pattern = [[0, 0, 0],[0, 1, 1], [1, 1, 1]]

content = {
    'title':'Game of Life',
    'pattern':pattern
}

with open(path, 'w') as file:
    json.dump(content, file)
