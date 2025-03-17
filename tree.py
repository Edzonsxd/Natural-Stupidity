from gamestate import GameState

class GameStateNode:
    def __init__(self, state, move=None, depth=0):
        self.state = state  # Spēles stāvoklis
        self.move = move    # Gājiens no iepriešējā stāvokļa uz šo stāvokli
        self.children = []  # Pēcteču saraksts
        self.depth = depth  # Virsotnes dziļums kokā

    def add_child(self, node):
        self.children.append(node)

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

if __name__ == "__main__":
    print("Palaid main.py nevis šo, mīļumiņ!")
