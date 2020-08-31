# -*- coding: utf-8 -*-

from mlhearts.hearts.cards import Card, NO_CARDS
from mlhearts.hearts.pile import Pile

NO_TURNS = 52
NO_PLAYERS = 4
HAND_SIZE = 13


class PlayerData():
    """
    Holds onto (non-global) data specific to a player.
    """
    def __init__(self):
        self.collected = Pile()
        self.hand = Pile()
       
    def resetPiles(self):
        self.collected.empty()
        self.hand.empty()


class State():
    """
    Tracks and updates the round state of a Hearts game. It provides manipulation 
    functions to update the state through game events and helper functions to fetch 
    information about the round.
    
    This interface is meant to be wrapped, e.g. into a class or function, to abstract 
    an entire game.
    """
    def __init__(self):
        self.deck = Pile(list(range(NO_CARDS)))
        self.players = [PlayerData() for i in range(NO_PLAYERS)]
        self.trick = Pile()

        # game data 
        self._trick_num = 0
        self._turn_num = 0

        self._current_player = None
        self._lead_trick_player = None
        self._lead_suit = None
        
        self._hearts_broken = False
        self._legal_move_idxs = []

        self.state_params = {}

    # -*- getters and setters -*-
    
    def getTrickPile(self):
        return self.trick
    
    def getPlayerArray(self):
        return self.players 

    def setTrickNum(self, num):
        self._trick_num = num
        self.state_params["trick_num"] = num

    def getTrickNum(self):
        return self._trick_num

    def setTurnNum(self, num):
        self._turn_num = num
        self.state_params["turn_num"] = num

    def getTurnNum(self):
        return self._turn_num

    def setCurrentPlayer(self, idx):
        self._current_player = idx
        self.state_params["current_player"] = idx

    def getCurrentPlayer(self):
        return self._current_player
 
    def setLeadTrickPlayer(self, idx):
        self._lead_trick_player = idx
        self.state_params["lead_trick_player"] = idx

    def getLeadTrickPlayer(self):
        return self._lead_trick_player

    def setLeadSuit(self, suit):
        self._lead_suit = suit
        self.state_params["lead_suit"] = suit 

    def getLeadSuit(self):
        return self._lead_suit

    def setHeartsBroken(self, boolean):
        self._hearts_broken = boolean
        self.state_params["hearts_broken"] = boolean

    def getHeartsBroken(self):
        return self._hearts_broken

    def getLegalMoveIndices(self):
        return self._legal_move_idxs

    # -*- state functions and round mechanics -*-
    
    def resetState(self):
        """
        Assign (reset) the state and card piles to their initial values.
        """
        self.setTurnNum(0)
        self.setTrickNum(0)
        self.setCurrentPlayer(None)
        self.setLeadTrickPlayer(None)
        self.setLeadSuit(None)
        self.setHeartsBroken(False)
        
        self.trick.empty()
        
        for p in self.players:
            p.resetPiles()

    def dealCards(self):
        """
        Shuffle and then deal cards to the players.
        """
        self.deck.shuffle()
        for i in range(NO_PLAYERS):
            self.players[i].hand.append(self.deck[13*i:13*(i+1)])
            self.players[i].hand.sort()
            
    def hasSuit(self, player_idx, suit):
        """
        Checks if a player owns a card of a given suit.
        """
        if suit == None:
            return False
        for card in self.players[player_idx].hand:
            if card.get_suit() == suit:
                return True
        return False

    def getPlayerHoldingCard(self, target_card):
        """
        Returns the index of the player which owns a given card.

        If no player owns the card, returns None.
        """
        for i in range(NO_PLAYERS):
            for card in self.players[i].hand:
                if card == target_card:
                    return i
        return None

    def updateLegalMoveIndices(self):
        """
        Updates the legal move array for the current player to move.
        """
        self._legal_move_idxs.clear()

        hand = self.players[self._current_player].hand

        has_lead_suit = self.hasSuit(self._current_player, self._lead_suit)

        for i in range(len(hand)):
            c_rank = hand[i].get_rank()
            c_suit = hand[i].get_suit()

            if self._turn_num == 0:
                # must play two of clubs on first turn
                if c_rank == 0 and c_suit == 0:
                    self._legal_move_idxs.append(i)
                    break
            elif self._turn_num > 0 and self._turn_num < 4:
                # follow suit if possible, otherwise play anything
                # (except hearts/queen of spades)
                if has_lead_suit:
                    if self._lead_suit == c_suit:
                        self._legal_move_idxs.append(i)
                else:
                    if c_suit != 3 and not (c_rank == 10 and c_suit == 2):
                        self._legal_move_idxs.append(i)
            elif self._turn_num % NO_PLAYERS == 0:
                # new trick, play anything
                # (except hearts if they have not been broken)
                if self._hearts_broken:
                    self._legal_move_idxs.append(i)
                elif c_suit != 3:
                    self._legal_move_idxs.append(i)
            else:
                # follow suit if possible, otherwise play anything
                if has_lead_suit:
                    if self._lead_suit == c_suit:
                        self._legal_move_idxs.append(i)
                else:
                    self._legal_move_idxs.append(i)

        # The legal moves table should never be empty! However, it is possible from
        # the above implementation if the player either:
        #
        # * has all hearts at the start
        # * has to lead with hearts but hearts are not broken
        #
        # The method below corrects this.
        if len(self._legal_move_idxs) == 0:
            for i in range(len(hand)):
                self._legal_move_idxs.append(i)

    def selectAction(self, action_idx):
        """
        With a given index, play a card from the current player to move.
        """
        p_c = self._current_player
        
        card = self.players[p_c].hand.pop_at_idx(action_idx)

        c_suit = card.get_suit()
       
        if c_suit == 3:
            self.setHeartsBroken(True)
        
        self.trick.append(card)

        # trick has started
        if self._turn_num % NO_PLAYERS == 0:
            self.setLeadSuit(c_suit)
            self.setLeadTrickPlayer(p_c)

        self.setTurnNum(self._turn_num + 1)
        self.setCurrentPlayer((p_c + 1) % NO_PLAYERS)

    def calcTrickWinner(self):
        """
        Calculate the winner of a trick.
        """
        trick_winner_index = self._lead_trick_player
        max_rank = self.trick[0].get_rank()

        if self._turn_num % NO_PLAYERS != 0:
            return None
        else:
            # "i_r" -> relative player index (to _lead_trick_player)
            for i_r in range(1,NO_PLAYERS):
                i_r_suit = self.trick[i_r].get_suit()
                i_r_rank = self.trick[i_r].get_rank()
                if self._lead_suit == i_r_suit and i_r_rank > max_rank:
                    max_rank = i_r_rank
                    trick_winner_index = (self._lead_trick_player + i_r) % NO_PLAYERS
            return trick_winner_index

    def updateToNextTrick(self):
        """
        Assign the next player to start the next trick and clear the current 
        trick pile. To use together with 'move', run this when 
        
            self.turn_no % NO_PLAYERS == 0
        """
        # a trick is complete
        winner_index = self.calcTrickWinner()

        self.setTrickNum(self._trick_num + 1)
        self.setCurrentPlayer(winner_index)
        self.setLeadTrickPlayer(winner_index)
        self.players[winner_index].collected.append(self.trick)
        self.trick.empty()

    def tallyScores(self):
        """
        Compute the score of each player and return a list of values (with index
        corresponding to player numbers).
        """
        scores = []
        for i in range(NO_PLAYERS):
            points = 0
            for card in self.players[i].collected:
                if card.get_suit() == 3:
                    points += 1
                elif card.get_suit() == 2 and card.get_rank() == 10:
                    points += 13
            scores.append(points)

        # check if moon was shot
        if 26 in scores:
            moon_index = scores.index(26)
            for i in range(NO_PLAYERS):
                if i == moon_index:
                    scores[i] = 0
                else:
                    scores[i] = 26
                    
        return scores