from field import field
from functools import reduce
import figure as figs
from moves import Moves_history
from copy import deepcopy
from moves import ImpossibleMove, UndoMove

class Chess(field):
    def __init__(self):
        self.move = 1
        self.turn = "white"
        super().__init__()
        self._moves_history = Moves_history()
        self._color_turn = "white"
        self._in_check = False
        self._GAME_IN_PROCESS = True

    def _make_move(self, from_sq, to_sq):
        if(to_sq in self._possible_moves):
            self._moves_history.push(self[from_sq],
                                     self[to_sq],
                                     from_sq,
                                     to_sq)

            self[to_sq] = self[from_sq]
            self[from_sq] = None
            self[to_sq]._pos = to_sq
        else:
            raise ImpossibleMove("Impossible move")

        if(self._check_for_check(self._color_turn)):
            self[to_sq] = deepcopy(self._moves_history[-1]["captured_piece"])
            self[from_sq] = deepcopy(self._moves_history[-1]["piece"])
            self._moves_history.pop()

            raise ImpossibleMove("ImpossibleMove")

        if('p' in self[to_sq].prefix and not self[to_sq]._been_moved):
            self[to_sq].moves = self[to_sq].moves[:-1]

        self[to_sq]._been_moved = 1

    def _undo_move(self):
        if(self._color_turn == "white" and self.move == 1):
            return

        (fr, to), moved_piece, capt_piece = self._moves_history.pop()
        
        self[fr] = moved_piece
        self[to] = capt_piece
        
        if(self._color_turn == "white"):
            self.move-=1
        self._color_turn = self.op_color(self._color_turn)
        self._in_check = self._check_for_check(self._color_turn)

    def _get_list_of_figures(self, color=None):
        all_sq = reduce(lambda x, y: x+y,
                        [list(i.values()) for i in self._field.values()])
        all_sq = list(filter(lambda x: x is not None, all_sq))
        if(color):
            return list(filter(lambda x: x._color == color, all_sq))
        return all_sq

    def _update_possible_moves(self, from_sq):
        self._possible_moves = []
        for piece_move in self[from_sq].moves:
            self._possible_moves += piece_move.get_possible(from_sq, self)

        if(not self._possible_moves):
            raise ImpossibleMove("Impossible move")

    def _check_for_check(self, color):
        king_piece = next(filter(lambda x: isinstance(x, figs.King),
                                 self._get_list_of_figures(color)))

        for piece in self._get_list_of_figures(self.op_color(color)):
            possible_capt = []
            for piece_move in piece.moves:
                possible_capt += piece_move.get_possible_capture(
                    piece._pos, self)
            if(king_piece._pos in possible_capt):
                return True
        return False

    def _check_for_mate(self, color):
        # Not Implemented (yet)
        return 0

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

            except ImpossibleMove as VE:
                print("Impossible Move")
            except KeyError as KE:
                print("Ошибка ввода")
            except UndoMove as UM:
                print("Undoing last move")
                self._undo_move()

    def _main_loop(self):
        self._render_board()

        print(f"King in check: {self._in_check}")
        print(f"Move: {self.move}. It's {self._color_turn}'s turn")

        fr = input("Which piece to move:").lower()
        if("undo" in fr):
            raise UndoMove();
        if(self[fr] is None):
            raise ImpossibleMove("Impossible move")
        if(self[fr]._color != self._color_turn):
            raise ImpossibleMove("Impossible move")

        self._update_possible_moves(fr)
        self._render_board(show_possible=1)

        to = input("Where to move:").lower()
        self._make_move(fr, to)

        self._in_check = self._check_for_check(self.op_color(self._color_turn))

        if(self._in_check):
            if(self._check_for_mate(self.op_color(self._color_turn))):
                self._GAME_IN_PROCESS = False


if __name__ == "__main__":
    game = Chess()
    #print(game["e2"].moves[1].get_possible("e2", game))
    #print(game["f3"].moves[0].get_possible("f3", game))
    # print(game['f3'].moves)
    game.start_game()
