# checkers_project_python

## Description

Checkers game built using Python/Processing.

## Usage

Fully playable game of Checkers completing with an AI opponent

## Installation

Install Processing3 (https://github.com/processing/processing/releases/tag/processing-0270-3.5.4) with Python Mode (https://github.com/jdf/processing.py)

## Program Design

### Data Structures Used

- Dictionary - {tuple of checker position : whether check can move or not}
- Set - {(x1,y1), (x2,y2)}valid move and jump
- List - [(x,y)]tuple checker position

### Defining Classes and Methods

- class GameControll - handle game operation
  - methods:
    - def update():
      update board and chcker, constantly being called by Processing draw method
    - def update_board_position():
      update checker position on board
    - def check_valid_move():
      check if checker can move
    - def check_valid_jump():
      check if checker can jump
    - def drag_checker():
      handle mouse drag
    - def release_checker():
      handle mouse release
    - def end_game():
      determine win or lose
    - def display_end_text():
      display appropriate text
    - def create_king():
      make a chcker king if they've reached the opposite side
- class Board - create board

  - methods:
    - def display():
      #draw board with color and size, etc.

- class Checker - create checker, handle checker function

  - methods:
    - def display():
      draw check with color, size, etc.
    - def mouseDragged():
      move checker to mouse when dragged
    - def mouseRelease():
      check if checker can jump or move, place checker accordingly
    - def highlight():
      higlight moveable checker when mouse is over it
    - def draw_king():
      draw king checker

- class Player - create player

  - methods:
    - def allow_move():
      allow player to make a move
    - def count_move():
      count the number of moves
    - def store_checker_position():
      store player checker position

- class AI - create AI
  - methods:
    - def count_move():
      count the number of moves
    - def checker_jump():
      allow valid jump
    - def checker_move():
      allow valid move
    - def pause():
      pause AI

### Flow of Control

- When the user makes a move
  - Check if there is a jumpable checker, if so jump must be taken and remove the opponent checker
  - Allow player to select a black checker that can move legally
  - Moveable checker is higlighted when mouse is over it
- When the checker is moved to a legal position (or not)
  - If the move is legal, move the piece and update the board
  - If not legal, place the checker back to the last position
- When it’s the computer’s turn
  - Check if there is a jumpable checker, if so, jump and remove the opponent checker
  - Randomly and legally move a red checker
- When game over status is assessed
  - Check who won, what color checker is on the board, display appropriate statement
