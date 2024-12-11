from board import Board
from piece import Piece

from typing import List, Dict, NewType, Generator
from board import Board, BoardRenderer

#Board = NewType('Piece', object)

# Representa el juego en sí
class TestingMoves:
    def __init__(self, list_move: List[Dict[int, List[int]]]):
        self.board = Board()
        self.current_player = 0  # Comienza el jugador 1
        self.list_move = list_move  
        self.current_moves = None

    @property
    def play_turn(self):
    
        current_pieces = self.board.pieces_p1 if self.current_player == 0 else self.board.pieces_p2
        print(f"\n\tTurno del Jugador {self.current_player + 1}\n")
        # Solicitar al jugador que seleccione una pieza (en este caso, elegimos automáticamente para simplificar)
        selected_piece = None
        while True:
            piece_idx = self.current_moves[self.current_player].pop(0) - 1
            if 0 <= piece_idx < len(current_pieces):
                print(f"\tPieza seleccionada {piece_idx +1}\n")
                selected_piece = current_pieces[piece_idx]
            if selected_piece.move(self.board) and (selected_piece is not None): break
        self.board.update_grid()

    @property
    def start(self):
        while True:  
            BoardRenderer.display(self.board)

            # Check for empty moves
            if len(self.current_moves[0]) == 0 and len(self.current_moves[1]) == 0: 
                print("\tNo hay mas movimientos en este juego\n")
                break  

            self.play_turn

            if self.board.is_win(self.current_player):
                print(f"Jugador {self.current_player + 1} ha ganado!")
                break  # This also exits the inner loop, not the outer loop

            # Cambiar de jugador
            self.current_player = 1 - self.current_player

    @property
    def preparing_game(self):
        for idx, _ in enumerate(self.load_moves()):
            print(f"\tJuego numero {idx}\n")
            self.start
        

    def load_moves(self) -> Generator[Dict[int, List[int]], None, None]:
        '''
        Load all moves for a game lazily (one move at a time).
        '''
        while self.list_move:
            self.current_moves = self.list_move.pop(0)
            yield 



# Predefined list of moves
list_move: List[Dict[int, List[int]]] = [
    {0: [1, 1], 1: [3, 3]},  # Moves for Player 1 and Player 2 for one round
    {0: [1, 1, 1], 1: [1, 1, 1]}  # Another round of moves
]

if __name__ == "__main__":
    game = TestingMoves(list_move)
    game.preparing_game
