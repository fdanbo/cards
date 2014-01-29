import cards
import itertools
import unittest
from poker import poker


# ♡♣♢♠
class PokerTest(unittest.TestCase):
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
    _7CARD_STRINGS = [
        ('6♡Q♣4♡5♢7♣2♢6♣', 'pair of 6s [6Q75]'),
        ('A♢7♡5♠J♡2♡3♡7♢', 'pair of 7s [7AJ5]')
    ]

    @staticmethod
    def clone_and_rotate_suit(hand):
        newhand = []
        for card in hand:
            newsuit = cards.SUITS[(cards.SUITS.index(card.suit) + 1) % 4]
            newhand.append(cards.card(card.rank+newsuit))
        return newhand

    def test_5card_rankings(self):
        for handstring, rep in self._5CARD_STRINGS:
            hand = cards.makehand(handstring)
            self.assertEqual(repr(poker.get_5_card_ranking(hand)), rep)

            # rotating the suits should always give an equal hand
            rotated = self.clone_and_rotate_suit(hand)
            r1 = poker.get_5_card_ranking(hand)
            r2 = poker.get_5_card_ranking(rotated)
            self.assertEqual(r1, r2)
            self.assertEqual(repr(r1), repr(r2))

        # compare hands with each other; later ones in the list are better than
        # earlier ones.
        for (s1, d1), (s2, d2) in itertools.combinations(
                self._5CARD_STRINGS, 2
        ):
            self.assertLess(poker.get_5_card_ranking(cards.makehand(s1)),
                            poker.get_5_card_ranking(cards.makehand(s2)))

    def test_7card_rankings(self):
        for s1, rep in self._5CARD_STRINGS:
            h1 = cards.makehand(s1)
            h2 = cards.makehand(s1)

            # deal two cards out of a deck; the results should always make an
            # equal or better hand.
            deck = cards.deck()
            deck.shuffle()
            for card in deck.deal(2):
                # adding a card should always make the hand the same or better
                h2.append(card)
                self.assertLessEqual(poker.get_7_card_ranking(h1),
                                     poker.get_7_card_ranking(h2))

                # suit rotation shouldn't change anything
                h1_rotated = self.clone_and_rotate_suit(h1)
                h2_rotated = self.clone_and_rotate_suit(h2)
                self.assertEqual(poker.get_7_card_ranking(h2),
                                 poker.get_7_card_ranking(h2_rotated))
                self.assertLessEqual(poker.get_7_card_ranking(h1_rotated),
                                     poker.get_7_card_ranking(h2))
                self.assertLessEqual(poker.get_7_card_ranking(h1),
                                     poker.get_7_card_ranking(h2_rotated))
                self.assertLessEqual(poker.get_7_card_ranking(h1_rotated),
                                     poker.get_7_card_ranking(h2_rotated))

        for s, rep in self._7CARD_STRINGS:
            hand = cards.makehand(s)
            self.assertEqual(repr(poker.get_7_card_ranking(hand)), rep)
            # rotating the suits should always give an equal hand
            rotated = self.clone_and_rotate_suit(hand)
            r1 = poker.get_7_card_ranking(hand)
            r2 = poker.get_7_card_ranking(rotated)
            self.assertEqual(r1, r2)
            self.assertEqual(repr(r1), repr(r2))

        # compare hands with each other; later ones in the list are better than
        # earlier ones.
        for (s1, d1), (s2, d2) in itertools.combinations(
                self._7CARD_STRINGS, 2
        ):
            h1 = cards.makehand(s1)
            h2 = cards.makehand(s2)
            self.assertLess(poker.get_7_card_ranking(h1),
                            poker.get_7_card_ranking(h2))
