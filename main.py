import tkinter as tk
from gamestate import GameState
from tree import GameStateTree
from algo import minimax, alphabeta
from gui import GameGUI

class GameController:
    def __init__(self, root):
        self.root = root
        self.gui = GameGUI(root, self)

        self.total_visited_nodes = [0]
        self.game_length = 15
        self.ai_starts = True
        self.algo = alphabeta

    def start_game_from_setup(self):
        try:
            length = int(self.gui.length_entry.get())
            if not 15 <= length <= 25:
                raise ValueError
        except ValueError:
            self.gui.update_info("Lūdzu ievadiet skaitli no 15 līdz 25")
            return

        self.game_length = length
        self.ai_starts = self.gui.turn.get() == "ai"
        algo_choice = self.gui.algo_var.get()
        self.algo = minimax if algo_choice == "minimax" else alphabeta #noklusējumā tiks izvēlēts alfa-beta algoritms

        self.start_game()

    def start_game(self):
        self.total_visited_nodes = [0]
        self.game = GameState(self.ai_starts, self.game_length)
        self.tree = GameStateTree()

        self.gui.setup_game_screen()
        self.update_view()

        if self.game.ai_turn:
            self.root.after(500, self.computer_move)

    def update_view(self):
        self.gui.update_board(self.game.board, self.game.available_moves())
        self.gui.update_info(f"Punkti: {self.game.points} | {'Datora' if self.game.ai_turn else 'Spēlētāja'} gājiens")

    def make_move(self, move_index):
        if self.game.ai_turn:
            return

        move_pair = self.game.available_moves()[move_index - 1]
        success = self.game.make_move(move_index, self.game.ai_turn)
        if not success:
            self.gui.update_info("Kļūda: Nederīgs gājiens!")
            return

        self.gui.add_move_to_history(
            f"Spēlētājs: {move_pair} → {self.game.board[move_index - 1]} | Punkti: {self.game.points}"
        )

        self.update_view(highlight_index=move_index - 1)
        self.check_game_over_or_continue()

    def computer_move(self):
        self.tree.create_tree(self.game)
        _, move = self.algo(self.tree.root, self.total_visited_nodes)

        if move is not None:
            move_pair = self.game.available_moves()[move - 1]
            self.game.make_move(move, self.game.ai_turn)
            self.gui.add_move_to_history(
                f"Dators: {move_pair} → {self.game.board[move - 1]} | Punkti: {self.game.points}"
            )
            self.update_view(highlight_index=move - 1)

        self.check_game_over_or_continue()

    def update_view(self, highlight_index=None):
        self.gui.update_board(self.game.board, self.game.available_moves(), highlight_index)
        self.gui.update_info(f"Punkti: {self.game.points} | {'Datora' if self.game.ai_turn else 'Spēlētāja'} kārta")

    def check_game_over_or_continue(self):
        if self.game.game_over():
            self.gui.update_board(self.game.board)
            self.gui.game_over(self.game.winner(), self.game, self.total_visited_nodes[0])
        elif self.game.ai_turn:
            self.root.after(500, self.computer_move)

if __name__ == "__main__":
    root = tk.Tk()
    controller = GameController(root)
    root.mainloop()