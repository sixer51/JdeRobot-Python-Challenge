from Life import Life

if __name__ == "__main__":
    path = 'config.json'
    game = Life(path)

    #game.show_pattern()

    for _ in range(10):
        game.update()

    game.end()