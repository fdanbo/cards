
import cards
import collections
import unittest


class CardsTest(unittest.TestCase):
    def test_card(self):
        c = cards.card('K♠')
        self.assertEqual(c.rank, 'K')
        self.assertEqual(c.suit, '♠')
        self.assertEqual(repr(c), 'K♠')
        self.assertEqual(str(c), 'K♠')
        self.assertEqual(c.ace_low_index(), 13)
        self.assertEqual(c.ace_high_index(), 13)

        c = cards.card('A♡')
        self.assertEqual(c.rank, 'A')
        self.assertEqual(c.suit, '♡')
        self.assertEqual(repr(c), 'A♡')
        self.assertEqual(str(c), 'A♡')
        self.assertEqual(c.ace_low_index(), 1)
        self.assertEqual(c.ace_high_index(), 14)

    def create_shuffled_deck(self, deckcount=1):
        deck = cards.deck(deckcount=deckcount)
        self.assertEqual(len(deck.cardlist), 52*deckcount)
        deck.shuffle()
        self.assertEqual(len(deck.cardlist), 52*deckcount)
        return deck

    def test_deck(self):
        deck1 = self.create_shuffled_deck()
        deck2 = self.create_shuffled_deck()

        # deal all the cards from both decks, should be the same set of 52
        # cards
        cardset1 = set([str(x) for x in deck1.deal(count=52)])
        self.assertEqual(len(deck1.cardlist), 0)
        self.assertEqual(len(cardset1), 52)
        cardset2 = set([str(x) for x in deck2.deal(count=52)])
        self.assertEqual(len(deck2.cardlist), 0)
        self.assertEqual(len(cardset2), 52)
        self.assertEqual(cardset1, cardset2)

        # now run some tests with 8 decks
        deck3 = self.create_shuffled_deck(deckcount=8)
        for rank in cards.RANKS:
            # should be 8*4 cards of each rank
            self.assertEqual(deck3.countspecificcard(rank), 8*4)
            # should be 8 when we also specify the suit
            for suit in cards.SUITS:
                # test both the string and "card" version
                self.assertEqual(deck3.countspecificcard(rank+suit), 8)
                self.assertEqual(deck3.countspecificcard(
                    cards.card(rank+suit)), 8)

        # the cards dealt should be 8 of each dealt in the one-deck case above
        cardset3 = collections.Counter(
            [str(x) for x in deck3.deal(count=52*8)]
        )
        self.assertEqual(set(cardset3.keys()), cardset1)
        for count in cardset3.values():
            self.assertEqual(count, 8)

        # dealing should now raise a DeckEmptyError
        self.assertRaises(cards.DeckEmptyError, deck1.dealone)
        self.assertRaises(cards.DeckEmptyError, deck2.dealone)
        self.assertRaises(cards.DeckEmptyError, deck3.dealone)

        # test dealspecificcard by taking all the jacks out of a deck
        deck4 = self.create_shuffled_deck()
        jacks = set()
        for i in range(4):
            card = deck4.dealspecificcard('J')
            self.assertEqual(card.rank, 'J')
            jacks.add(str(card))
            self.assertEqual(len(jacks), i+1)
        with self.assertRaises(cards.DeckEmptyError):
            deck4.dealspecificcard('J')
        self.assertEqual(len(deck4.cardlist), 48)
        cardset4 = set([str(x) for x in deck4.deal(count=48)])
        self.assertEqual(len(cardset4), 48)
        self.assertEqual(cardset1 - cardset4, jacks)

    def test_deck_repr(self):
        deck = self.create_shuffled_deck()
        deckrep = repr(deck)
        cardstrings1 = [rank+suit for rank, suit in
                        zip(deckrep[::2], deckrep[1::2])]
        cardstrings2 = [repr(x) for x in deck.deal(count=52)]
        self.assertEqual(cardstrings1, cardstrings2)

    def test_makehand(self):
        hand = cards.makehand('6♡Q♣4♡5♢7♣2♢')
        self.assertEqual(len(hand), 6)
        self.assertEqual(hand[0].rank, '6')
        self.assertEqual(hand[0].suit, '♡')
        self.assertEqual(hand[-1].rank, '2')
        self.assertEqual(hand[-1].suit, '♢')
