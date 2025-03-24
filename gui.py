import tkinter as tk
from tkinter import messagebox
from gamestate import GameState
from tree import GameStateTree
from algo import random_move
from algo import alphabeta  # make sure this is imported
from tree import GameStateNode

class NumberGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Skaitļu spēle")
        self.main_menu()
        self.history = []  # Stores tuples like ("Spēlētājs", move, state)

    def main_menu(self):
        # Clear any existing widgets
        self.clear_window()

        tk.Label(self.root, text="Laipni lūdzam skaitļu spēlē!", font=("Helvetica", 16)).pack(pady=20)
        tk.Button(self.root, text="Sākt spēli", width=20, command=self.setup_game).pack(pady=10)
        tk.Button(self.root, text="Iziet", width=20, command=self.root.quit).pack(pady=10)


    def setup_game(self):
        self.clear_window()

        tk.Label(self.root, text="Cik ciparus ģenerēt?", font=("Helvetica", 12)).pack(pady=10)
        self.entry_game_length = tk.Entry(self.root)
        self.entry_game_length.pack(pady=5)

        tk.Button(self.root, text="Ģenerēt spēli", command=self.start_game).pack(pady=10)
        tk.Button(self.root, text="Atpakaļ", command=self.main_menu).pack(pady=5)


    def start_game(self):
        try:
            game_length = int(self.entry_game_length.get())
            if game_length < 2:
                raise ValueError("Virknei jābūt vismaz 2 garai.")
        except ValueError as e:
            messagebox.showerror("Kļūda", f"Nav derīgs skaitlis: {e}")
            return
        
        self.history = []  # ✅ CLEAR HISTORY
        self.game = GameState(p1_turn=True, game_length=game_length)
        self.update_game_screen()


    def update_game_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Spēles stāvoklis", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(self.root, text=f"Cipari: {self.game.board}").pack()
        tk.Label(self.root, text=f"Punkti: {self.game.points}").pack()
        tk.Label(self.root, text="Izvēlieties gājienu:").pack(pady=5)

        move_list = self.game.available_moves()
        self.move_buttons = []

        for idx, move in enumerate(move_list):
            btn = tk.Button(self.root, text=f"{idx+1}: {move}", command=lambda i=idx: self.make_move(i))
            btn.pack(pady=2)
            self.move_buttons.append(btn)

        tk.Button(self.root, text="Atgriezties uz galveno izvēlni", command=self.main_menu).pack(pady=10)
        tk.Label(self.root, text="").pack()
        tk.Label(self.root, text="Gājienu vēsture:", font=("Helvetica", 10, "bold")).pack(pady=(10, 0))
        for who, move, board, points in self.history[-6:]:  # show last 6 moves
            text = f"{who} izvēlējās {move}: {board}, Punkti: {points}"
            tk.Label(self.root, text=text, font=("Helvetica", 9)).pack()
        tk.Button(self.root, text="Eksportēt AI spēles koku", command=self.export_current_tree).pack(pady=5)


    def make_move(self, move_index):
        valid = self.game.make_move(move_index + 1, self.game.p1_turn)
        if not valid:
            messagebox.showwarning("Nederīgs gājiens", "Šis gājiens nav atļauts.")
            return

        if self.game.game_over():
            winner = self.game.winner()
            result = "Uzvarēja spēlētājs!" if winner == 1 else "Uzvarēja dators!" if winner == 2 else "Neizšķirts!"
            messagebox.showinfo("Spēles beigas", result)
            self.main_menu()
        else:
            self.update_game_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        
    def make_move(self, move_index):
        move = move_index + 1
        valid = self.game.make_move(move, self.game.p1_turn)
        if not valid:
            messagebox.showwarning("Nederīgs gājiens", "Šis gājiens nav atļauts.")
            return

        self.history.append(("Spēlētājs", move, self.game.board.copy(), self.game.points.copy()))

        if self.game.game_over():
            self.show_winner()
        elif not self.game.p1_turn:
            self.root.after(500, self.ai_move)
        else:
            self.update_game_screen()


    def ai_move(self):
        tree = GameStateTree()
        tree.create_tree(self.game.clone_state(), max_depth=2)
        node = tree.root
        ai_choices = []

        # Gather all possible moves and their evaluations
        for child in node.generatechildren():
            val, _ = alphabeta(child)
            ai_choices.append((child.move, val))

        # Sort by value (best first)
        ai_choices.sort(key=lambda x: -x[1])

        # Pick the best move
        best_move = ai_choices[0][0]

        # Show AI choices in the GUI
        self.clear_window()
        tk.Label(self.root, text="AI domā...", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(self.root, text=f"Aizdomātie gājieni:").pack()

        for move, score in ai_choices:
            color = "green" if move == best_move else "black"
            text = f"{move}: vērtējums = {score:.2f}"
            tk.Label(self.root, text=text, fg=color).pack()

        # Wait a moment before executing the AI move (so player can see choice)
        self.root.after(1500, lambda: self.execute_ai_move(best_move))


    def execute_ai_move(self, move):
        self.game.make_move(move, self.game.p1_turn)
        self.history.append(("AI", move, self.game.board.copy(), self.game.points.copy()))
        
        if self.game.game_over():
            self.show_winner()
        else:
            self.update_game_screen()


    def show_winner(self):
        winner = self.game.winner()
        result = (
            "Uzvarēja spēlētājs!" if winner == 1
            else "Uzvarēja dators!" if winner == 2
            else "Neizšķirts!"
        )

        self.clear_window()
        tk.Label(self.root, text="Spēles beigas!", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(self.root, text=result, font=("Helvetica", 14)).pack(pady=5)
        
        # ✅ Show move history
        tk.Label(self.root, text="Spēles gājienu vēsture:", font=("Helvetica", 12, "bold")).pack(pady=(15, 5))
        for who, move, board, points in self.history:
            text = f"{who} izvēlējās {move}: {board}, Punkti: {points}"
            tk.Label(self.root, text=text, font=("Helvetica", 10)).pack()

        tk.Button(self.root, text="Atgriezties uz izvēlni", command=self.main_menu).pack(pady=15)

    def export_current_tree(self):
        from tree import GameStateTree
        tree = GameStateTree()
        tree.create_tree(self.game.clone_state(), max_depth=3)  # or more if needed
        tree.export_tree_to_file("exported_game_tree.txt")
        messagebox.showinfo("Eksportēts", "Spēles koks ir saglabāts kā 'exported_game_tree.txt'")


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGameGUI(root)
    root.mainloop()