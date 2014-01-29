
import random

RANKS = 'A23456789TJQK'
SUITS = '♡♣♢♠'


# for the purpose of ordering, we assign an integer "index" to the ranks based
# on whether aces are high or low.
def ace_low_index(r):
    return RANKS.index(r) + 1


def ace_high_index(r):
    index = RANKS.index(r) + 1
    return 14 if index == 1 else index


def index_to_rank(i):
    if i == 14:
        i = 1
    return RANKS[i-1]


class DeckEmptyError(Exception):
    pass


class card:
    def __init__(self, string):
        assert string[0] in RANKS
        assert string[1] in SUITS
        self.rank = string[0]
        self.suit = string[1]

    def __repr__(self):
        return self.rank+self.suit

    def clone(self):
        return card(self.rank, self.suit)

    def ace_low_index(self):
        return ace_low_index(self.rank)

    def ace_high_index(self):
        return ace_high_index(self.rank)


# s is something like 'A♡5♣7♡A♠J♣'
def makehand(s):
    cardlist = []
    for rank, suit in zip(s[::2], s[1::2]):
        cardlist.append(card(rank+suit))
    return cardlist


class deck:
    def __init__(self, deckcount=1):
        self.cardlist = [
            card(rank+suit)
            for n in range(deckcount)
            for suit in SUITS
            for rank in RANKS
        ]

    def shuffle(self):
        random.shuffle(self.cardlist)

    def dealone(self):
        try:
            return self.cardlist.pop()
        except IndexError:
            raise DeckEmptyError

    def deal(self, count=1):
        return [self.dealone() for i in range(count)]

    # card_wanted can be a rank ('K'), a card string ('K♠'), or a card object.
    # c should be a card object.
    def _cardmatches(self, c, card_wanted):
        try:
            rank_wanted = card_wanted.rank
            suit_wanted = card_wanted.suit
        except AttributeError:
            # must be a string
            rank_wanted = card_wanted[0]
            suit_wanted = card_wanted[1] if len(card_wanted) > 1 else None
        if suit_wanted is None:
            return c.rank == rank_wanted
        else:
            return c.rank == rank_wanted and c.suit == suit_wanted

    def dealspecificcard(self, card_wanted):
        for i, c in enumerate(self.cardlist):
            if self._cardmatches(c, card_wanted):
                return self.cardlist.pop(i)
        raise DeckEmptyError

    def countspecificcard(self, card_wanted):
        count = 0
        for c in self.cardlist:
            if self._cardmatches(c, card_wanted):
                count += 1
        return count

    def __repr__(self):
        return ''.join(str(x) for x in reversed(self.cardlist))
