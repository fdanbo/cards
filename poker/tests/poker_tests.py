import cards
import itertools
import unittest
from poker import poker


# ♡♣♢♠
class PokerTest(unittest.TestCase):
    BUILD_STRINGS = ['2♡', '4♣', '3♡', 'A♠', '5♣', '6♢', 'Q♢']
    _5CARD_STRINGS = [
        ('2♡4♡8♡3♣6♠', '8 high [86432]'),
        ('A♡5♣7♡T♠J♣', 'A high [AJT75]'),
        ('A♡5♣7♡A♠J♣', 'pair of As [AJ75]'),
        ('7♡5♣7♣T♠5♡', 'two pair, 7s and 5s [75T]'),
        ('T♡T♣7♡T♠J♣', 'three Ts [TJ7]'),
        ('2♡4♣3♡A♠5♣', '5-high straight [5]'),
        ('T♡9♣7♡8♠J♣', 'J-high straight [J]'),
        ('T♡J♣Q♡K♠A♣', 'A-high straight [A]'),
        ('T♡9♡7♡3♡J♡', 'J-high flush [JT973]'),
        ('T♡T♣7♡T♠7♣', 'full house, Ts over 7s [T7]'),
        ('T♡T♣7♢T♠T♢', 'four Ts [T7]'),
        ('T♢9♢7♢8♢J♢', 'J-high straight flush [J]')
    ]
    # we add these two cards to all of the above hands, and make sure the hand
    # is evaluated at equal or better
    _7CARD_STRINGS = ['6♢', 'Q♢']
    _7CARD_HANDS = [
        ('6♡Q♣4♡5♢7♣2♢6♣', 'pair of 6s [6Q75]'),
        ('A♢7♡5♠J♡2♡3♡7♢', 'pair of 7s [7AJ5]')
    ]

    def setUp(self):
        self.build_cards = [
            cards.card.fromstring(a) for a in PokerTest.BUILD_STRINGS
        ]
        self._5card_hands = [
            (poker.hand.fromstring(a), b)
            for a, b in PokerTest._5CARD_STRINGS
        ]
        self._7card_cards = [
            cards.card.fromstring(a) for a in PokerTest._7CARD_STRINGS
        ]
        self._7card_hands = [
            (poker.hand.fromstring(a), b)
            for a, b in PokerTest._7CARD_HANDS
        ]

    @staticmethod
    def clone_and_rotate_suit(hand):
        newhand = poker.hand()
        for card in hand.cards:
            newsuit = (card.suit + 1) % 4
            newhand.addcard(cards.card(card.rank, newsuit))
        return newhand

    @staticmethod
    def add_card_to_hand(hand):
        for rank in range(1, 14):
            for suit in range(4):
                newcard = cards.card(rank, suit)
                hand.addcard(newcard)

    def test_build_hand(self):
        hand = poker.hand()
        for i, card in enumerate(self.build_cards):
            hand.addcard(card)
            self.assertEqual(hand.get_card_count(), i+1)
            self.assertEqual(hand.is_ready(), i >= 4)

    def test_5card_rankings(self):
        for hand, rep in self._5card_hands:
            self.assertEqual(repr(hand.get_ranking()), rep)

            # rotating the suits should always give an equal hand
            rotated = self.clone_and_rotate_suit(hand)
            self.assertEqual(hand.get_ranking(), rotated.get_ranking())
            self.assertEqual(hand.get_description(), rotated.get_description())

        # compare hands with each other; later ones in the list are better than
        # earlier ones.
        for (h1, d1), (h2, d2) in itertools.combinations(self._5card_hands, 2):
            self.assertLess(h1.get_ranking(), h2.get_ranking())

    def test_7card_rankings(self):
        for h1, rep in self._5card_hands:
            h2 = h1.clone()
            for card in self._7card_cards:
                # adding a card should always make the hand the same or better
                h2.addcard(card)
                self.assertLessEqual(h1.get_ranking(), h2.get_ranking())

                # suit rotation shouldn't change anything
                h1_rotated = self.clone_and_rotate_suit(h1)
                h2_rotated = self.clone_and_rotate_suit(h2)
                self.assertEqual(h2.get_ranking(),
                                 h2_rotated.get_ranking())
                self.assertLessEqual(h1_rotated.get_ranking(),
                                     h2.get_ranking())
                self.assertLessEqual(h1.get_ranking(),
                                     h2_rotated.get_ranking())
                self.assertLessEqual(h1_rotated.get_ranking(),
                                     h2_rotated.get_ranking())

        for hand, rep in self._7card_hands:
            self.assertEqual(repr(hand.get_ranking()), rep)
            # rotating the suits should always give an equal hand
            rotated = self.clone_and_rotate_suit(hand)
            self.assertEqual(hand.get_ranking(), rotated.get_ranking())
            self.assertEqual(hand.get_description(), rotated.get_description())

        # compare hands with each other; later ones in the list are better than
        # earlier ones.
        for (h1, d1), (h2, d2) in itertools.combinations(self._7card_hands, 2):
            self.assertLess(h1.get_ranking(), h2.get_ranking())
