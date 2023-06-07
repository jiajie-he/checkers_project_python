class AI:
    """
    Create an AI player
    """

    def __init__(self, team):
        """Initialize the AI player"""
        self.team = team
        self.take_turn = False
        self.no_jumps = True
        self.no_moves = None
        self.checker_position = []
        self.valid_move = []
        self.valid_jump = []
        self.delay = 30

    def rest_delay(self):
        """Reset delay timer"""
        self.delay = 50
