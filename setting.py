# write basic setting of the game into the json file

import json
import numpy as np

path = "tests/bigworld.json"
introduction = "Any live cell with two or three neighbors survives.\n" + \
            "Any dead cell with three live neighbors becomes a live cell."

SYMBOL_DEAD = '-' # dead cell symbol
SYMBOL_LIVE = 'o' # live cell symbol
ROW = 30 # row of map
COLUMN = 30 # column of map
PERCENT_DEAD = 0.5 # percentage of dead cell
PERCENT_LIVE = 1 - PERCENT_DEAD # percentage of live cell
ITERATION = 10

world = np.random.choice([0, 1], ROW*COLUMN, 
            p = [PERCENT_DEAD, PERCENT_LIVE]).reshape(ROW, COLUMN)
world = world.tolist()

content = {
    'title':'======Game of Life======',
    'introduction':introduction,
    'world':world,
    'size':[ROW, COLUMN],
    'dead':{'symbol':SYMBOL_DEAD, 'percentage':PERCENT_DEAD},
    'live':{'symbol':SYMBOL_LIVE, 'percentage':PERCENT_LIVE},
    'iteration':ITERATION
}

with open(path, 'w') as file:
    json.dump(content, file)