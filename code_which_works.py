from classes import Game


def main():
    game = Game() 
    game_objects_pool = game.setup_game()

    while 1:
        game.update_game_screen(*game_objects_pool)

if __name__ == '__main__':
    main()
