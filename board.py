class Board:
    """Create the checker game board"""
    def __init__(self, SQUARE_SIZE, BOARD_SIZE):
        """Initialize the game board"""
        self.SQUARE_SIZE = SQUARE_SIZE
        self.BOARD_SIZE = BOARD_SIZE
        self.position = {}
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                self.position[(i, j)] = False

    def display(self):
        """Display the checker board"""
        MILKTEA = (255, 222, 173)
        COFFEE = (139, 69, 19)
        MOD = 2
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                if (row + column) % MOD == 0:
                    fill(*MILKTEA)
                else:
                    fill(*COFFEE)
                noStroke()
                rect(row * self.SQUARE_SIZE, column * self.SQUARE_SIZE,
                     self.SQUARE_SIZE, self.SQUARE_SIZE)
