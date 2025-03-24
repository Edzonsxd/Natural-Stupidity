from gamestate import GameState


class GameStateNode:
    def __init__(self, state, move=None, depth=0):
        self.state = state
        self.move = move
        self.children = []
        self.depth = depth
        self.score = state.evaluate()

    def add_child(self, node):
        self.children.append(node)

    def is_terminal(self):
        return self.state.game_over()

    def evaluate(self):
        score, _, _ = self.state.evaluate()
        return score

    @property
    def current_player(self):
        return 1 if self.state.p1_turn == False else 2  # AI is player 1 (when it's NOT p1_turn)

    def generatechildren(self):
        children = []
        for pos in range(1, len(self.state.available_moves()) + 1):
            clone = self.state.clone_state()
            if clone.make_move(pos, clone.p1_turn):
                child = GameStateNode(clone, move=pos, depth=self.depth + 1)
                children.append(child)
        return children

class GameStateTree:
    def __init__(self):
        self.root = None

    # Inicializē koku, ar rekursīvo funkciju izveido koku
    def create_tree(self, state, max_depth):
        self.root = GameStateNode(state, depth=0)
        self.build_tree(self.root, max_depth)

    # Rekursīvā funkcija
    def build_tree(self, node, max_depth):
        # Koka limitācijas
        if node.depth >= max_depth or node.state.game_over():
            return
        
        # Par katru iespējamo gājienu izveido pēcteča mezglu
        for position in range (1, len(node.state.available_moves()) + 1):
            # Noklonē stāvokli, lai neietekmētu oriģinālo
            node_state = node.state.clone_state()
            valid_move = node_state.make_move(position, node_state.p1_turn)
            if valid_move:
                child_node = GameStateNode(node_state, position, node.depth + 1)
                node.add_child(child_node)
                # Izsauc sevi, veidojot zarus zaru galos
                self.build_tree(child_node, max_depth)

    def print_tree(self, node=None, indent=""):
        if node is None: 
            node = self.root
        # D - dziļums, G - gājiens (pēc kārtas no iespējamajiem), L - Laukums, P - punkti
        print(f"{indent}D: {node.depth} - G: {node.move} - L: {node.state.board} P: {node.state.points}")
        for child in node.children:
            self.print_tree(child, indent + "    ")    


def export_tree_to_file(self, filename="game_tree.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        self._export_node(self.root, f)

def _export_node(self, node, file, indent=""):
    move_info = f"Gājiens: {node.move}" if node.move is not None else "Sākuma stāvoklis"
    score, diff, good = node.state.evaluate()
    file.write(f"{indent}Dziļums: {node.depth} | {move_info} | Valde: {node.state.board} | Punkti: {node.state.points} | Vērtējums: {score:.2f}\n")
    for child in node.children:
        self._export_node(child, file, indent + "    ")

GameStateTree.export_tree_to_file = export_tree_to_file
GameStateTree._export_node = _export_node