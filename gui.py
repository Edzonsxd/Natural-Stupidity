import tkinter as tk
from tkinter import messagebox


### PIEZĪME: Grafiskā saskarne izveidota ar ChatGPT palīdzību. 
### Izvēle tika veikta šāda, jo sāka pietrūkt laiks, un tas neietekmē pašu spēles loģiku.
class GameGUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("0-1 Game")

        self.setup_screen = None
        self.board_frame = None
        self.move_buttons = []

        self.show_setup_screen()

    def show_setup_screen(self):
        self.clear_root()

        self.setup_screen = tk.Frame(self.root)
        self.setup_screen.pack(padx=20, pady=20)

        tk.Label(self.setup_screen, text="Spēles garums (15–25):").pack()
        self.length_entry = tk.Entry(self.setup_screen)
        self.length_entry.pack(pady=5)

        tk.Label(self.setup_screen, text="Kurš sāk spēli?").pack()
        self.turn = tk.StringVar(value="player")
        tk.Radiobutton(self.setup_screen, text="Spēlētājs", variable=self.turn, value="player").pack()
        tk.Radiobutton(self.setup_screen, text="Dators", variable=self.turn, value="ai").pack()

        tk.Label(self.setup_screen, text="Izvēlieties algoritmu:").pack()
        self.algo_var = tk.StringVar(value="alphabeta")
        tk.Radiobutton(self.setup_screen, text="Minimax", variable=self.algo_var, value="minimax").pack()
        tk.Radiobutton(self.setup_screen, text="Alpha-Beta", variable=self.algo_var, value="alphabeta").pack()

        tk.Button(self.setup_screen, text="Sākt spēli", command=self.controller.start_game_from_setup).pack(pady=10)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_game_screen(self):
        self.clear_root()

        self.info_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.info_label.pack(pady=10)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack()

        self.restart_button = tk.Button(self.control_frame, text="Jauna spēle", command=self.show_setup_screen)
        self.restart_button.pack()

        self.history_frame = tk.Frame(self.root)
        self.history_frame.pack(pady=5)

        tk.Label(self.history_frame, text="Gājienu vēsture:", font=("Arial", 12)).pack()

        self.history_text = tk.Text(self.history_frame, width=60, height=10, state="disabled", wrap="none")
        self.history_text.pack(side="left")

        scrollbar = tk.Scrollbar(self.history_frame, command=self.history_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_text.config(yscrollcommand=scrollbar.set)

    def update_board(self, board, moves=None, highlight_index=None):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        for idx, val in enumerate(board):
            color = "lightgreen" if idx == highlight_index else "white"
            cell = tk.Label(self.board_frame, text=str(val), width=3, font=("Arial", 16),
                            bg=color, relief="ridge", borderwidth=2)
            cell.grid(row=0, column=idx, padx=1, pady=2)

        if moves is not None:
            self.draw_move_buttons(moves)
        else:
            self.clear_move_buttons()

    def draw_move_buttons(self, moves):
        self.clear_move_buttons()
        for idx, move in enumerate(moves):
            btn = tk.Button(self.board_frame, text=f"{move}", command=lambda i=idx+1: self.controller.make_move(i))
            btn.grid(row=1, column=idx, padx=1, pady=2)
            self.move_buttons.append(btn)

    def clear_move_buttons(self):
        for btn in self.move_buttons:
            btn.destroy()
        self.move_buttons = []

    def update_info(self, text):
        self.info_label.config(text=text)

    def game_over(self, winner, final_state, total_nodes):
        msg = f"Spēle beigusies! Uzvarēja: {'Dators' if winner == 1 else 'Spēlētājs' if winner == 2 else 'Neizšķirts'}\n"
        msg += f"Punkti: {final_state.points}\n"
        msg += f"Datora apskatīto virsotņu skaits: {total_nodes}"
        messagebox.showinfo("Rezultāts", msg)
        self.clear_move_buttons()
    
    def add_move_to_history(self, text):
        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, text + "\n")
        self.history_text.see(tk.END)
        self.history_text.config(state="disabled")

if __name__ == "__main__":
    print("Palaid main.py nevis šo, mīļumiņ!")