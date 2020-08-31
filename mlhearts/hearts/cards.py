# -*- coding: utf-8 -*-

NO_RANKS = 13
NO_SUITS = 4
NO_CARDS = 52

_rankmap = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
           "J", "Q", "K", "A"]
_suitmap = ["c", "d", "s", "h"]

class Card():
    """Standard playing card class."""
    def __init__(self, rank, suit=None):
        if suit is not None:
            self.rank = rank
            self.suit = suit
        else:
            self.rank = rank % NO_RANKS
            self.suit = rank // NO_RANKS

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def __lt__(self, card):
        if self.suit < card.suit:
            return True
        elif self.suit == card.suit and self.rank < card.rank:
            return True
        else:
            return False

    def __eq__(self, card):
        if self.suit == card.suit and self.rank == card.rank:
            return True
        else:
            return False

    def __int__(self):
        return (NO_RANKS * self.suit) + self.rank

    def __str__(self):
        return "%s%s" % (_rankmap[self.rank], _suitmap[self.suit])
