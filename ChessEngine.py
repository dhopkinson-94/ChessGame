"""
This class is responsible for storing all the information about the current state of a chess game.
it will also be responsible for determining valid moves at the current state. It will also keep a move log.
"""
class GameState():
    def __init__(self):
        #board is 8*8 2D list. Each element of the list has two characters
        #The first character represents the color of the piece
        #The second character represents the type of piece,
        #represents an empty space
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.move_functions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.whiteMove = True
        self.movelog = []
        self.WhiteKingLoc = (7, 4)
        self.BlackKingLoc = (0 ,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.pieces_taken = []


    """
    Takes a move as a parameter and executes it (this will not work for castling, en-passant or pawn promotion
    """
    def make_move(self,move):
        self.board[move.start_row][move.start_col] = '--'
        if self.board[move.end_row][move.end_col] != '--':
            self.pieces_taken.append(self.board[move.end_row][move.end_col])
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.movelog.append(move) #log move so we can undo later
        self.whiteMove = not self.whiteMove
        #update the kings location
        if move.piece_moved == 'wK':
            self.WhiteKingLoc = (move.end_row,move.end_col)
        elif move.piece_moved == 'bK':
            self.BlackKingLoc = (move.end_row,move.end_col)

    """
    Undo the last move
    """
    def undo_move(self):
        if len(self.movelog) != 0: #make sure there is a move to undo
            move = self.movelog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.whiteMove = not self.whiteMove #change to other persons turn
        if  move.piece_moved == 'wK':
            self.WhiteKingLoc = (move.start_row,move.start_col)
        elif move.piece_moved == 'bK':
            self.BlackKingLoc = (move.start_row,move.start_col)

    """
    All moves considering check
    """
    def get_valid_moves(self):
        moves =  self.get_all_possible_moves()
        pinsandcheck = self.checkForPinsandCheck()
        incheck = pinsandcheck[0]
        pins = pinsandcheck[1]
        if len(pins) > 0:
           print(pins)
           for p in pins:
                pinnedpiece = (p[0], p[1])
                for i in range(len(moves) - 1, -1, -1):
                    m = moves[i]
                    if m.start == pinnedpiece:
                        self.make_move(m)
                        self.whiteMove = not self.whiteMove
                        double_check = self.checkForPinsandCheck()
                        dc = double_check[0]
                        if dc:
                            moves.remove(m)
                            self.undo_move()
                            self.whiteMove = not self.whiteMove
                        else:
                            self.undo_move()
                            self.whiteMove = not self.whiteMove

        if incheck:
            for i in range(len(moves) - 1, -1, -1):
               m = moves[i]
               self.make_move(m)
               self.whiteMove = not self.whiteMove
               double_check = self.checkForPinsandCheck()
               dc = double_check[0]
               if dc:
                   moves.remove(m)
                   self.undo_move()
                   self.whiteMove = not self.whiteMove
               else:
                   self.undo_move()
                   self.whiteMove = not self.whiteMove

        return moves


    """
    All moves without considering check
    """
    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteMove) or (turn == 'b' and not self.whiteMove):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)
        return moves


    """
    Get all the pawn moves for the pawn located at row, col and add these moves to the list 'moves'
    """
    def get_pawn_moves(self, r, c, moves):
         if self.whiteMove: #white pawn moves
             if self.board[r -1][c] == '--': #one square pawn advance
                 moves.append(Move((r, c),(r - 1,c), self.board))
                 if r == 6 and self.board[r - 2][c] == '--': #this is a two square pawn advance
                     moves.append(Move((r,c),(r-2,c), self.board))
             if c - 1 >= 0: #captures to the left
                 if self.board[r-1][c - 1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c-1), self.board))
             if c + 1 <= 7: #captures to the right
                 if self.board[r-1][c + 1][0] == 'b':
                     moves.append(Move((r, c), (r - 1, c + 1), self.board))
         else:
             if self.board[r + 1][c] == '--': #one square pawn advance
                 moves.append(Move((r, c),(r + 1,c), self.board))
                 if r == 1 and self.board[r + 2][c] == '--': #this is a two square pawn advance
                     moves.append(Move((r,c),(r + 2,c), self.board))
             if c - 1 >= 0: #captures to the left
                 if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r,c), (r + 1,c-1), self.board))
             if c + 1 <= 7: #captures to the right
                 if self.board[r + 1][c + 1][0] == 'w':
                     moves.append(Move((r, c), (r + 1, c + 1), self.board))

         return moves

    """
    Get all the rook moves for the rook located at row, col and add these moves to the list 'moves'
    """
    def get_rook_moves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'b' if self.whiteMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    endpiece = self.board[endrow][endcol]
                    if endpiece == '--':
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                    elif endpiece[0] == enemy_color:
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                        break
                    else:
                        break
                else:
                    break

    """
    Get all the knight moves for the knight located at row, col and add these moves to the list 'moves'
    """
    def get_knight_moves(self, r, c, moves):
        knight_moves = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2))
        enemypiece = 'b' if self.whiteMove else 'w'
        for i in knight_moves:
            if 0 <= r + i[0] <= 7 and 0 <= c + i[1] <= 7:
                 if self.board[r + i[0]][c + i[1]] == '--':
                     moves.append(Move((r, c),(r + i[0],c + i[1]),self.board))
                 elif self.board[r + i[0]][c + i[1]][0] == enemypiece:
                    moves.append(Move((r, c),(r + i[0],c + i[1]),self.board))



    """
    Get all the bishop moves for the bishop located at row, col and add these moves to the list 'moves'
    """
    def get_bishop_moves(self, r, c, moves):
        directions = ((1, 1), (-1, 1), (1, -1), (-1, -1))
        enemypiece = 'b' if self.whiteMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow <= 7 and 0 <= endcol <= 7:
                    endpiece = self.board[endrow][endcol]
                    if endpiece == '--':
                        moves.append(Move((r, c), (endrow, endcol),self.board))
                    elif endpiece[0] == enemypiece:
                         moves.append(Move((r, c), (endrow, endcol),self.board))
                         break
                    else:
                         break
                else:
                    break

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)


    def get_king_moves(self, r, c, moves):
        king_moves = ((1,0),(1,1),(1,-1),(0,1),(0,-1),(-1,0),(-1,1),(-1,-1))
        enemypiece = 'b' if self.whiteMove else 'w'
        for i in king_moves:
            if 0 <= r + i[0] <= 7 and 0 <= c + i[0] <= 7:
                 if self.board[r + i[0]][c + i[1]] == '--':
                     moves.append(Move((r,c),(r + i[0], c + i[1]), self.board))
                 elif self.board[r + i[0]][c + i[1]][0] == enemypiece:
                     moves.append(Move((r, c), (r + i[0], c + i[1]), self.board))
                     break

    def checkForPinsandCheck(self):
        pins = [] #squares where the allied pinned piece is and direction pinned from
        checks = [] #square where enemy is applying check
        incheck = False
        if self.whiteMove:
            enemycolor = 'b'
            allycolor = 'w'
            startrow = self.WhiteKingLoc[0]
            startcol = self.WhiteKingLoc[1]
        else:
            enemycolor = 'w'
            allycolor = 'b'
            startrow = self.BlackKingLoc[0]
            startcol = self.BlackKingLoc[1]
        #check outward from king for pins and checks, keep track of pins
        directions = [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () #reset possible pins
            for i in range(1, 8):
                endRow = startrow + d[0] * i
                endCol = startcol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol <  8:
                    endpiece = self.board[endRow][endCol]
                    if endpiece[0] == allycolor:
                        if possiblePin == (): #first allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: #second allied piece so no pin or check possible in this direction
                            break
                    elif endpiece[0] == enemycolor:
                        type = endpiece[1]
                        """
                        5 possibilities in this complex conditional
                        1. orthogonally away from the king and the piece is a rook
                        2 diagonally away from the king and the piece is a bishop
                        3. 1 square away diagonally and the piece is a pawn
                        4. diagonally and orthogonally away from the king and the piece is a queen
                        5. any direction 1 square away and the piece is a king
                        """
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemycolor == 'w' and 6 <= j <= 7 ) or ( enemycolor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): #no piece blocking, so check
                                incheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: #piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else: #enemy piece not applying check
                            break
                else: #end piece is off board
                    break
        # check for knight checks
        knight_moves = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2))
        for m in knight_moves:
            endRow = startrow + m[0]
            endCol = startcol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endpiece = self.board[endRow][endCol]
                if endpiece[0] == enemycolor and endpiece[1] == 'N':
                    incheck = True
                    checks.append(endRow, endCol, m[0], m[1])
        return incheck, pins, checks



class Move():
    # maps keys to values
    # key : value
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4,
                     '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                     'e': 4, 'f': 5, 'g': 6, 'h': 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}


    def __init__(self, start, end, board):
        self.start = start
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        print(self.moveID)

    """
    Overriding the equals method
    """
    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)


    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
