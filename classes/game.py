from classes.board import Board

class SquadroGame:
    def __init__(self,argv):
        self.board = Board()
        self.current_player = 0  
        self.argv = argv

    def play_turn(self,pieceIndex):

        pieceIndex = int(pieceIndex)
        current_pieces = self.board.pieces_p1 if self.current_player == 0 else self.board.pieces_p2

        selected_piece = None
        try:
            if 0 <= pieceIndex < len(current_pieces):
                selected_piece = current_pieces[pieceIndex]
            else:
                print(f"Error: need integer between 1 and {len(current_pieces)}.")
                return False

            if selected_piece is not None and selected_piece.move(self.board):
                self.board.update_grid()
                return True
                
        except ValueError:
            print("Error: Invalid input.")

        

    def change_turn(self):
        self.current_player = 1 - self.current_player

    def run(self):
        self.tutorial_general_information()
        while True:
            print(f"\n\tPlayer {self.current_player + 1} turn's\n")
            print(self.board)
            pieceIndex = int(input(f"Select a piece (1-5): ")) - 1

            while not self.play_turn(pieceIndex) : 
                pieceIndex = int(input(f"Select a piece (1-5): ")) - 1

            if self.board.is_win:
                print(self.board)
                print(f"Player {self.current_player + 1} win !")
                break
            self.change_turn()
    
    def tutorial_general_information(self):
        if self.argv.tutorial  :
            instructions = open("assets/instruction.txt","r",encoding="utf-8")
            print(instructions.read())
            input("Are you ready?")
