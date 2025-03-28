import random

class GameState:
    def __init__(self, ai_turn, game_length=0, debug=False):
        if debug:
            # STATISKA ciparu virkne debugošanai
            self.board = [0, 1, 0, 1, 0, 0]
        else:
            # Uzģenērē ciparu virkni spēles sākumam
            self.board = [ random.randint(0, 1) for i in range(game_length) ]  

        # Abu spēlētāju punkti glabājas vārdnīcā, manuprāt, vieglākai piekļuvei
        self.points = {1: 0, 2: 0} 
        self.ai_turn = ai_turn # BOOL - T, ja sāk dators, F, ja sāk cilvēks

    def print_state(self):
        print(self.board)
        print(self.points)

    # Metode sevis klonēšanai, nepieciešama kokam
    def clone_state(self):
        new_state = GameState(self.ai_turn) # Inicializē jaunu, tukšu spēles stāvokli 
        # Iekopē visus atribūtus
        new_state.board = self.board.copy()
        new_state.points = self.points.copy()
        new_state.ai_turn = self.ai_turn
        return new_state

    def available_moves(self):
        board = self.board
        return [(board[i], board[i+1]) for i in range(len(board)-1)]
    
    def evaluate(self):
        # Punktu starpība starp spēlētājiem (Galvenais faktors)
        point_diff = self.points[1] - self.points[2]

        moves = self.available_moves()
        # Visi labie gājieni (palielina punktu starpību pret pretinieku)
        good_moves = [m for m in moves if m in [(0, 0), (1, 0)]]

        # Koeficients, ja pēc pretinieka gājiena, spēlētājam varētu palikt labs gājiens
        good_moves_count = len(good_moves)
        good_moves_coef = good_moves_count if good_moves_count % 2 == 0 else 0

        # (0, 0) labāks, jo tas atdod 1 (objektīvi sliktāks cipars)
        move_score = sum(1 for m in good_moves if m == (0, 0)) + good_moves_coef

        # Ja mans gājiens tad kruta, ja pretineka gājiens tad nav kruta
        turn_coef = 1 if self.ai_turn else -1
        score = point_diff + 0.4 * move_score * turn_coef

        return score
    
    # Pie lielāka koka mazāks dziļums
    def dynamic_depth(self):
        moves_left = len(self.available_moves())
        if moves_left > 10:
            return 4
        else:
            return 6    
    
    def make_move(self, position, ai_turn):
        if self.game_over():
            return False
        
        available_moves = self.available_moves()
        if position > len(available_moves):
            return False

        # nosaka pašreizējo spēlētāju un pretinieku
        player = 1 if ai_turn else 2
        opponent = 2 if ai_turn else 1

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
        self.ai_turn = not self.ai_turn
        return True
        
    def game_over(self):
        return len(self.available_moves()) == 0
    
    def winner(self):
        if not self.game_over():
            return None

        if self.points[1] > self.points[2]:
            return 1 # 1. spēlētājs (dators)
        elif self.points[2] > self.points[1]:
            return 2 # 2. spēlētājs
        else:
            return 0 # neizšķirts
        
if __name__ == "__main__":
    print("Palaid main.py nevis šo, mīļumiņ!")
