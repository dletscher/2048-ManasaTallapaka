

from Game2048 import *
import math
from typing import Tuple, Optional

_WEIGHTS = (
    ( 65536, 16384,  4096, 1024),
    (   256,    64,    16,    4),
    (     1,     2,     8,   32),
    (   128,   512,  2048, 8192),
)
_EMPTY_BONUS = 1000
_MAX_DEPTH = 4


class Player(BasePlayer):
    """Iterative‑deepening expectimax player for *Game 2048*."""

    # Construction & book‑keeping
  
    def __init__(self, timeLimit: float):
        # Call the contest’s BasePlayer initializer (sets self._timeLimit, etc.).
        BasePlayer.__init__(self, timeLimit)

        # Simple statistics you can dump via stats().
        self._movesPlayed     = 0
        self._nodesExpanded   = 0
        self._maxDepthReached = 0

    # PUBLIC ENTRY POINT – called once per move by Play.py
 
    def findMove(self, state):
        """Choose a move using iterative‑deepening expectimax search."""

        self._movesPlayed += 1
        bestMove: Optional[str] = None
        depth = 1  # player‑ply pairs

        while depth <= _MAX_DEPTH and self.timeRemaining():
            value, move = self._maximize(state, depth)
            if not self.timeRemaining():  # ran out of time mid‑iteration
                break
            bestMove = move
            self._maxDepthReached = depth
            depth += 1

        # Fallback when no legal moves (should only happen if game already over)
        if bestMove is None:
            actions = state.actions()
            bestMove = actions[0] if actions else 'U'

        self.setMove(bestMove)

    # EXPECTIMAX RECURSION
  
    def _maximize(self, state, depth: int) -> Tuple[float, Optional[str]]:
        """Return *(expected value, bestMove)* for the *player* node."""

        self._nodesExpanded += 1

        # Terminal tests
        if depth == 0 or state.gameOver() or not self.timeRemaining():
            return self._evaluate(state), None

        bestValue = -math.inf
        bestMove  = None

        for action in state.actions():
            if not self.timeRemaining():
                break
            value = self._expect(state, action, depth - 1)
            if value > bestValue:
                bestValue, bestMove = value, action

        return bestValue, bestMove

    def _expect(self, state, action: str, depth: int) -> float:
        """Expected utility after taking *action* and spawning a random tile."""

        expected = 0.0
        for successor, prob in state.possibleResults(action):
            if not self.timeRemaining():
                break
            if depth == 0:
                expected += prob * self._evaluate(successor)
            else:
                expected += prob * self._maximize(successor, depth - 1)[0]
        return expected

  
    # HEURISTIC EVALUATION FUNCTION

    def _evaluate(self, state) -> float:
        """Fast static evaluation of a board position."""
        total  = 0
        empty  = 0

        for r in range(4):
            for c in range(4):
                exp = state.getTile(r, c)  # 0 = empty, i = 2**i
                if exp == 0:
                    empty += 1
                else:
                    total += (1 << exp) * _WEIGHTS[r][c]

        return total + empty * _EMPTY_BONUS + state.getScore()

    def stats(self):
        print(f"Moves played: {self._movesPlayed}")
        print(f"Nodes expanded: {self._nodesExpanded}")
        print(f"Max depth reached: {self._maxDepthReached}")

    def saveData(self, filename):
        # Not used in this agent, but provided for completeness.
        pass

    def loadData(self, filename):
        pass
