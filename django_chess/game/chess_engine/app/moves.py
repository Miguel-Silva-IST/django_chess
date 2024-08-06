#movements checks
#1 each piece has x possible moves
#2 moves restricted by (a : obstacle pieces) & (b : board_boundaries)
#3 can eat piece if diff color
#4 check if after move king is on check - if yes then impossible move

#EXCEPTION - MOVEMENTS ARE OPOSIT IF WHITE/BLACK PIECES FOR SOME PIECES
#pieces that change move dir - pawn
from .colors import WHITE, BLACK
from .utils import *
from .directions import FRONT, BACK, LEFT, RIGHT
from .player import *
from .board import *
from .pieces import *
from .move_registry import *
import copy



class PossibleMoves:
    """
    Checks all possible moves - for now excludes king check - see if implement here or separatly
    """
    
    def __init__(self, board, piece):
        self._board = board
        self._piece = piece
        self.possible_moves = []
   
    
    def check_possible_moves(self):
        """Iterates in all directions to get possible moves"""
        
        for dir in self._piece.dir_moves:
            pos_f = copy.deepcopy(self._piece.pos)
            while True:
                pos_f[0] += dir[0]
                pos_f[1] += dir[1]                 
                
                #check board boundaries - if doesnt satisfy then jumps
                if not check_board_in_boundaries(self._board,pos_f):
                    break
                
                target_piece = self._board.get_board_piece(pos_f)                 
                
                #check if empty square
                if not target_piece:
                    self.possible_moves.append(copy.deepcopy(pos_f))
                
                #in case not empty verifies if can eat - if yes then adds that pos, else breaks
                else:
                    
                    #if blocking piece has diff color then can eat and add to pos
                    if self._piece.color != target_piece.color:
                        self.possible_moves.append(copy.deepcopy(pos_f))
                    
                    #in either case, since blocking piece is there, it stops moving
                    break      
                
                #if piece can only move one square breaks 
                if not self._piece.n_moves:
                    break
                
                        


class PawnMoves(PossibleMoves):    
    
    def check_diagonal_eat(self):
        """
        Checks for diagonal moves for eating enimy pieces and returns new possible moves
        """
        diag_moves = []
        
        #movements differ depending on side of board
        if self._piece.color == WHITE:
            diag_pos_r, diag_pos_l = [self._piece.pos[0]+FRONT, self._piece.pos[1]+RIGHT], [self._piece.pos[0]+FRONT, self._piece.pos[1]+ LEFT]
        elif self._piece.color == BLACK:
            diag_pos_r, diag_pos_l = [self._piece.pos[0]+ BACK, self._piece.pos[1]+RIGHT], [self._piece.pos[0]+BACK, self._piece.pos[1]+ LEFT]
        
        #first checks if diag pos is in boundaries, then checks if there is piece to eat
        if check_board_in_boundaries(self._board,diag_pos_r):
            target_piece_diag_r = self._board.get_board_piece(diag_pos_r)
            if target_piece_diag_r:
                if target_piece_diag_r.color!= self._piece.color:
                    diag_moves.append(diag_pos_r)
        
        #first checks if diag pos is in boundaries, then checks if there is piece to eat
        if check_board_in_boundaries(self._board, diag_pos_l):
            target_piece_diag_l = self._board.get_board_piece(diag_pos_l)
            if target_piece_diag_l:
                if target_piece_diag_l.color!= self._piece.color:
                    diag_moves.append(diag_pos_l)
        
        return diag_moves
                
    
    
    def check_first_move(self):
        if self._piece.color == WHITE:
            begin_row = 1
            move = FRONT
        if self._piece.color == BLACK:
            begin_row = 6
            move = BACK
        
        
        if self._piece.pos[0] == begin_row:
            second_row_pos = [self._piece.pos[0]+move, self._piece.pos[1]]
            third_row_pos = [self._piece.pos[0]+2*move, self._piece.pos[1]]
            #if no piece in second row and third row then moves
            if (not self._board.get_board_piece(second_row_pos)) and (not self._board.get_board_piece(third_row_pos)):
                return [third_row_pos]
            else:
                return []

        else:
            return []
    
    
    def check_en_passant(self):
        pass                    
        
    
    
    def check_possible_moves(self):
        
        super().check_possible_moves()
        
        #Added here because pawn is the only piece that cannot eat in its moving direction
        # so if it has a move to a square with another piece, this move is deleted 
        if self.possible_moves:
            pos_f = self.possible_moves[0]
            if self._board.get_board_piece(pos_f):
                self.possible_moves = []
                                
        diag_moves = self.check_diagonal_eat()
        first_pawn_moves = self.check_first_move()
        
        if diag_moves:
            self.possible_moves.extend(diag_moves)
        if first_pawn_moves:
            self.possible_moves.extend(first_pawn_moves)
                



class RookMoves(PossibleMoves):
    pass


class KnightMoves(PossibleMoves):
    pass


class BishopMoves(PossibleMoves):
    pass


class QueenMoves(PossibleMoves):
    pass


class KingMoves(PossibleMoves):
    
    def check_rock_n_roll(self):
        pass
    
    def check_possible_moves(self):
        
        super().check_possible_moves()
        
        #add here extra possible move for rock n roll



#register moves in class, to avoid circular import
MovesRegistry.register("Pawn", PawnMoves)
MovesRegistry.register("Rook", RookMoves)
MovesRegistry.register("Knight", KnightMoves)
MovesRegistry.register("Bishop", BishopMoves)
MovesRegistry.register("Queen", QueenMoves)
MovesRegistry.register("King", KingMoves)






#notes - 
# sequence: 
# 1- after player 1 moving one piece, we need to check if king from player 1 is checked.
# 2- before starting one move, player needs to see if self king is checked. If so, only moves player can do is to defend king 
# 3- analyze point2 : ... 


#check logic:  
#1 - based on king pos, see in which directions king can move from -> those are the directions that it can be checked, otherwhise is covered
#2 - check possible horses - only pieces that can jump - check if there are enemy knights surrounding king   

#Check logic when moving piece
#1 - if player 1 moves one piece and players 1 king gets checked, then all moves in that direction cant be taken
#2 - 



#two types of checks - > 1 move piece results in self check, 2 - play start king is checked 


#Only makes scense to check if king was checked after a move if that move was in line with king ...

class VerifyCheck:
    """
    Calculates if king is in check, based on oponent move or self move
    (move of a knight uncovering the king for example)
    """
      
    def __init__(self, board, player):
        #Piece and new_pos are used for verify if new move results in self check 
        self._board = board
        self._player = player   
    
    def verify_check(self):
        """Verifies if target king is in check"""
        
        king = find_king(self._player, self._board)
        
        #doesnt work if a piece of enemy gets moved between my king and self played piece...
        #if not verify_piece_in_line_king(self._piece, king):
        #    return 0
        
        #1 See in which directions king can be atacked first
        #goes in every dir and checks if there are enemy rooks/queens in lines, enemy queens/bishops in diagonals - dont forget to verify pawns
        
        #D - diagonal atack , H - horizontal/vertical atack
        for dir, dir_dsc in zip(King().dir_moves, ['D','D','D','D', 'H', 'H','H','H']):
            square = copy.deepcopy(king).pos 
            while True:
                
                square[0] += dir[0]
                square[1] += dir[1]                 
                
                #check board boundaries - if doesnt satisfy then jumps
                if not check_board_in_boundaries(self._board,square):
                    break
                
                blocking_piece = self._board.get_board_piece(square)
                
                if blocking_piece:
                    if blocking_piece.color ==  self._player.color:
                        break
                    
                    else:
                        #blocking piece is enemy piece
                        
                        #if is diagonal direction
                        if dir_dsc == 'D':
                            
                            if (blocking_piece.__class__.__name__ == 'Bishop') or (blocking_piece.__class__.__name__ == 'Queen'):
                                print('Check due to bishop/queen')
                                return 1
                            elif blocking_piece.__class__.__name__ == 'Pawn':
                                #moving in same direction and oposite way to see if pawn is close to king to atack (takes into account the direction pawn eats
                                #depending on color)
                                if (blocking_piece.pos[0] + blocking_piece.dir_moves[0][0] == king.pos[0]) and (blocking_piece.pos[1] - dir[1] == king.pos[1]):
                                    print('Check due to pawn')
                                    return 1
                                else:
                                    #Blocking pawn at distance
                                    break   
                            else:
                                #ex.:for the case where a blocking piece is an enemy horse in diagonal
                                #stops the iteration in this dir since king is covered
                                break
                        #if is horizontal direction                    
                        elif dir_dsc == 'H':
                            if (blocking_piece.__class__.__name__ == 'Rook') or (blocking_piece.__class__.__name__ == 'Queen'):
                                print('Check due to rook/queen')
                                return 1
                            else:
                                break
        
        
        
        
        #2 After check horses
        for dir in Knight().dir_moves:
            square = copy.deepcopy(king).pos
            square[0] += dir[0]
            square[1] += dir[1]

            #check board boundaries - if doesnt satisfy then jumps
            if not check_board_in_boundaries(self._board,square):
                continue

            blocking_piece = self._board.get_board_piece(square)
            #oponent knight atacking king
            if blocking_piece.__class__.__name__ == 'Knight' and blocking_piece.color!=self._player.color:
                print('Check due to knight')
                return 1
        

        #if passes all scenarios then is not in check
        return 0



if __name__ == '__main__':
    pawn = Pawn([1,0],1)
    board1 = Board()
    board2 = Board([[-2, -3, -4, -5, -6, -4, -3, -2], [-1, -1, -1, -1, -1, -1, -1, -1], [None, 1, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [1, None, 1, 1, 1, 1, 1, 1], [2, 3, 4, 5, 6, 4, 3, 2]])
    board3 = Board([[None, -3, -4, -5, -6, -4, -3, -2], [-1, -1, -1, -1, -1, -1, -1, -1], [-2, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [1, None, 1, 1, 1, 1, 1, 1], [2, 3, 4, 5, 6, 4, 3, 2]])
    board4 = Board([[None, -3, -4, -5, -6, -4, -3, -2], [None, None, None, None, None, None, None, None], [-2, None, None, None, None, None, None, None], [None, None, None, None, 2, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [1, None, 1, 1, 1, 1, 1, 1], [2, 3, 4, 5, 6, 4, 3, 2]])
    board5 = Board([[None, -3, -4, -5, -6, -4, -3, -2], [None, None, None, None, None, None, None, None], [-2, None, None, None, None, None, 4, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [1, None, 1, 1, 1, 1, 1, 1], [2, 3, 4, 5, 6, 4, 3, 2]])
    board6 = Board([[None, -3, -4, -5, -6, -4, -3, -2], [None, None, None, None, None, -1, None, None], [-2, None, None, None, None, None, 4, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [1, None, 1, 1, 1, 1, 1, 1], [2, 3, 4, 5, 6, 4, 3, 2]])    

    
    rook1 = Rook([2,0],1)
    rook2 = Rook([0,0],1)
    
      
    rook_moves1 = RookMoves(board3, rook1)
    print('Testing white rook moves at [2,0]')
    print('Board 3->',board3)
    rook_moves1.check_possible_moves()
    print(rook_moves1.possible_moves)
    
    
    rook_moves2 = RookMoves(board3, rook2)
    rook_moves2.check_possible_moves()
    print(rook_moves2.possible_moves)


    print('Board 4->',board4)
    player = Player(WHITE)
    verify_check = VerifyCheck(board4, player)
    result = verify_check.verify_check()
    print(result)



    print('Board 5->',board5)
    player = Player(WHITE)
    verify_check = VerifyCheck(board5, player)
    result = verify_check.verify_check()
    print(result)


    print('Board 6->',board6)
    player = Player(WHITE)
    verify_check = VerifyCheck(board6, player)
    result = verify_check.verify_check()
    print(result)