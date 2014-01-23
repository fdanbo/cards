# encoding: utf-8

import cards
import collections
import unittest


class CardsTest(unittest.TestCase):
    def test_card(self):
        c1 = cards.card(1, 0)
        self.assertEqual(c1.rank, 1)
        self.assertEqual(c1.suit, 0)
        self.assertEqual(str(c1), 'A♡')

        c2 = cards.card(13, 3)
        self.assertEqual(c2.rank, 13)
        self.assertEqual(c2.suit, 3)
        self.assertEqual(str(c2), 'K♠')

    def create_shuffled_deck(self, deckCount=1):
        deck = cards.deck(deckCount=deckCount)
        self.assertEqual(deck.getCardCount(), 52*deckCount)
        deck.shuffle()
        self.assertEqual(deck.getCardCount(), 52*deckCount)
        return deck

    def test_deck(self):
        deck1 = self.create_shuffled_deck()
        deck2 = self.create_shuffled_deck()

        # deal all the cards from both decks, should be the same set of 52
        # cards
        cardset1 = set([str(x) for x in deck1.deal(count=52)])
        self.assertEqual(deck1.getCardCount(), 0)
        self.assertEqual(len(cardset1), 52)
        cardset2 = set([str(x) for x in deck2.deal(count=52)])
        self.assertEqual(deck2.getCardCount(), 0)
        self.assertEqual(len(cardset2), 52)
        self.assertEqual(cardset1, cardset2)

        # now run some tests with 8 decks
        deck3 = self.create_shuffled_deck(deckCount=8)
        for rank in range(1, 14):
            # should be 8*4 cards of each rank
            self.assertEqual(deck3.getCardsLeft(rank), 8*4)

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
            card = deck4.dealspecificcard(11)  # deal a jack
            self.assertEqual(card.rank, 11)
            jacks.add(str(card))
            self.assertEqual(len(jacks), i+1)
        self.assertRaises(cards.DeckEmptyError,
                          lambda: deck4.dealspecificcard(11))
        self.assertEqual(deck4.getCardCount(), 48)
        cardset4 = set([str(x) for x in deck4.deal(count=48)])
        self.assertEqual(len(cardset4), 48)
        self.assertEqual(cardset1 - cardset4, jacks)

    def test_deck_repr(self):
        deck = self.create_shuffled_deck()
        cardstrings1 = repr(deck).split(' ')
        cardstrings2 = [repr(x) for x in deck.deal(count=52)]
        self.assertEqual(cardstrings1, cardstrings2)
