from gamestate import GameState
from algo import random_move

game_length = 15 # Cik ciparu virkne tiek ģenerēta
p1_start = True # Vai spēli sāk spēlētājs

game = GameState(game_length, p1_start)

print(f"Spēli sāk { 'Spēlētājs' if p1_start else 'dators' }")
print("-----------------")

while not game.game_over():
    game.print_state()
    move_list = game.available_moves()
    print(f"Gājienu izvēle: {move_list}")
    if game.p1_turn:
        move = int(input("Ievadiet gājiena numuru: "))
    else:
        move = random_move(game)
        print(f"Dators veic gājienu: { move } ")

    if not game.make_move(move, game.p1_turn) :
        print("Nederīgs gājiens")
        continue

    print("-----------------")

print(f"{ 'Uzvarēja spēlētājs' if game.winner() == 1 else 'Uzvarēja dators' if game.winner() == 2 else 'neizšķirts' }")
game.print_state()
