class Checker:
    """Create a checker"""

    def __init__(self, x, y, color):
        """Initialize the checker"""
        self.SQUARE_SIZE = 100
        self.HALF_SQAURE = 50
        self.x = x
        self.y = y
        self.board_x = self.HALF_SQAURE + self.x * self.SQUARE_SIZE
        self.board_y = self.HALF_SQAURE + self.y * self.SQUARE_SIZE
        self.color = color
        self.king = False

        self.can_jump = False
        self.valid_jump = set()
        self.can_move = False
        self.valid_move = set()

        self.is_dragged = False
        self.jumped = False
        self.moved = False
        self.remove_opponent = None

    def display(self):
        """Draw the checkers"""
        BLACK = 0
        RED = (255, 0, 0)
        WHITE = 255
        CIRCLE_STROKE_WEIGHT = 2
        BIG = 90
        SMALL = 70
        CHECKER_OUTTER = (self.board_x, self.board_y, BIG, BIG)
        CHECKER_INNER = (self.board_x, self.board_y, SMALL, SMALL)

        if self.color == "Black":
            fill(BLACK)
        else:
            fill(*RED)
        stroke(WHITE)

        # outter cycle
        strokeWeight(CIRCLE_STROKE_WEIGHT)
        if self.can_move or self.can_jump:
            self.highlight()
        ellipse(*CHECKER_OUTTER)

        # inner cycle
        strokeWeight(CIRCLE_STROKE_WEIGHT)
        ellipse(*CHECKER_INNER)

        # draw the king sign
        if self.king:
            self.draw_king()

    def mousePressed(self):
        """Turn on switch"""
        CIRCLE_RADIUS = 45
        if dist(mouseX, mouseY, self.board_x, self.board_y) < CIRCLE_RADIUS:
            self.is_dragged = True

    def mouseDragged(self):
        """Move the checkers"""
        CIRCLE_RADIUS = 45
        if dist(mouseX, mouseY, self.board_x, self.board_y) < CIRCLE_RADIUS \
                and self.is_dragged and (self.can_move or self.can_jump):
            self.board_x = mouseX
            self.board_y = mouseY

    def mouseReleased(self):
        """Release the checkers"""
        MOVE_STEP = 1
        if self.is_dragged:
            if self.can_jump:
                for new_x, new_y in self.valid_jump:
                    if new_x * self.SQUARE_SIZE < mouseX \
                        < new_x * self.SQUARE_SIZE + self.SQUARE_SIZE \
                        and new_y * self.SQUARE_SIZE < mouseY \
                            < new_y * self.SQUARE_SIZE + self.SQUARE_SIZE:

                        if new_x > self.x and new_y < self.y:
                            self.remove_opponent = (
                                new_x - MOVE_STEP, new_y + MOVE_STEP)
                        elif new_x < self.x and new_y < self.y:
                            self.remove_opponent = (
                                new_x + MOVE_STEP, new_y + MOVE_STEP)
                        elif new_x < self.x and new_y > self.y:
                            self.remove_opponent = (
                                new_x + MOVE_STEP, new_y - MOVE_STEP)
                        elif new_x > self.x and new_y > self.y:
                            self.remove_opponent = (
                                new_x - MOVE_STEP, new_y - MOVE_STEP)

                        self.x, self.y = new_x, new_y

                        self.board_x = self.HALF_SQAURE + \
                            new_x * self.SQUARE_SIZE
                        self.board_y = self.HALF_SQAURE + \
                            new_y * self.SQUARE_SIZE
                        self.jumped = True

                    else:
                        self.board_x = self.HALF_SQAURE + \
                            self.x * self.SQUARE_SIZE
                        self.board_y = self.HALF_SQAURE + \
                            self.y * self.SQUARE_SIZE

            if self.can_move:
                for new_x, new_y in self.valid_move:
                    if new_x * self.SQUARE_SIZE <= mouseX \
                        <= new_x * self.SQUARE_SIZE + self.SQUARE_SIZE \
                        and new_y * self.SQUARE_SIZE <= mouseY \
                            <= new_y * self.SQUARE_SIZE + self.SQUARE_SIZE:
                        self.x, self.y = new_x, new_y
                        self.board_x = self.HALF_SQAURE + \
                            new_x * self.SQUARE_SIZE
                        self.board_y = self.HALF_SQAURE + \
                            new_y * self.SQUARE_SIZE
                        self.moved = True

                    else:
                        self.board_x = self.HALF_SQAURE + \
                            self.x * self.SQUARE_SIZE
                        self.board_y = self.HALF_SQAURE + \
                            self.y * self.SQUARE_SIZE
        self.is_dragged = False

    def highlight(self):
        """Highlight moveable checkers"""
        CIRCLE_RADIUS = 45
        Light = 4
        distance = dist(mouseX, mouseY, self.board_x, self.board_y)
        if distance < CIRCLE_RADIUS:
            strokeWeight(Light)

    def draw_king(self):
        """Draw king checkers"""
        CROWN = loadImage("crown.png")
        IMG_CENTER_X = 30
        IMG_CENTER_Y = 35
        image(CROWN, self.board_x - IMG_CENTER_X, self.board_y - IMG_CENTER_Y)
