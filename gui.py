import tkinter as tk
import random
from gamestate import GameStateNode
import algo

# Global game state variables
sequence = []
p1_points = 0
p2_points = 0
current_player = 0  # 0: human, 1: computer
selected_index = None

root = tk.Tk()
root.title("Natural Stupidity Game")

def generate_sequence(length):
    return [random.choice([0, 1]) for _ in range(length)]

def update_display():
    for widget in frame_buttons.winfo_children():
        widget.destroy()
    for i, num in enumerate(sequence):
        btn = tk.Button(frame_buttons, text=str(num), font=("Arial", 20), width=4,
                        command=lambda i=i: on_click(i))
        btn.grid(row=0, column=i)
    label_scores.config(text=f"Human: {p1_points} | Computer: {p2_points}")
    label_turn.config(text="Turn: " + ("Human" if current_player == 0 else "Computer"))

def check_game_over():
    if len(sequence) == 1:
        if p1_points > p2_points:
            result = "Human wins!"
        elif p2_points > p1_points:
            result = "Computer wins!"
        else:
            result = "It's a tie!"
        label_result.config(text=result)
        btn_new_game.config(state=tk.NORMAL)

def apply_move(index):
    global sequence, p1_points, p2_points, current_player
    # Merge pair at positions index and index+1
    pair = [sequence[index], sequence[index+1]]
    if pair == [0,0]:
        if current_player == 0:
            p1_points += 1
        else:
            p2_points += 1
        new_value = 1
    elif pair == [0,1]:
        if current_player == 0:
            p2_points += 1
        else:
            p1_points += 1
        new_value = 0
    elif pair == [1,0]:
        if current_player == 0:
            p1_points += 1
            p2_points -= 1
        else:
            p2_points += 1
            p1_points -= 1
        new_value = 1
    elif pair == [1,1]:
        new_value = 0
    else:
        return

    sequence[index] = new_value
    del sequence[index+1]
    current_player = 1 - current_player
    update_display()
    check_game_over()
    if current_player == 1 and len(sequence) > 1:
        root.after(500, computer_move)

def on_click(index):
    global selected_index
    if current_player != 0:
        return  # Ignore clicks if not human turn
    if selected_index is None:
        selected_index = index
    else:
        if abs(selected_index - index) == 1:
            first = min(selected_index, index)
            apply_move(first)
        selected_index = None

def computer_move():
    global sequence, p1_points, p2_points, current_player
    # Create a game state node from current state and scores.
    node = GameStateNode(state=sequence.copy(), parent=None, move=None, depth=0,
                         p1_points=p1_points, p2_points=p2_points, current_player=current_player)
    algo_choice = var_algo.get()
    if algo_choice == "minimax":
        _, move = algo.minimax(node)
    else:
        _, move = algo.alphabeta(node)
    if move is not None:
        index = move[0]
        apply_move(index)
    else:
        check_game_over()

def start_game():
    global sequence, p1_points, p2_points, current_player, selected_index
    try:
        length = int(entry_length.get())
        if length < 15 or length > 25:
            length = 15
    except:
        length = 15
    sequence = generate_sequence(length)
    p1_points = 0
    p2_points = 0
    current_player = var_first.get()  # 0: human first; 1: computer first
    selected_index = None
    label_result.config(text="")
    btn_new_game.config(state=tk.DISABLED)
    update_display()
    if current_player == 1:
        root.after(500, computer_move)

def new_game():
    start_game()

# Layout
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Enter sequence length (15-25):").grid(row=0, column=0, padx=5)
entry_length = tk.Entry(frame_top)
entry_length.grid(row=0, column=1, padx=5)
entry_length.insert(0, "15")

# Choose starting player
var_first = tk.IntVar(value=0)
tk.Radiobutton(frame_top, text="Human First", variable=var_first, value=0).grid(row=1, column=0)
tk.Radiobutton(frame_top, text="Computer First", variable=var_first, value=1).grid(row=1, column=1)

# Choose algorithm
var_algo = tk.StringVar(value="minimax")
tk.Label(frame_top, text="Algorithm:").grid(row=2, column=0, padx=5)
tk.Radiobutton(frame_top, text="Minimax", variable=var_algo, value="minimax").grid(row=2, column=1)
tk.Radiobutton(frame_top, text="Alpha-Beta", variable=var_algo, value="alphabeta").grid(row=2, column=2)

tk.Button(frame_top, text="Start Game", command=start_game).grid(row=3, column=0, columnspan=3, pady=10)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

label_scores = tk.Label(root, text="Human: 0 | Computer: 0", font=("Arial", 14))
label_scores.pack()

label_turn = tk.Label(root, text="Turn: ", font=("Arial", 14))
label_turn.pack()

label_result = tk.Label(root, text="", font=("Arial", 16, "bold"))
label_result.pack(pady=10)

btn_new_game = tk.Button(root, text="New Game", command=new_game, state=tk.DISABLED)
btn_new_game.pack(pady=5)

root.mainloop()