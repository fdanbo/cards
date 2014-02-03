
import cards
import collections
import copy
import random
import unittest


class CardTest(unittest.TestCase):
    def test_init(self):
        card = cards.Card('K♠')
        self.assertEqual(card.rank, 'K')
        self.assertEqual(card.suit, '♠')
        self.assertEqual(repr(card), 'K♠')
        self.assertEqual(str(card), 'K♠')

        with self.assertRaises(ValueError):
            # must specify both rank and suit
            card = cards.Card('A')

        with self.assertRaises(ValueError):
            # cannot specify both string and rank/suit
            card = cards.Card('A♡', suit='♡')

        with self.assertRaises(ValueError):
            # rank must be valid
            card = cards.Card('AKQ', '♡')

        with self.assertRaises(ValueError):
            # another invalid rank case
            card = cards.Card('a', '♡')

        with self.assertRaises(ValueError):
            # suit must be valid
            card = cards.Card('K', '♡♣')

        with self.assertRaises(ValueError):
            # another invalid suit case
            card = cards.Card('K', 'h')

    def test_immutable(self):
        card = cards.Card('A♡')

        with self.assertRaises(AttributeError):
            card.rank = 'K'

        with self.assertRaises(AttributeError):
            card.suit = '♣'

    def test_eq(self):
        card = cards.Card('A♡')
        rankmatches = cards.Card('A♣')
        suitmatches = cards.Card('7♡')
        neithermatch = cards.Card('7♣')
        bothmatch = cards.Card('A♡')

        self.assertEqual(card, card)
        self.assertNotEqual(card, rankmatches)
        self.assertNotEqual(card, suitmatches)
        self.assertNotEqual(card, neithermatch)
        self.assertEqual(card, bothmatch)

    def test_hash(self):
        cardlist = [cards.Card(rank, suit)
                    for i in range(3)
                    for suit in cards.SUITS
                    for rank in cards.RANKS]
        random.shuffle(cardlist)
        self.assertEqual(len(cardlist), 52*3)
        cardset = set(cardlist)
        self.assertEqual(len(cardset), 52)

    def test_orderings(self):
        a1 = cards.Card('A♡')
        a2 = cards.Card('A♣')
        t1 = cards.Card('T♣')
        t2 = cards.Card('T♡')
        cardlist = [a1, t1, a2, t2]

        def s(key):
            return list(sorted(cardlist, key=key))

        self.assertEqual(s(cards.RankFirstOrderings.AceHigh), [t2, t1, a1, a2])
        self.assertEqual(s(cards.RankFirstOrderings.AceLow), [a1, a2, t2, t1])
        self.assertEqual(s(cards.SuitFirstOrderings.AceHigh), [t2, a1, t1, a2])
        self.assertEqual(s(cards.SuitFirstOrderings.AceLow), [a1, t2, a2, t1])

        self.assertEqual(cards.AceHighIndex('A'), 14)
        self.assertEqual(cards.AceLowIndex('A'), 1)
        for i, r in enumerate(cards.RANKS[1:], 2):
            self.assertEqual(cards.AceHighIndex(r), i)
            self.assertEqual(cards.AceLowIndex(r), i)


class HandTest(unittest.TestCase):

    def test_init(self):
        for hand in [cards.Hand('6♡Q♣4♡5♢7♣2♢'),
                     cards.Hand([cards.Card('6♡'), cards.Card('Q♣'),
                                 cards.Card('4♡'), cards.Card('5♢'),
                                 cards.Card('7♣'), cards.Card('2♢')])]:
            self.assertEqual(len(hand), 6)
            self.assertEqual(hand[0], cards.Card('6♡'))
            self.assertEqual(hand[-1], cards.Card('2♢'))
            self.assertEqual(repr(hand), '6♡Q♣4♡5♢7♣2♢')
            self.assertEqual(str(hand), '6♡Q♣4♡5♢7♣2♢')
            with self.assertRaises(IndexError):
                hand[6]

    def test_sort_shuffle(self):
        hands = [cards.Hand('6♡Q♣4♡5♢7♣2♢') for i in range(5)]

        hands[1].sort(key=cards.RankFirstOrderings.AceHigh)
        hands[2].sort(key=cards.SuitFirstOrderings.AceLow)
        hands[3].shuffle()
        hands[4].shuffle()

        for hand in hands:
            self.assertEqual(len(hand), 6)

        cardsets = [set(hand[:]) for hand in hands]
        for i in range(4):
            self.assertEqual(cardsets[i], cardsets[i+1])

    def test_copy(self):
        h1 = cards.Hand('6♡Q♣4♡5♢7♣2♢')
        h2 = cards.Hand('6♡Q♣4♡5♢7♣2♢')
        h3 = copy.copy(h1)
        h4 = copy.deepcopy(h1)
        self.assertEqual(h1[:], h2[:])
        self.assertEqual(h1[:], h3[:])
        self.assertEqual(h1[:], h4[:])

        h2.append(cards.Card('K♠'))
        h3.pop()
        h4.sort(key=cards.RankFirstOrderings.AceHigh)
        self.assertNotEqual(h1[:], h2[:])
        self.assertNotEqual(h1[:], h3[:])
        self.assertNotEqual(h1[:], h4[:])

    def test_pop(self):
        hand = cards.Hand('6♡Q♣4♡5♢7♣2♢')
        self.assertEqual(hand.pop(), cards.Card('6♡'))
        self.assertEqual(hand.pop(), cards.Card('Q♣'))
        self.assertEqual(hand.pop(2), cards.Card('7♣'))
        self.assertEqual(len(hand), 3)

        hand = cards.Hand('6♡Q♣4♡5♢7♣2♢')
        self.assertEqual(hand.popn(0), [])
        self.assertEqual(hand.popn(1), [cards.Card('6♡')])
        self.assertEqual(hand.popn(2), [cards.Card('Q♣'), cards.Card('4♡')])
        self.assertEqual(len(hand), 3)

    def test_setitem(self):
        hand = cards.Hand('6♡Q♣4♡5♢7♣2♢')

        hand[0] = cards.Card('K♠')
        self.assertEqual(repr(hand), 'K♠Q♣4♡5♢7♣2♢')

        hand[-1] = cards.Card('6♡')
        self.assertEqual(repr(hand), 'K♠Q♣4♡5♢7♣6♡')

        cardlist = cards.Hand('T♠J♡8♠A♢')[:]
        hand[1:3] = cardlist
        self.assertEqual(repr(hand), 'K♠T♠J♡8♠A♢5♢7♣6♡')

    def test_iter(self):
        hand = cards.Hand('6♡Q♣4♡5♢7♣2♢')
        cardlist = hand[:]
        for i, card in enumerate(hand):
            self.assertEqual(card, cardlist[i])

    def test_popcard(self):
        hand = cards.Hand('6♡Q♣4♡5♢7♣2♢Q♢Q♡')
        card = hand.popcard(rank='5')
        self.assertEqual(repr(card), '5♢')
        self.assertEqual(len(hand), 7)
        self.assertEqual(repr(hand), '6♡Q♣4♡7♣2♢Q♢Q♡')

        card = hand.popcard(suit='♣')
        self.assertEqual(repr(card), 'Q♣')
        self.assertEqual(len(hand), 6)
        self.assertEqual(repr(hand), '6♡4♡7♣2♢Q♢Q♡')

        card = hand.popcard(rank='Q', suit='♡')
        self.assertEqual(repr(card), 'Q♡')
        self.assertEqual(len(hand), 5)
        self.assertEqual(repr(hand), '6♡4♡7♣2♢Q♢')

        with self.assertRaises(cards.CardNotFoundError):
            hand.popcard(rank='Q', suit='♡')

    def test_countcards(self):
        hand = cards.Hand('6♡Q♣4♡5♢7♣2♢Q♢Q♡')
        self.assertEqual(hand.countcards(rank='9'), 0)
        self.assertEqual(hand.countcards(rank='Q'), 3)
        self.assertEqual(hand.countcards(rank='Q', suit='♢'), 1)
        self.assertEqual(hand.countcards(suit='♢'), 3)


class TestDeck(unittest.TestCase):
    def setUp(self):
        deck = cards.Deck(shuffle=False)
        self.all_cards_set = set(deck[:])

    def test_deck(self):
        # test with various numbers of decks
        for deckcount in [1, 2, 6, 8, 20]:
            deck = cards.Deck(deckcount=deckcount)
            self.assertEqual(len(deck), 52*deckcount)
            for rank in cards.RANKS:
                self.assertEqual(deck.countcards(rank=rank), 4*deckcount)
                for suit in cards.SUITS:
                    self.assertEqual(deck.countcards(rank=rank, suit=suit),
                                     deckcount)
            for suit in cards.SUITS:
                self.assertEqual(deck.countcards(suit=suit), 13*deckcount)

            counter = collections.Counter(x for x in deck[:])
            self.assertEqual(counter.keys(), self.all_cards_set)
            for count in counter.values():
                self.assertEqual(count, deckcount)

    def test_deal(self):
        deck = cards.Deck(shuffle=False)
        card = deck.deal()
        self.assertEqual(len(deck), 51)
        self.assertEqual(repr(card), 'A♡')

        cardlist = deck.dealn(12)
        self.assertEqual(len(deck), 39)
        self.assertEqual(''.join(repr(c) for c in cardlist),
                         '2♡3♡4♡5♡6♡7♡8♡9♡T♡J♡Q♡K♡')

        # dealn() deals as many as it can if count>length
        cardlist = deck.dealn(40)
        self.assertEqual(len(cardlist), 39)
        self.assertEqual(len(deck), 0)
        self.assertEqual(deck.dealn(1), [])
        with self.assertRaises(IndexError):
            deck.deal()

    def test_repr(self):
        deck = cards.Deck()
        deckrep = repr(deck)
        cardstrings1 = [rank+suit for rank, suit in
                        zip(deckrep[::2], deckrep[1::2])]
        cardstrings2 = [repr(x) for x in deck[:]]
        self.assertEqual(cardstrings1, cardstrings2)
