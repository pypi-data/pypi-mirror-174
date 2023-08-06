"""
Classes available to a user-defined agent

The agent ingests a game state, and returns an agent move
"""


from dataclasses import dataclass


@dataclass
class AgentMove:
    row: int
    col: int


@dataclass
class GameState:
    rows: int
    cols: int
    k: int
    current_move: str
    grid: list[list[str]]
