from field import field

class Chess(field):
    def __init__(self):
        self.move = 1
        self.turn = "white"
        super().__init__()
        self._move_history = [];
        self._color_turn = "white"
        self._in_check = False
        self._GAME_IN_PROCESS = True

    def _make_move(self, from_sq, to_sq):
        if(to_sq in self._possible_moves):
            self._last_taken = self[to_sq]
            self[to_sq] = self[from_sq]
            self[from_sq] = None
        else:
            raise ValueError("Impossible move")
    
    def _update_possible_moves(self, from_sq):

        
        self._possible_moves = []
        for piece_move in self[from_sq].moves:
            self._possible_moves+=piece_move.get_possible(from_sq, self) 

        if(not self._possible_moves):
            raise   ValueError("Impossible move")
    
    def _check_for_check(self, color):
        for row in self._row_names:
            for col in self._col_names:
                if(self[col+row]):
                    if(self[col+row]._cost is None and self[col+row]._color == color):
                        king_pos = col+row
                        #print(king_pos)
                        break
        for row in self._row_names:
            for col in self._col_names:
                if(self[col+row]):
                    if(self[col+row] and self[col+row]._color != color):
                        possible_capt = []
                        for piece_move in self[col+row].moves:
                            possible_capt+=piece_move.get_possible_capture(col+row, self) 
                        #print(possible_capt)
                        if(king_pos in possible_capt):
                            return True
        return False
    
    @staticmethod
    def op_color(color):
        if(color == "white"):
            return "black"
        return "white"

    def start_game(self):
        while self._GAME_IN_PROCESS:
            try:
                self._main_loop()
                if(self._color_turn == "white"):
                    self._color_turn = "black"
                else:
                    self.move += 1
                    self._color_turn = "white"
                
            except ValueError as VE:
                print("Impossible Move")
            except KeyError as KE:
                print("Ошибка ввода")

    def _main_loop(self):
        self._render_board()
        print(f"King in check: {self._in_check}")
        print(f"Move: {self.move}. It's {self._color_turn}'s turn")
        fr = input("Which piece to move:").lower()
        if(self[fr] is None):
            raise ValueError("Impossible move")
        if(self[fr]._color != self._color_turn):
            raise ValueError("Impossible move")

        self._update_possible_moves(fr)
        self._render_board(show_possible=1)

        to = input("Where to move:").lower()
        self._make_move(fr, to)
        if(self._check_for_check(self._color_turn)):
            self[to],self[fr] = self._last_taken,self[to]
            raise ValueError("ImpossibleMove")

        if('p' in self[to].prefix and not self[to]._been_moved):
            self[to].moves = self[to].moves[:-1]
        self[to]._been_moved = 1
        self._in_check = self._check_for_check(self.op_color(self._color_turn))
        self._move_history.append((fr,to))

        
if __name__ == "__main__":
    game = Chess()
    #print(game["e2"].moves[1].get_possible("e2", game))
    #print(game["f3"].moves[0].get_possible("f3", game))
    #print(game['f3'].moves)
    game.start_game()
