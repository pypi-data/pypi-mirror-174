# Tic-Tac-Toe Arena Helpers

This package includes helper classes for Tic Tac Toe Arena, the COMP3900 project for W18B - TheBigMacs.

These helpers allow the user to easily parse the input and create the output as required by our API. This is in the form of two straight-forward [dataclasses](https://docs.python.org/3/library/dataclasses.html): AgentMove, and GameState.

GameState defines the information the agent has available with which to make a decision. It has the attributes:

* rows
* cols
* k
* current_move
* grid

AgentMove helps the agent declare the position it wishes to make a move in. It simply has the attributes row and col.

In order to create an agent that fits our API, the user simply needs to implement a function such that it takes in an input GameState and returns an AgentMove, such as the following.

```python
from comp3900_ttt_arena_helpers import AgentMove, GameState

def make_move(game_state: GameState) -> AgentMove:
    """
    Dummy agent that looks for the first empty cell it can find and makes a move there
    """

    for row in range(game_state.rows):
        for col in range(game_state.cols):
            if game_state.grid[row][col] == "":
                return AgentMove(row, col)
```
