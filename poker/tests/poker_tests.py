import cards
import itertools
import unittest

from poker import poker


def parse_hands(pairs):
    return [(cards.Hand(h), s) for h, s in pairs]


# ♡♣♢♠
class PokerTest(unittest.TestCase):
    _5CARD_HANDS = parse_hands([
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
    ])
    _7CARD_HANDS = parse_hands([
        ('A♣K♣7♣8♢J♠3♣2♠', 'A high [AKJ87]'),
        ('6♣J♡A♡7♢5♡T♠K♣', 'A high [AKJT7]'),
        ('8♣A♣5♢7♠8♢9♣3♢', 'pair of 8s [8A97]'),
        ('9♣J♣6♠8♠A♠T♢J♠', 'pair of Js [JAT9]'),
        ('8♠8♡Q♢7♢A♡7♡4♢', 'two pair, 8s and 7s [87A]'),
        ('K♢7♣7♠8♣Q♡T♢K♠', 'two pair, Ks and 7s [K7Q]'),
        ('2♢J♣7♡Q♢2♣8♣2♡', 'three 2s [2QJ]'),
        ('2♢7♢2♠2♡T♡K♢3♠', 'three 2s [2KT]'),
        ('5♢2♠3♡4♣3♢A♠6♢', '6-high straight [6]'),
        ('7♡T♠9♠8♡8♠J♠Q♢', 'Q-high straight [Q]'),
        ('T♣J♢9♠8♢4♢A♢2♢', 'A-high flush [AJ842]'),
        ('8♢4♣6♣A♣K♣T♣5♢', 'A-high flush [AKT64]'),
        ('9♣3♠9♠8♠9♡T♢3♣', 'full house, 9s over 3s [93]'),
        ('Q♠Q♢Q♣9♢A♢4♡A♣', 'full house, Qs over As [QA]'),
        ('9♣J♠T♣9♡9♢6♠9♠', 'four 9s [9J]'),
        ('T♣T♠3♠T♢T♡5♢K♣', 'four Ts [TK]'),
        ('4♣6♠A♢5♠2♠3♠4♠', '6-high straight flush [6]'),
        ('T♣6♣6♢8♢8♣9♣7♣', 'T-high straight flush [T]')
    ])

    def clone_and_shuffle(self, hand):
        newhand = cards.Hand()

        # rotate suits
        for card in hand:
            newsuit = cards.SUITS[(cards.SUITS.index(card.suit) + 1) % 4]
            newhand.append(cards.Card(card.rank, newsuit))

        newhand.shuffle()

        # ranks should be the same
        s1 = ''.join(card.rank for card in
                     sorted(hand[:], key=cards.RankFirstOrderings.AceLow))
        s2 = ''.join(card.rank for card in
                     sorted(newhand[:], key=cards.RankFirstOrderings.AceLow))
        self.assertEqual(s1, s2)
        return newhand

    def test_5card_rankings(self):
        for hand, rep in self._5CARD_HANDS:
            self.assertEqual(repr(poker.get_5_card_ranking(hand)), rep)

            # rotating the suits and shifting the cards around should always
            # give an equal hand
            shuffled = self.clone_and_shuffle(hand)
            r1 = poker.get_5_card_ranking(hand)
            r2 = poker.get_5_card_ranking(shuffled)
            self.assertEqual(r1, r2)
            self.assertEqual(repr(r1), repr(r2))

        # compare hands with each other; later ones in the list are better than
        # earlier ones.
        for (h1, d1), (h2, d2) in itertools.combinations(self._5CARD_HANDS, 2):
            self.assertLess(poker.get_5_card_ranking(h1),
                            poker.get_5_card_ranking(h2))

    def test_7card_rankings(self):
        for hand, rep in self._7CARD_HANDS:
            self.assertEqual(repr(poker.get_7_card_ranking(hand)), rep)
            # rotating the suits should always give an equal hand
            shuffled = self.clone_and_shuffle(hand)
            r1 = poker.get_7_card_ranking(hand)
            r2 = poker.get_7_card_ranking(shuffled)
            self.assertEqual(r1, r2)
            self.assertEqual(repr(r1), repr(r2))

        # compare hands with each other; later ones in the list are better than
        # earlier ones.
        for (h1, d1), (h2, d2) in itertools.combinations(
                self._7CARD_HANDS, 2
        ):
            self.assertLess(poker.get_7_card_ranking(h1),
                            poker.get_7_card_ranking(h2))
