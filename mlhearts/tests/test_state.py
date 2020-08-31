# -*- coding: utf-8 -*-
"""
Unit tests for the State class in mlhearts.hearts.state.
"""
import unittest
from mlhearts.hearts.cards import Card, NO_SUITS
from mlhearts.hearts.state import State

class TestState(unittest.TestCase):
    """
    Test for non-trivial State methods. Future tests may be added for other
    methods if the code is refactored for new rules or new game mechanics.
    """
    @classmethod
    def setUpClass(cls):
        cls.state = State()

    def test_State_updateLegalMoveIndices(self):
        p = self.state.players

        # --- test first turn condition ---
        p[0].hand.append([Card(0), Card(1)])
        j = self.state.getPlayerHoldingCard(Card(0))
        self.state._turn_num = 0
        self.state._current_player = j
        
        self.assertEqual(0,j)

        self.state.updateLegalMoveIndices()

        self.assertEqual(self.state._legal_move_idxs, [0])

        self.state.resetState()

        # --- test first trick condition ---
        # 3 of diamonds, 3 of clubs
        p[0].hand.append([Card(1,1), Card(1,0)])
        self.state._turn_num = 1
        self.state._current_player = 0
        self.state._lead_suit = 0
        self.state.updateLegalMoveIndices()

        self.assertEqual(self.state._legal_move_idxs, [1])

        self.state.resetState()

        # Q of spades, A of hearts, 2 of diamonds
        p[0].hand.append([Card(10,2), Card(12,3), Card(0,1)])
        self.state._turn_num = 1
        self.state._current_player = 0
        self.state._lead_suit = 0
        self.state.updateLegalMoveIndices()

        self.assertEqual(self.state._legal_move_idxs, [2])

        self.state.resetState()

        # --- test starting trick action (after first trick) ---
        p[0].hand.append([Card(10,s) for s in range(NO_SUITS)])
        self.state._turn_num = 4
        self.state._current_player = 0
        self.state.updateLegalMoveIndices()

        # hearts not broken
        self.assertEqual(self.state._legal_move_idxs, [i for i in range(NO_SUITS-1)])

        self.state._hearts_broken = True
        self.state.updateLegalMoveIndices()

        # hearts are broken
        self.assertEqual(self.state._legal_move_idxs, [i for i in range(NO_SUITS)])

        self.state.resetState()

        # --- test non-starting trick action (after first trick) ---
        p[0].hand.append([Card(10,2), Card(12,3), Card(0,1)])
        self.state._turn_num = 5
        self.state._current_player = 0
        self.state._lead_suit = 1
        self.state.updateLegalMoveIndices()

        self.assertEqual(self.state._legal_move_idxs, [2])

        self.state._lead_suit = 0
        self.state.updateLegalMoveIndices()

        self.assertEqual(self.state._legal_move_idxs, [0,1,2])

        self.state.resetState()

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()