from typing import Tuple, NewType

Board = NewType('Board', object)

class Piece:
    def __init__(self, player: int, position: Tuple[int, int], forward_steps: int, backward_steps: int):

        self.player = player  # 0 o 1 para indicar el jugador
        self.position = position  # Posición actual de la pieza en el tablero (fila, columna)
        self.forward_steps = forward_steps  # Número de casillas que avanza en la ida
        self.backward_steps = backward_steps  # Número de casillas que avanza en la vuelta

        self.direction = False  # Indica si la direccion de la pieza 
        self.movement_info = set() # Información de los movimientos realizados
        self.out_piece = 0 # Si llega a 3 es porque esta afuera
        self.killed = False

    def move(self, board: Board):
        if self.is_out():
            if not self.direction:
                self._move_forward(board)
            else:
                self._move_backward(board)

            self.restore_piece(board)
            return True
        return False

    def _move_forward(self, board: Board):
        for _ in range(self.forward_steps):
            self._move(board)
            self.check_turn(board)
            if self.check_kill(): break
            if self.position in board.check_point_backward: break

    def _move_backward(self, board: Board):
        for _ in range(self.backward_steps):
            self._move(board)
            self.check_turn(board)
            if self.check_kill(): break
            if self.position in board.check_point_forward: break

    def _move(self, board: Board):
        #self.movement_info.add(self.position)
        advance_or_regress = 1 if not self.direction else -1

        if self.player == 0:  # Horizontal movement
            self._move_piece(board, (0, advance_or_regress))
        elif self.player == 1:  # Vertical movement
            self._move_piece(board, (advance_or_regress, 0))

    def _move_piece(self, board: Board, delta: Tuple[int, int]):
        row, col = self.position
        for i in range(1, 10):  # Limit movement to 10 squares
            self.movement_info.add((row, col))
            row, col = row + delta[0], col + delta[1]
            if i > 1:
                self.killed = True
            if board.grid[row][col] is None:
                self.position = (row, col)
                break

    def check_turn(self, board):
        # Verificar si tiene que cambiar de direccion.
        if not self.direction:
            if self.position in board.check_point_backward: # Verificar si llego a un checkpoint
                self.direction_change(board)  
        else:
            if self.position in board.check_point_forward:
                self.direction_change(board)

    def check_kill(self):
        if self.killed:  self.killed = False; return True
        else: False

    def direction_change(self, board):
        # Gira la pieza cuando llega al final del carril
        self.out_piece += 1
        self.direction = True

        if self.out_piece == 2:
            if self.player == 0:
                board.out_pieces_p1 +=1
            elif self.player == 1:
                 board.out_pieces_p2 +=1

    def restore_piece(self, board: Board):
        #row, col = self.position
        if self.player == 0:
            for piece in board.pieces_p2:
                row, col = piece.position
                check_point = 0 if not piece.direction else 6
                if piece.position in self.movement_info:
                    piece.position = (check_point,col)
                    
        if self.player == 1:
            for piece in board.pieces_p1:
                row, col = piece.position
                check_point = 0 if not piece.direction else 6
                if piece.position in self.movement_info:
                    piece.position = (row,check_point)

        self.movement_info = set()

    def is_out(self) -> bool:
        """Comprueba si la pieza está fuera del tablero."""
        if self.out_piece >= 2:
            self.is_active = False  # Marca la pieza como inactiva si está fuera
            print(f"Pieza del Jugador {self.player + 1} ha salido del tablero.")
            return False
        return True

    def __str__(self):
        return f"Piece({self.player}, {self.position}, {self.forward_steps}, {self.backward_steps}, {self.direction})"
    
    def actionToOut(self):
        pos = self.position[1+self.player % 2]

        if self.direction:
            return (pos)//self.backward_steps
        else:
            return (6-pos)//self.forward_steps + 6//self.backward_steps
