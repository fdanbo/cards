
import random

# asterik means "any" or "unspecified" or something
RANKS = 'A23456789TJQK'
SUITS = '♡♣♢♠'


class CardNotFoundError(Exception):
    pass


# these index functions are not just used for ordering -- it's important that
# their absolute values are correct ('9' is 9, etc) and that consecutive cards
# differ by one.
def AceHighIndex(rank):
    if rank == 'A':
        return 14
    else:
        return RANKS.index(rank)+1


def AceLowIndex(rank):
    return RANKS.index(rank)+1


# eg, '8♡9♣T♢T♠Q♣'
class RankFirstOrderings:
    @staticmethod
    def AceHigh(card):
        rankindex = AceHighIndex(card.rank)
        suitindex = SUITS.index(card.suit)
        return (rankindex, suitindex)

    @staticmethod
    def AceLow(card):
        rankindex = AceLowIndex(card.rank)
        suitindex = SUITS.index(card.suit)
        return (rankindex, suitindex)


# a bridge-like ordering, eg '8♡9♣Q♣T♢T♠'
class SuitFirstOrderings:
    @staticmethod
    def AceHigh(card):
        rankindex = AceHighIndex(card.rank)
        suitindex = SUITS.index(card.suit)
        return (suitindex, rankindex)

    @staticmethod
    def AceLow(card):
        rankindex = AceLowIndex(card.rank)
        suitindex = SUITS.index(card.suit)
        return (suitindex, rankindex)


def CardMatcher(rank=None, suit=None):
    def matches(card):
        return ((rank is None or card.rank == rank) and
                (suit is None or card.suit == suit))
    if rank is not None:
        if rank not in RANKS or len(rank) != 1:
            raise ValueError('rank must be one of {}'.format(RANKS))
    if suit is not None:
        if suit not in SUITS or len(suit) != 1:
            raise ValueError('suit must be one of {}'.format(SUITS))
    return matches


class Card:
    # either pass the 2-character string or pass the rank & suit separately
    def __init__(self, string_or_rank, suit=None):
        if suit is None:
            # expect a 2-character string
            if len(string_or_rank) != 2:
                raise ValueError('must pass either a card '
                                 'string or rank & suit')
            rank = string_or_rank[0]
            suit = string_or_rank[1]
        else:
            rank = string_or_rank

        if rank not in RANKS or len(rank) != 1:
            raise ValueError('rank must be one of {}'.format(RANKS))

        if suit not in SUITS or len(suit) != 1:
            raise ValueError('suit must be one of {}'.format(SUITS))

        # cards are immutable so that they can be hashed -- never set _rank or
        # _suit directly.
        self._rank = rank
        self._suit = suit

    # cards are immutable so that they can be hashed, so we only provide
    # getters and not setters.
    @property
    def rank(self):
        return self._rank

    @property
    def suit(self):
        return self._suit

    def __eq__(self, rhs):
        return (self.rank == rhs.rank and
                self.suit == rhs.suit)

    def __hash__(self):
        return repr(self).__hash__()

    def __repr__(self):
        return self.rank+self.suit


class Hand:
    # pass either a string or an iterator of cards. if you pass neither, you'll
    # get an empty hand.
    def __init__(self, string_or_cardlist=None):
        if isinstance(string_or_cardlist, str):
            cardlist = [Card(rank, suit) for rank, suit in
                        zip(string_or_cardlist[::2], string_or_cardlist[1::2])]
        elif string_or_cardlist is None:
            cardlist = []
        else:
            cardlist = string_or_cardlist

        self._cardlist = list(cardlist)

    def __iter__(self):
        for card in self._cardlist:
            yield card

    def __copy__(self):
        return type(self)(self._cardlist)

    def append(self, card):
        return self._cardlist.append(card)

    def extend(self, cardlist):
        return self._cardlist.extend(cardlist)

    def sort(self, key):
        return self._cardlist.sort(key=key)

    def shuffle(self):
        return random.shuffle(self._cardlist)

    # an important difference between this pop() and list.pop() is that the
    # index defaults to 0 (front of list) not -1 (back of list).
    def pop(self, index=0):
        return self._cardlist.pop(index)

    def insert(self, index, card):
        return self._cardlist.insert(index, card)

    def popn(self, count):
        result = self._cardlist[0:count]
        del self._cardlist[0:count]
        return result

    def __len__(self):
        return len(self._cardlist)

    # get the list of cards with hand[:]
    def __getitem__(self, _slice):
        return self._cardlist[_slice]

    def __setitem__(self, _slice, value):
        self._cardlist[_slice] = value

    def __repr__(self):
        return ''.join(repr(x) for x in self._cardlist)

    # I just provide this because the font support sucks in my terminal;
    # unreadable without the spaces.
    def pretty(self):
        return ' '.join(repr(x) for x in self._cardlist)

    def popcard(self, rank=None, suit=None):
        matcher = CardMatcher(rank, suit)
        for i, c in enumerate(self._cardlist):
            if matcher(c):
                return self._cardlist.pop(i)
        raise CardNotFoundError

    def countcards(self, rank=None, suit=None):
        matcher = CardMatcher(rank, suit)
        return sum(1 for c in self._cardlist if matcher(c))


# a deck is a hand with a different constructor.  it's provided as a separate
# class to make code more clear/readable -- conceptually, a Hand and a Deck are
# different things, even though they're implemented the same.
class Deck(Hand):
    def __init__(self, deckcount=1, shuffle=True):
        super().__init__()
        self._cardlist = [Card(rank, suit)
                          for i in range(deckcount)
                          for suit in SUITS
                          for rank in RANKS]
        if shuffle:
            self.shuffle()

    # same as pop(), but doesn't take an index
    def deal(self):
        return self._cardlist.pop(0)

    # same as popn()
    def dealn(self, count):
        result = self._cardlist[0:count]
        del self._cardlist[0:count]
        return result
