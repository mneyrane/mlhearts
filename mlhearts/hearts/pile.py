import random

from mlhearts.hearts.cards import Card, NO_RANKS, NO_CARDS

class Pile():
    """
    Pile class. Abstracts the idea of a hand, deck, draw pile, discard pile, etc.
    """
    def __init__(self, items=None):
        self._cards = None

        if items is None:
            self._cards = []
        elif isinstance(items, list):
            self._cards = [self._item_to_card(i) for i in items]
        else:
            raise TypeError("'items' must be a list containing Card or int")

    def append(self, obj):
        if isinstance(obj, Card):
            self._cards.append(obj)
        elif isinstance(obj, int):
            self._cards.append(Card(obj))
        elif isinstance(obj, Pile):
            self._cards += obj._cards
        elif isinstance(obj, list):
            self._cards += [self._item_to_card(i) for i in obj]
        else:
            raise TypeError("'item' is not a Card, int, Pile or list")

    def peek_at_idx(self, index):
        return self._cards[index]

    def pop_at_idx(self, index):
        return self._cards.pop(index)

    def sort(self):
        self._cards.sort()

    def shuffle(self):
        random.shuffle(self._cards)

    def empty(self):
        self._cards.clear()

    def _item_to_card(self, item):
        if isinstance(item, Card):
            return item
        elif isinstance(item, int):
            return Card(item)
        else:
            raise TypeError("'item' is not a Card or int")

    def __getitem__(self, key):
        return self._cards[key]

    def __iter__(self):
        return iter(self._cards)

    def __len__(self):
        return len(self._cards)

    def __str__(self):
        size = len(self._cards)
        string = ''
        for i in range(size):
            string += self._cards[i].__str__() + ' '
        return '( %s)' % string
