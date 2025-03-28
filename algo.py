import math

def minimax(node):
    if node.state.game_over():
        return node.state.evaluate(), None
    
    if not node.children:
        return node.state.evaluate(), None

    if node.state.ai_turn:  # Computer's turn: maximizer
        best_val = -math.inf
        best_move = None
        for child in node.children:
            val, _ = minimax(child)
            if val > best_val:
                best_val = val
                best_move = child.move
        return best_val, best_move
    else:  # Human's turn: minimizer
        best_val = math.inf
        best_move = None
        for child in node.children:
            val, _ = minimax(child)
            if val < best_val:
                best_val = val
                best_move = child.move
        return best_val, best_move

def alphabeta(node, alpha=-math.inf, beta=math.inf):
    if node.state.game_over():
        return node.state.evaluate(), None
    
    if not node.children:
        return node.state.evaluate(), None

    if node.state.ai_turn:  # Maximizer turn (computer)
        best_val = -math.inf
        best_move = None
        for child in node.children:
            val, _ = alphabeta(child, alpha, beta)
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
        for child in node.children:
            val, _ = alphabeta(child, alpha, beta)
            if val < best_val:
                best_val = val
                best_move = child.move
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val, best_move

if __name__ == "__main__":
    print("Palaid main.py nevis šo, mīļumiņ!")
