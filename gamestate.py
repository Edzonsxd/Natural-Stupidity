import random

class GameState:
    def __init__(self, game_length, p1_turn, debug=False):
        if debug:
            # STATISKA ciparu virkne debugošanai
            self.board = [0, 1, 0, 1, 0, 1, 1, 0, 0]
        else:
            # Uzģenērē ciparu virkni spēles sākumam
            self.board = [ random.randint(0, 1) for i in range(game_length) ]  

        # Abu spēlētāju punkti glabājas vārdnīcā, manuprāt, vieglākai piekļuvei
        self.points =  {1: 0, 2: 0} 
        self.p1_turn = p1_turn # BOOL - T, ja p1, F, ja p2

    def print_state(self):
        print(self.board)
        print(self.points)

    def available_moves(self):
        board = self.board
        return [[board[i], board[i+1]] for i in range(len(board)-1)]
    
    def make_move(self, position, p1_turn):
        if self.game_over():
            return False
        
        available_moves = self.available_moves()
        if position > len(available_moves):
            return False

        # nosaka pašreizējo spēlētāju un pretinieku
        player = 1 if p1_turn else 2
        opponent = 2 if p1_turn else 1

        pair = available_moves[position-1]
        replacement = None

        if pair[0] == pair[1]: # situācija, kad cipari ir vienādi
            if pair[0] == 0:            
                self.points[player] += 1     # [0, 0] -> 1, + punkts sev
                replacement = 1
            else:                       
                self.points[player] -= 1     # [1, 1] -> 0, - punkts sev
                replacement = 0
        else: # kad cipari ir atšķirīgi
            if pair[0] == 0:
                self.points[opponent] += 1     # [0, 1] -> 0, + punkts pretiniekam
                replacement = 0
            else:
                self.points[opponent] -= 1     # [1, 0] -> 1, - punkts pretiniekam
                replacement = 1

        # Izgriež ciparu pāri no virknes un aizstāj to
        self.board = self.board[:position-1] + [replacement] + self.board[position+1:]
        self.p1_turn = not self.p1_turn
        return True
        
    def game_over(self):
        return len(self.available_moves()) == 0
    
    def winner(self):
        if not self.game_over():
            return None

        if self.points[1] > self.points[2]:
            return 1 # 1. spēlētājs 
        elif self.points[2] > self.points[1]:
            return 2 # 2. spēlētājs
        else:
            return 0 # neizšķirts
        
if __name__ == "__main__":
    print("Palaid main.py nevis šo, mīļumiņ!")

        