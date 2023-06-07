from game_controller import GameController
from player import Player
from AI import AI
from checker import Checker
from board import Board


def test_constructor():
    gc = GameController(100, 8, "5001")

    # Assert that the game controller's properties were initialized correctly
    assert gc.BOARD_SIZE == 8
    assert gc.SQUARE_SIZE == 100
    assert gc.move_count == 0
    assert gc.result is None
    assert gc.moves == 0
    assert gc.answer == "5001"
    assert gc.game_over is False
