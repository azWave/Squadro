from classes.piece import Piece
from typing import List


class Board:
    
    BOARD_SIZE = 7
    WINNING_PIECES = 4
    STEPS_P1 = [3, 1, 2, 1, 3]
    STEPS_P2 = [1, 3, 2, 3, 1]

    def __init__(self):
        """
        Initializes the game board and sets up the pieces for both players.

        Attributes:
            out_pieces_p1 (int): Counter for Player 1's pieces that have been removed from the board.
            out_pieces_p2 (int): Counter for Player 2's pieces that have been removed from the board.
            grid (List[List[Optional[Piece]]]): A 7x7 game board initialized with None, representing empty spaces.
            pieces_p1 (List[Piece]): A list of Player 1's pieces, each placed in its starting position with corresponding movement steps.
            pieces_p2 (List[Piece]): A list of Player 2's pieces, each placed in its starting position with corresponding movement steps.
            check_point_forward (Set[Tuple[int, int]]): Set of board positions representing checkpoints for forward movement.
            check_point_backward (Set[Tuple[int, int]]): Set of board positions representing checkpoints for backward movement.

        The method sets up an empty 7x7 board, initializes the pieces for both players, and defines key checkpoints for forward and backward movement. 
        It then calls `update_grid` to place the pieces on the board.
        """
        self.out_pieces_p1 = 0
        self.out_pieces_p2 = 0
        self.grid = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.pieces_p1 = [Piece(0, (i + 1, 0), self.STEPS_P1[i], self.STEPS_P2[i]) for i in range(5)]
        self.pieces_p2 = [Piece(1, (0, i + 1), self.STEPS_P2[i], self.STEPS_P1[i]) for i in range(5)]
        self.check_point_forward = {(i, 0) for i in range(1, 7)} | {(0, j) for j in range(1, 7)}
        self.check_point_backward = {(i, 6) for i in range(1, 7)} | {(6, j) for j in range(1, 7)}
        self.update_grid()  
        
    @property
    def is_win(self) -> bool:
        return self.out_pieces_p1 == 4 or self.out_pieces_p2 == 4

    
    def update_grid(self) -> None:
        """
        Resets and updates the grid with the current positions of all pieces.
        """
        self.grid = [[None] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        
        self.place_pieces_on_grid(self.pieces_p1)
        self.place_pieces_on_grid(self.pieces_p2)

    def place_pieces_on_grid(self, pieces: List[Piece]) -> None:
        """
        Places the given pieces on the grid based on their positions.

        Args:
            pieces (List[Piece]): A list of pieces to place on the grid.
        """
        for piece in pieces:
            row, col = piece.position
            self.grid[row][col] = piece

    def to_json(self):
        return {
            "p1": [piece.position for piece in self.pieces_p1],
            "p2": [piece.position for piece in self.pieces_p2],
            "out_p1": self.out_pieces_p1,
            "out_p2": self.out_pieces_p2
        }
    
    def __str__(self):
        # return self.__name__
        steps_p1 = [3, 1, 2, 1, 3]  
        steps_p2 = [1, 3, 2, 3, 1]  
        string = ""

        string += "\t" + "   ".join(map(str, steps_p2)) + "\n\r"

        string += "x | " + " | ".join([self.get_colored_piece(piece) for piece in self.grid[0]]) + " | x" + "\n\r"
        string += "-" * 29 + "\n\r"

        for i in range(1, 6):
            row = f"{steps_p1[i - 1]} | "  # Parte lateral izquierdo - Movimientos Forward jugador uno
            row += " | ".join([self.get_colored_piece(piece) for piece in self.grid[i]])
            row += f" | {steps_p2[i - 1]}"  # Parte lateral derecho - Movimientos Backward jugador uno
            string += row + "\n\r"
            string += "-" * 29 + "\n\r"

        string += "x | " + " | ".join([self.get_colored_piece(piece) for piece in self.grid[6]]) + " | x" + "\n\r"
        string += "\t" + "   ".join(map(str, steps_p1)) + "\n\r"
        return string

    def get_colored_piece(self,piece):

        if piece is None:
            return '.'

        colors = {1: '\033[33m', 0: '\033[31m'}
        directions = {
            (1, True): '↑', (1, False): '↓',
            (0, True): '←', (0, False): '→'
        }
        
        return f"{colors[piece.player]}{directions[(piece.player, piece.direction)]}\033[0m"
    
if __name__ == "__main__":
    b = Board()
    print(b)
