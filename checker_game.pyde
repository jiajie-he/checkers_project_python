SQUARE_SIZE = 100
BOARD_SIZE = 8


def setup():
    global gc
    from game_controller import GameController
    size(SQUARE_SIZE * BOARD_SIZE, SQUARE_SIZE * BOARD_SIZE)
    answer = input('enter your name')
    if answer:
        print('Hi ' + answer)
    elif answer == '':
        answer='Player'
        print('Player')
    else:
        answer='Player'
        print('Player')  # Canceled dialog will print None
    gc = GameController(SQUARE_SIZE, BOARD_SIZE, answer)



def draw():
    gc.update()


def mousePressed(self):
    gc.press_checker()


def mouseDragged(self):
    gc.drag_checker()


def mouseReleased(self):
    gc.release_checker()


def input(self, message='Welcome to Checkers Game! Please enter your name'):
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)
