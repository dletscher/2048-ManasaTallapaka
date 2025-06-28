# MyAgent.py  –  High‑score expectimax agent for Game‑2048
# Requires the driver’s BasePlayer and board State API from Game2048.py

import math
from typing import Tuple, Optional
from Game2048 import BasePlayer

# ───────────────────────────────────────── tunables ──────────────────────────
_MAX_DEPTH          = 6         # iterative‑deepening ceiling (adjust if needed)
_EMPTY_WEIGHT       = 270.0     # weight for each empty tile
_MONOTONICITY_WEIGHT = 47.0     # monotonic rows / columns
_CORNER_MAX_BONUS   = 10000.0   # reward if max tile sits in a corner

# Positional weights (snake pattern)
_POS_W = (
    (65536, 16384,  4096, 1024),
    (  256,    64,    16,    4),
    (    1,     2,     8,   32),
    (  128,   512,  2048, 8192),
)

# ────────────────────────────────────────── player ────────────────────────────
class Player(BasePlayer):
    """Iterative‑deepening expectimax agent tuned for high scores."""

    def __init__(self, timeLimit: float):
        super().__init__(timeLimit)
        self._moves = 0
        self._nodes = 0
        self._depthHit = 0

    # PUBLIC entry
    def findMove(self, state):
        self._moves += 1
        bestMove, depth = None, 1

        while depth <= _MAX_DEPTH and self.timeRemaining():
            value, move = self._maxNode(state, depth)
            if not self.timeRemaining():          # ran out mid‑iteration
                break
