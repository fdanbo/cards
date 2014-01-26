
import random


class DeckEmptyError(Exception):
    pass


class card:
    RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
    SUITS = ('♡', '♣', '♢', '♠')

    # rank is 1 (ace) to 13 (King)
    # suit is 0-3, hearts, clubs, diamonds, spades
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return '{}{}'.format(card.RANKS[self.rank-1],
                             card.SUITS[self.suit])

    @staticmethod
    def fromstring(string):
        return card(card.RANKS.index(string[0])+1,
                    card.SUITS.index(string[1]))

    def clone(self):
        return card(self.rank, self.suit)


class deck:
    def __init__(self, deckCount=1):
        self.deck = []
        for deckNumber in range(0, deckCount):
            for suit in range(4):
                for rank in range(1, 14):
                    self.deck.append(card(rank, suit))
        self.nextCardIndex = 0

    def shuffle(self):
        random.shuffle(self.deck)
        self.nextCardIndex = 0

    def dealone(self):
        try:
            nextCard = self.deck[self.nextCardIndex]
        except IndexError:
            raise DeckEmptyError
        self.nextCardIndex += 1
        return nextCard

    def deal(self, count=1):
        return [self.dealone() for i in range(count)]

    def dealspecificcard(self, rank, suit=None):
        n = self.nextCardIndex
        for i in range(n, len(self.deck)):
            if self.deck[i].rank == rank:
                if suit is None or suit == self.deck[i].suit:
                    (self.deck[i], self.deck[n]) = (self.deck[n], self.deck[i])
                    return self.dealone()
        raise DeckEmptyError

    def getCardCount(self):
        return len(self.deck)-self.nextCardIndex

    def getCardsLeft(self, rank):
        count = 0
        n = self.nextCardIndex
        for i in range(n, len(self.deck)):
            if self.deck[i].rank == rank:
                count += 1
        return count

    def __repr__(self):
        return ' '.join(str(x) for x in self.deck[self.nextCardIndex:])
