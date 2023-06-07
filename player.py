class Player:
    """
    Create the black team player
    """

    def __init__(self, team):
        """Initialize the player"""
        self.team = team
        self.take_turn = True
        self.no_jumps = True
        self.no_moves = None
        self.checker_position = []
        self.valid_move = []
        self.valid_jump = []
