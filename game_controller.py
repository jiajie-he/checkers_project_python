from player import Player
from AI import AI
from checker import Checker
from board import Board


class GameController:
    """
    The Game Controller
    """

    def __init__(self, SQUARE_SIZE, BOARD_SIZE, ANSWER):
        """Initialize the game controller"""
        self.BOARD_SIZE = BOARD_SIZE
        self.SQUARE_SIZE = SQUARE_SIZE
        self.board = Board(SQUARE_SIZE, BOARD_SIZE)
        self.move_count = 0
        self.player = Player("Black")
        self.ai = AI("Red")
        self.checkers = []  # list to store checkers
        self.ai_checkers = []
        self.result = None
        self.moves = 0
        self.answer = ANSWER
        self.game_over = False

        # create red checkers from the top side
        MOD = 2
        ROW = 3
        for x in range(BOARD_SIZE):
            for y in range(ROW):
                if (x + y) % MOD != 0:
                    checker = Checker(x, y, "Red")
                    self.ai_checkers.append(checker)
                    self.ai.checker_position.append((checker.x, checker.y))

        # create black checkers from the bottom side
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE-ROW, BOARD_SIZE):
                if (x + y) % MOD != 0:
                    checker = Checker(x, y, "Black")
                    self.checkers.append(checker)
                    self.player.checker_position.append((checker.x, checker.y))

    def update(self):
        """Updates game state on every frame"""
        self.player.no_jumps = True
        self.ai.no_jumps = True
        self.board.display()
        self.update_board_position()
        # loop through checkers and call their display method
        for i, checker in enumerate(self.checkers):
            checker.display()
            self.player.checker_position[i] = (checker.x, checker.y)
            self.check_valid_jump(checker)

        for checker in self.checkers:
            if checker.can_jump:
                self.player.no_jumps = False
                self.take_turn()

        if self.player.no_jumps:
            for checker in self.checkers:
                self.check_valid_move(checker)

        for i, ai_checker in enumerate(self.ai_checkers):
            ai_checker.display()
            self.ai.checker_position[i] = (ai_checker.x, ai_checker.y)
            self.check_ai_valid_jump(ai_checker)

        for ai_checker in self.ai_checkers:
            if ai_checker.can_jump:
                self.ai.no_jumps = False
                self.take_turn()

        if self.ai.no_jumps:
            for ai_checker in self.ai_checkers:
                self.check_ai_valid_move(ai_checker)

        self.take_turn()

        if self.ai.take_turn:
            if self.ai.delay > 0:
                self.ai.delay -= 1
            if self.ai.delay == 0:
                self.activate_ai()
                self.ai.rest_delay()

        self.create_king()

        self.end_game()

    def update_board_position(self):
        """Update the checker position on the board"""
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                self.board.position[(i, j)] = False

        for checker in self.checkers:
            x, y = checker.x, checker.y
            self.board.position[(x, y)] = True

        for ai_checker in self.ai_checkers:
            x, y = ai_checker.x, ai_checker.y
            self.board.position[(x, y)] = True

    def create_king(self):
        """Make a king checker """
        for checker in self.checkers:
            if checker.y == 0 and checker.color == "Black":
                if not checker.king:
                    checker.king = True
                    print("This checker became a King")

        for ai_checker in self.ai_checkers:
            if ai_checker.y == self.BOARD_SIZE - 1 \
                    and ai_checker.color == "Red":
                if not ai_checker.king:
                    ai_checker.king = True
                    print("This checker became a King")

    def check_valid_jump(self, checker):
        """Check valid jump of checkers"""
        JUMP_STEP = 2
        MOVE_STEP = 1
        checker.can_jump = False
        checker.valid_jump = set()

        x, y = checker.x, checker.y

        if self.player.take_turn:
            if x - JUMP_STEP >= 0 and y - JUMP_STEP >= 0 \
                    and not \
                    self.board.position[(x - JUMP_STEP, y - JUMP_STEP)] \
                    and self.board.position[(x - MOVE_STEP, y - MOVE_STEP)] \
                    and (x - MOVE_STEP, y - MOVE_STEP) \
                    not in self.player.checker_position:
                checker.can_jump = True
                checker.valid_jump.add((x - JUMP_STEP, y - JUMP_STEP))

            if x + JUMP_STEP < self.BOARD_SIZE and y - JUMP_STEP >= 0 \
                    and not \
                    self.board.position[(x + JUMP_STEP, y - JUMP_STEP)] \
                    and self.board.position[(x + MOVE_STEP, y - MOVE_STEP)]\
                    and (x + MOVE_STEP, y - MOVE_STEP) \
                    not in self.player.checker_position:
                checker.can_jump = True
                checker.valid_jump.add((x + JUMP_STEP, y - JUMP_STEP))

            if checker.king:
                if x - JUMP_STEP >= 0 and y + JUMP_STEP < self.BOARD_SIZE \
                        and not\
                        self.board.position[(x - JUMP_STEP, y + JUMP_STEP)]\
                        and \
                        self.board.position[(x - MOVE_STEP, y + MOVE_STEP)]\
                        and (x - MOVE_STEP, y + MOVE_STEP) \
                        not in self.player.checker_position:
                    checker.can_jump = True
                    checker.valid_jump.add((x - JUMP_STEP, y + JUMP_STEP))

                if x + JUMP_STEP < self.BOARD_SIZE \
                        and y + JUMP_STEP < self.BOARD_SIZE \
                        and not \
                        self.board.position[(x + JUMP_STEP, y + JUMP_STEP)]\
                        and \
                        self.board.position[(x + MOVE_STEP, y + MOVE_STEP)]\
                        and (x + MOVE_STEP, y + MOVE_STEP) \
                        not in self.player.checker_position:
                    checker.can_jump = True
                    checker.valid_jump.add((x + JUMP_STEP, y + JUMP_STEP))

    def check_valid_move(self, checker):
        """Check valid move of a checker"""
        MOVE_STEP = 1
        checker.can_move = False
        checker.valid_move = set()

        x, y = checker.x, checker.y

        if self.player.take_turn:

            if x - MOVE_STEP >= 0 and y - MOVE_STEP >= 0\
                and not\
                    self.board.position[(x - MOVE_STEP, y - MOVE_STEP)]:
                checker.can_move = True
                self.player.no_moves = False
                checker.valid_move.add((x - MOVE_STEP, y - MOVE_STEP))

            if x + MOVE_STEP < self.BOARD_SIZE and y - MOVE_STEP >= 0\
                    and not \
                    self.board.position[(x + MOVE_STEP, y - MOVE_STEP)]:
                checker.can_move = True
                self.player.no_moves = False
                checker.valid_move.add((x + MOVE_STEP, y - MOVE_STEP))

            if checker.king:
                if x - MOVE_STEP >= 0 and y + MOVE_STEP < self.BOARD_SIZE \
                    and not \
                        self.board.position[(x - MOVE_STEP, y + MOVE_STEP)]:
                    checker.can_move = True
                    self.player.no_moves = False
                    checker.valid_move.add((x - MOVE_STEP, y + MOVE_STEP))

                if x + MOVE_STEP < self.BOARD_SIZE \
                        and y + MOVE_STEP < self.BOARD_SIZE \
                        and not \
                        self.board.position[(x + MOVE_STEP, y + MOVE_STEP)]:
                    checker.can_move = True
                    self.player.no_moves = False
                    checker.valid_move.add((x + MOVE_STEP, y + MOVE_STEP))

    def check_ai_valid_jump(self, checker):
        """Check valid jump of checkers"""
        JUMP_STEP = 2
        MOVE_STEP = 1
        checker.can_jump = False
        checker.valid_jump = set()

        x, y = checker.x, checker.y

        if self.ai.take_turn:

            if x - JUMP_STEP >= 0 and y + JUMP_STEP < self.BOARD_SIZE \
                    and \
                    not self.board.position[(x - JUMP_STEP, y + JUMP_STEP)]\
                    and self.board.position[(x - MOVE_STEP, y + MOVE_STEP)]\
                    and (x - MOVE_STEP, y + MOVE_STEP) \
                    not in self.ai.checker_position:
                checker.can_jump = True
                checker.valid_jump.add((x - JUMP_STEP, y + JUMP_STEP))

            if x + JUMP_STEP < self.BOARD_SIZE \
                    and y + JUMP_STEP < self.BOARD_SIZE \
                    and \
                    not self.board.position[(x + JUMP_STEP, y + JUMP_STEP)]\
                    and self.board.position[(x + MOVE_STEP, y + MOVE_STEP)]\
                    and (x + MOVE_STEP, y + MOVE_STEP) \
                    not in self.ai.checker_position:
                checker.can_jump = True
                checker.valid_jump.add((x + JUMP_STEP, y + JUMP_STEP))

            if checker.king:
                if x - JUMP_STEP >= 0 and y - JUMP_STEP >= 0 \
                        and not \
                        self.board.position[(x - JUMP_STEP, y - JUMP_STEP)]\
                        and \
                        self.board.position[(x - MOVE_STEP, y - MOVE_STEP)]\
                        and (x - MOVE_STEP, y - MOVE_STEP) \
                        not in self.ai.checker_position:
                    checker.can_jump = True
                    checker.valid_jump.add((x - JUMP_STEP, y - JUMP_STEP))

                if x + JUMP_STEP < self.BOARD_SIZE and y - JUMP_STEP >= 0 \
                        and not \
                        self.board.position[(x + JUMP_STEP, y - JUMP_STEP)]\
                        and \
                        self.board.position[(x + MOVE_STEP, y - MOVE_STEP)]\
                        and (x + MOVE_STEP, y - MOVE_STEP) \
                        not in self.ai.checker_position:
                    checker.can_jump = True
                    checker.valid_jump.add((x + JUMP_STEP, y - JUMP_STEP))

    def check_ai_valid_move(self, checker):
        """Check valid move of a checker"""
        MOVE_STEP = 1
        checker.can_move = False
        checker.valid_move = set()

        x, y = checker.x, checker.y

        if self.ai.take_turn:

            if x - MOVE_STEP >= 0 and y + MOVE_STEP < self.BOARD_SIZE\
                and \
                    not self.board.position[(x - MOVE_STEP, y + MOVE_STEP)]:
                checker.can_move = True
                self.ai.no_moves = False
                checker.valid_move.add((x - MOVE_STEP, y + MOVE_STEP))

            if x + MOVE_STEP < self.BOARD_SIZE \
                and y + MOVE_STEP < self.BOARD_SIZE \
                    and \
                    not self.board.position[(x + MOVE_STEP, y + MOVE_STEP)]:
                checker.can_move = True
                self.ai.no_moves = False
                checker.valid_move.add((x + MOVE_STEP, y + MOVE_STEP))

            if checker.king:
                if x - MOVE_STEP >= 0 and y - MOVE_STEP >= 0\
                        and not \
                        self.board.position[(x - MOVE_STEP, y - MOVE_STEP)]:
                    checker.can_move = True
                    self.ai.no_moves = False
                    checker.valid_move.add((x - MOVE_STEP, y - MOVE_STEP))

                if x + MOVE_STEP < self.BOARD_SIZE and y - MOVE_STEP >= 0\
                        and not \
                        self.board.position[(x + MOVE_STEP, y - MOVE_STEP)]:
                    checker.can_move = True
                    self.ai.no_moves = False
                    checker.valid_move.add((x + MOVE_STEP, y - MOVE_STEP))

    def activate_ai(self):
        print("Red Checker's Turn")
        ai_checker_holder = []
        ai_checker_valid_move = []
        ai_checker_valid_jump = []

        for ai_checker in self.ai_checkers:
            if ai_checker.can_jump:
                ai_checker_holder.append(ai_checker)
                for position in ai_checker.valid_jump:
                    ai_checker_valid_jump.append(position)
            elif ai_checker.can_move:
                ai_checker_holder.append(ai_checker)
                for position in ai_checker.valid_move:
                    ai_checker_valid_move.append(position)

        if len(ai_checker_valid_jump) > 0:
            MOVE_STEP = 1
            old_x, old_y = ai_checker_holder[0].x, ai_checker_holder[0].y

            ai_checker_holder[0].x, ai_checker_holder[0].y = (
                ai_checker_valid_jump[0])

            new_x, new_y = ai_checker_holder[0].x, ai_checker_holder[0].y

            if new_x > old_x and new_y < old_y:
                ai_checker_holder[0].remove_opponent = (
                    new_x - MOVE_STEP, new_y + MOVE_STEP)
            elif new_x < old_x and new_y < old_y:
                ai_checker_holder[0].remove_opponent = (
                    new_x + MOVE_STEP, new_y + MOVE_STEP)
            elif new_x < old_x and new_y > old_y:
                ai_checker_holder[0].remove_opponent = (
                    new_x + MOVE_STEP, new_y - MOVE_STEP)
            elif new_x > old_x and new_y > old_y:
                ai_checker_holder[0].remove_opponent = (
                    new_x - MOVE_STEP, new_y - MOVE_STEP)

            ai_checker_holder[0].board_x = \
                ai_checker_holder[0].HALF_SQAURE + ai_checker_holder[0].x\
                * ai_checker_holder[0].SQUARE_SIZE
            ai_checker_holder[0].board_y = \
                ai_checker_holder[0].HALF_SQAURE + ai_checker_holder[0].y\
                * ai_checker_holder[0].SQUARE_SIZE

            ai_checker_holder[0].jumped = True

            self.jump_and_remove()

        elif len(ai_checker_valid_move) > 0:
            ai_checker_holder[0].x, ai_checker_holder[0].y = (
                ai_checker_valid_move[0])
            ai_checker_holder[0].board_x = \
                ai_checker_holder[0].HALF_SQAURE + ai_checker_holder[0].x\
                * ai_checker_holder[0].SQUARE_SIZE
            ai_checker_holder[0].board_y = \
                ai_checker_holder[0].HALF_SQAURE + ai_checker_holder[0].y\
                * ai_checker_holder[0].SQUARE_SIZE
            ai_checker_holder[0].moved = True

        name = self.answer

        print(name + "'s Turn")

    def press_checker(self):
        """Press checker"""
        for checker in self.checkers:
            checker.mousePressed()

        # for ai_checker in self.ai_checkers:
        #     ai_checker.mousePressed()

    def drag_checker(self):
        """Drag checkers"""
        for checker in self.checkers:
            checker.mouseDragged()

        # for ai_checker in self.ai_checkers:
        #     ai_checker.mouseDragged()

    def release_checker(self):
        """Release checkers"""
        for checker in self.checkers:
            checker.mouseReleased()

        # for ai_checker in self.ai_checkers:
        #     ai_checker.mouseReleased()

        self.jump_and_remove()

    def take_turn(self):
        for checker in self.checkers:
            if checker.moved and self.player.take_turn \
                or (checker.jumped
                    and self.player.take_turn
                    and not checker.can_jump):
                if checker.jumped:
                    self.moves = 0
                else:
                    self.moves += 1
                self.player.take_turn = False
                self.ai.take_turn = True
                checker.jumped = False
                checker.moved = False

        for checker in self.ai_checkers:
            if checker.moved and self.ai.take_turn \
                or (checker.jumped
                    and self.ai.take_turn
                    and not checker.can_jump):
                if checker.jumped:
                    self.moves = 0
                else:
                    self.moves += 1
                self.ai.take_turn = False
                self.player.take_turn = True
                checker.jumped = False
                checker.moved = False

    def jump_and_remove(self):
        """Jump a checker and remove rival's checker"""
        for checker in self.checkers:
            if checker.jumped:
                for i in range(len(self.ai_checkers)):
                    if self.ai.checker_position[i] == checker.remove_opponent:
                        self.ai_checkers.pop(i)
            checker.remove_opponent = None

        for checker in self.ai_checkers:
            if checker.jumped:
                for i in range(len(self.checkers)):
                    if self.player.checker_position[i]\
                            == checker.remove_opponent:
                        self.checkers.pop(i)
            checker.remove_opponent = None

    def end_game(self):
        """End the game and set win or lose condition"""
        if self.checkers == []:
            self.display_end_text("Red")
        elif self.ai_checkers == []:
            self.display_end_text("Black")
        elif self.moves >= 50:
            self.display_end_text("Draw")

        if self.player.no_moves:
            self.display_end_text("Red")
        elif self.ai.no_moves:
            self.display_end_text("Black")

    def display_end_text(self, winner):
        """Display end of game message"""
        WHITE = 255
        LARGE = 100
        MID = 400
        fill(WHITE)
        textSize(LARGE)
        textAlign(CENTER)
        if winner == "Black":
            text(self.answer+" Wins", MID, MID)
            if not self.game_over:
                self.record_winner()
                self.game_over = True
        elif winner == "Red":
            text("Red Wins", MID, MID)
        elif winner == "Draw":
            text("Draw", MID, MID)

        self.player.take_turn = False
        self.ai.take_turn = False

    def record_winner(self):
        """Keep track of the winners in a file"""
        user_score = 1

        with open('scores.txt', 'r') as file:
            scores = file.readlines()

        scores_dict = {}
        for score in scores:
            name, value = score.strip().split()
            scores_dict[name] = int(value)

        if self.answer in scores_dict:
            scores_dict[self.answer] += user_score
        else:
            scores_dict[self.answer] = user_score

        sorted_scores = sorted(scores_dict.items(),
                               key=lambda x: x[1], reverse=True)

        with open('scores.txt', 'w') as file:
            for name, score in sorted_scores:
                text = "{} {}\n".format(name, score)
                file.write(text)
