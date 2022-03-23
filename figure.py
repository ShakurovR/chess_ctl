from moves import move


class figure():
    """ Base class for chess piece """

    def __init__(self, cost, color, pos, pref):
        self._cost = cost
        self._color = color
        self._pos = pos
        if(color == "white"):
            pref = "\u001b[31m\u001b[1m\u001b[4m"+pref+"\u001b[22m\u001b[24m"
        self.prefix = ' '+pref+' '

    def move(self, move_to):
        pass


class Pawn():
    _been_moved = 0
    _cost = 1

    def __init__(self, color, pos, pref):
        self._color = color
        self._pos = pos
        pawn_dir = "d"
        if(color == "white"):
            pawn_dir = "u"
            pref = "\u001b[31m\u001b[1m\u001b[4m"+pref+"\u001b[22m\u001b[24m"
        self.prefix = ' '+pref+' '

        self.moves = [move(pawn_dir, False, False),
                      move(pawn_dir + "r", True, False, True),
                      move(pawn_dir + "l", True, False, True),
                      move(pawn_dir*2, False, False)]


class Rook(figure):
    _been_moved = 0
    moves = [move("u"),
             move("d"),
             move("r"),
             move("l")]
    _cost = 5

    def __init__(self, color, pos, pref):
        self._color = color
        self._pos = pos
        if(color == "white"):
            pref = "\u001b[31m\u001b[1m\u001b[4m"+pref+"\u001b[22m\u001b[24m"
        self.prefix = ' '+pref+' '


class Knight():
    _been_moved = 0
    moves = [move("uur", True, False),
             move("uul", True, False),
             move("ddl", True, False),
             move("ddr", True, False),
             move("urr", True, False),
             move("ull", True, False),
             move("dll", True, False),
             move("drr", True, False)]
    _cost = 3

    def __init__(self, color, pos, pref):
        self._color = color
        self._pos = pos
        if(color == "white"):
            pref = "\u001b[31m\u001b[1m\u001b[4m"+pref+"\u001b[22m\u001b[24m"
        self.prefix = ' '+pref+' '


class Bishop(figure):
    _been_moved = 0
    moves = [move("ur"),
             move("dr"),
             move("ul"),
             move("dl")]

    _cost = 3

    def __init__(self, color, pos, pref):
        self._color = color
        self._pos = pos
        if(color == "white"):
            pref = "\u001b[31m\u001b[1m\u001b[4m"+pref+"\u001b[22m\u001b[24m"
        self.prefix = ' '+pref+' '


class Queen(figure):
    _been_moved = 0
    moves = [move("u"),
             move("d"),
             move("r"),
             move("l"),
             move("ur"),
             move("dr"),
             move("ul"),
             move("dl")]

    _cost = 10

    def __init__(self, color, pos, pref):
        self._color = color
        self._pos = pos
        if(color == "white"):
            pref = "\u001b[31m\u001b[1m\u001b[4m"+pref+"\u001b[22m\u001b[24m"
        self.prefix = ' '+pref+' '


class King(figure):
    _been_moved = 0
    moves = [move("u", 1, 0),
             move("d", 1, 0),
             move("r", 1, 0),
             move("l", 1, 0),
             move("ur", 1, 0),
             move("dr", 1, 0),
             move("ul", 1, 0),
             move("dl", 1, 0)]

    _cost = None

    def __init__(self, color, pos, pref):
        self._color = color
        self._pos = pos
        if(color == "white"):
            pref = "\u001b[31m\u001b[1m\u001b[4m"+pref+"\u001b[22m\u001b[24m"
        self.prefix = ' '+pref+' '
