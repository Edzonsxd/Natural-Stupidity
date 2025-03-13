import math

def minimax(node):
    if node.is_terminal():
        return node.evaluate(), None

    if node.current_player == 1:  # Computer's turn: maximizer
        best_val = -math.inf
        best_move = None
        for child in node.generatechildren():
            val,  = minimax(child)
            if val > best_val:
                best_val = val
                best_move = child.move
        return best_val, best_move
    else:  # Human's turn: minimizer
        best_val = math.inf
        best_move = None
        for child in node.generatechildren():
            val,  = minimax(child)
            if val < best_val:
                best_val = val
                best_move = child.move
        return best_val, best_move

def alphabeta(node, alpha=-math.inf, beta=math.inf):
    if node.is_terminal():
        return node.evaluate(), None

    if node.current_player == 1:  # Maximizer turn (computer)
        best_val = -math.inf
        best_move = None
        for child in node.generatechildren():
            val,  = alphabeta(child, alpha, beta)
            if val > best_val:
                best_val = val
                best_move = child.move
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_val, best_move
    else:  # Minimizer turn (human)
        best_val = math.inf
        best_move = None
        for child in node.generatechildren():
            val,  = alphabeta(child, alpha, beta)
            if val < best_val:
                best_val = val
                best_move = child.move
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val, best_move
def alphabeta(): 
    return

import random
def random_move(game):
    return random.randint(1, len(game.available_moves()))

if __name__ == "__main__":
    print("Palaid main.py nevis šo, mīļumiņ!")
