from gamestate import GameState
from tree import GameStateTree
from algo import minimax, alphabeta

# Sākotnējā spēles inicializācija (izsaukta, kad sāk spēli no jauna)
def initialize_game(game_length, ai_start):
    game = GameState(ai_start, game_length)
    game_tree = GameStateTree()
    print(f"Spēles koks ar dziļumu: {game.dynamic_depth()}")

    return game, game_tree

if __name__ == "__main__":
    while True:
        game_length = int(input("Ievadiet spēles garumu: "))
        ai_start = input("Vai dators sāk spēli? (y/n): ").strip().lower() == 'y'
        algo_input = int(input("Izvēlieties algoritmu (1 - Minimax, 2 - Alpha-Beta): "))
        algo = minimax if algo_input == 1 else alphabeta

        # Inicializē spēli
        game, game_tree = initialize_game(game_length, ai_start)
        print(f"Spēli sāk { 'Dators' if ai_start else 'Spēlētājs' }")
        print("-----------------")

        # Spēles cikls, kamēr spēle nav beigusies
        while not game.game_over():
            game.print_state()
            move_list = game.available_moves()
            print(f"Gājienu izvēle: {move_list}")

            scores = []
            # ChatGPT kods // Izdrukā gājienu vērtējumus
            # Evaluate each available move's score from the current state
            for idx, move in enumerate(game.available_moves(), start=1):
                cloned_state = game.clone_state()  # Clone the current state
                if cloned_state.make_move(idx, cloned_state.ai_turn):
                    eval_result = cloned_state.evaluate()  # (score, point_diff, move_score)
                    scores.append(round(eval_result, 2))
            # // ChatGPT kods beidzas
            print(f"Gājienu vērtējumi: {scores}")

            # Katrā datora gājienā pārtaisa spēles koku
            if game.ai_turn:
                game_tree.create_tree(game)
                _, move = algo(game_tree.root)
                print(f"Dators veic gājienu: { move }, izmantojot algoritmu: { algo.__name__ }")
            else:
                move = int(input("Ievadiet gājiena numuru: "))

            # Pārbauda vai gājiens ir izdarāms un izdara to
            if not game.make_move(move, game.ai_turn) :
                print("Nederīgs gājiens")
                continue

            print("-----------------")


        print(f"{ 'Uzvarēja dators' if game.winner() == 1 else 'Uzvarēja spēlētājs' if game.winner() == 2 else 'neizšķirts' }")
        game.print_state()

        if input("Atkārtot spēli? (y/n): ").strip().lower() != 'y':
            break
