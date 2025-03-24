def export_tree_to_dot(game_tree, filename="tree.dot"):
    """
    Export the game state tree to a DOT file for visualization with Graphviz.

    Each node will be labeled with its depth, board state, points, and applied move.
    """
    dot_lines = ["digraph GameStateTree {"]
    counter = [0]  # A mutable counter to assign unique IDs

    def traverse(node, node_id):
        # Create a label with line breaks (escaped as \\n)
          label = f"Depth: {node.depth}\\nBoard: {node.state.board}\\nPoints: {node.state.points}\\nMove: {node.move}\\nScore: {node.score[0]:.2f}\\nPoint diff: {node.score[1]:.2f}\\nNext Moves: {node.score[2]:.2f}"
          dot_lines.append(f'    node{node_id} [label="{label}"];')
          for child in node.children:
               counter[0] += 1
               child_id = counter[0]
               dot_lines.append(f"    node{node_id} -> node{child_id};")
               traverse(child, child_id)

    # Start traversal at the root node (with id 0)
    traverse(game_tree.root, 0)
    dot_lines.append("}")

    # Write all DOT lines to file.
    with open(filename, "w") as f:
        f.write("\n".join(dot_lines))
    print(f"DOT file saved to {filename}")

# Example usage (assuming you have already built your tree):
if __name__ == "__main__":
    from gamestate import GameState
    from tree import GameStateTree

    # Create a sample game and tree (choose a small board and depth for clarity)
    game = GameState(p1_turn=True, game_length=5, debug=True)
    tree = GameStateTree()
    tree.create_tree(game, max_depth=10)

    # Export the tree to a DOT file.
    export_tree_to_dot(tree)