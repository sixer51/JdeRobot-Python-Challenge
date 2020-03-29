from Life import GameofLife
import time
import random

game = GameofLife()
game.time_interval = 0.2
# test an empty random world
game.load('tests/empty.json')
time.sleep(2)
game.auto_generate()

# test a small random world
game.load('tests/smallworld.json')
time.sleep(2)
game.auto_generate()

# test a big random world
game.load('tests/bigworld.json')
time.sleep(2)
game.auto_generate()

# test random size world
for _ in range(3):
    game.iteration = 6
    game.row = random.randrange(1, 30)
    game.column = random.randrange(1, 30)
    game.generate_new_world()
    print("test random size world: "+str(game.row)+'*'+str(game.column))
    time.sleep(2)
    game.auto_generate()

# test pattern mode
print("Start to test pattern mode")
time.sleep(2)
game.row = 15
game.column = 15
game.iteration = 6
game.mode = "pattern"
game.generate_new_world()

# test a world with only block pattern
for num in range(1, 4):
    print("add "+str(num)+" blocks")
    time.sleep(2)
    game.add_block(num)
    game.auto_generate()

# test a world with only blinker pattern
for num in range(1, 4):
    print("add "+str(num)+" blinkers")
    time.sleep(2)
    game.generate_new_world()
    game.add_blinker(num)
    game.auto_generate()

# test a world with only gliders pattern
for num in range(1, 4):
    print("add "+str(num)+" gliders")
    time.sleep(2)
    game.generate_new_world()
    game.add_glider(num)
    game.auto_generate()

# test a world with block, blinker and glider
for _ in range(3):
    num_block = random.randrange(1, 3)
    num_blinker = random.randrange(1, 3)
    num_glider = random.randrange(1, 3)
    print("add "+str(num_block)+" blocks, " +str(num_blinker)+" blinkers, "+str(num_glider)+" gliders")
    time.sleep(2)
    game.generate_new_world()
    game.add_block(num_block)
    game.add_blinker(num_blinker)
    game.add_glider(num_glider)
    game.auto_generate()

# test long iteration
print("test long iteration")
time.sleep(2)
game.time_interval = 0.001
game.iteration = 10000
game.generate_new_world()
game.add_block(2)
game.add_blinker(2)
game.add_glider(2)
game.auto_generate()