class GameStateNode:
    def __init__(self, state, parent, move, depth, p1_points, p2_points, current_player):
        self.state = state          # List of 0/1 digits
        self.parent = parent        # Parent node
        self.move = move            # (index, original pair) that led to this state
        self.depth = depth          # Depth in the game tree
        self.p1_points = p1_points
        self.p2_points = p2_points
        self.current_player = current_player  # 0 for human, 1 for computer

    def is_terminal(self):
        return len(self.state) == 1

    def evaluate(self):
        # Heuristic: computer's points minus human's points.
        return self.p2_points - self.p1_points

    def generate_children(self):
        children = []
        # Try every adjacent pair replacement.
        for i in range(len(self.state) - 1):
            new_state = self.state.copy()
            pair = [new_state[i], new_state[i+1]]
            
            # Copy scores
            p1 = self.p1_points
            p2 = self.p2_points
            cp = self.current_player

            # Apply rules:
            if pair == [0, 0]:
                # Current player gets +1, replace with 1
                if cp == 0:
                    p1 += 1
                else:
                    p2 += 1
                new_value = 1
            elif pair == [0, 1]:
                # Opponent gets +1, replace with 0
                if cp == 0:
                    p2 += 1
                else:
                    p1 += 1
                new_value = 0
            elif pair == [1, 0]:
                # Current gets +1, opponent loses 1, replace with 1
                if cp == 0:
                    p1 += 1
                    p2 -= 1
                else:
                    p2 += 1
                    p1 -= 1
                new_value = 1
            elif pair == [1, 1]:
                # For [1, 1] we assume no score change and replace with 0.
                new_value = 0
            else:
                continue

            # Replace the pair with new_value at i, remove i+1.
            new_state[i] = new_value
            del new_state[i+1]
            
            child = GameStateNode(
                state=new_state,
                parent=self,
                move=(i, pair),
                depth=self.depth + 1,
                p1_points=p1,
                p2_points=p2,
                current_player=1 - cp  # Switch turn
            )
            children.append(child)
        return children
