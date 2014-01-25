
import cards
import collections
import functools
import itertools


def rank_to_string(r):
    if r == 14:
        r = 1
    return cards.card.RANKS[r-1]


@functools.total_ordering
class ranking():
    high_card = 1
    one_pair = 2
    two_pair = 3
    three_of_a_kind = 4
    straight = 5
    flush = 6
    full_house = 7
    four_of_a_kind = 8
    straight_flush = 9

    # ranking is one of the constants above.  high_cards is a list of integers
    # that should be considered to further rank the hand, in that order.
    # because they're integers, aces should come in as 14 -- and if you have a
    # 5-high straight, only a 5 should appear.
    def __init__(self, ranking, high_cards):
        self.ranking = ranking
        self.high_cards = list(high_cards)

    def __repr__(self):
        desc = self.get_description()
        return '{} [{}]'.format(desc, ''.join(
            [rank_to_string(x) for x in self.high_cards]))

    def __eq__(self, rhs):
        return (self.ranking == rhs.ranking and
                self.high_cards == rhs.high_cards)

    def __lt__(self, rhs):
        return (self.ranking < rhs.ranking or
                self.high_cards < rhs.high_cards)

    def get_description(self):
        h1 = rank_to_string(self.high_cards[0])
        if len(self.high_cards) > 1:
            h2 = rank_to_string(self.high_cards[1])
        if self.ranking == ranking.high_card:
            return '{} high'.format(h1)
        if self.ranking == ranking.one_pair:
            return 'pair of {}s'.format(h1)
        if self.ranking == ranking.two_pair:
            return 'two pair, {}s and {}s'.format(h1, h2)
        if self.ranking == ranking.three_of_a_kind:
            return 'three {}s'.format(h1)
        if self.ranking == ranking.straight:
            return '{}-high straight'.format(h1)
        if self.ranking == ranking.flush:
            return '{}-high flush'.format(h1)
        if self.ranking == ranking.full_house:
            return 'full house, {}s over {}s'.format(h1, h2)
        if self.ranking == ranking.four_of_a_kind:
            return 'four {}s'.format(h1)
        if self.ranking == ranking.straight_flush:
            return '{}-high straight flush'.format(h1)


def ace_high_rank(card_or_rank):
    if hasattr(card_or_rank, 'rank'):
        rank = card_or_rank.rank
    else:
        rank = card_or_rank
    return 14 if rank == 1 else rank


def is_consecutive(card1, card2):
    # there are a bunch of special cases for aces, because their rank is
    # '1' but they're sorted high.
    if card1.rank == 1:
        return False
    if card2.rank == 1:
        # since the ace is sorted high, I'm counting 2345A as a straight
        return card1.rank == 13 or card1.rank == 5
    else:
        return card2.rank == (card1.rank+1)


def straight_high_card(sorted_cards):
    # assert that the cards in fact form a straight
    seq = ''.join([cards.card.RANKS[c.rank-1] for c in sorted_cards])
    assert seq in ('2345A', '23456', '34567', '45678', '56789',
                   '6789T', '789TJ', '89TJQ', '9TJQK', 'TJQKA')

    # for straights, only the high card matters for relative ranking.  we
    # have to special case A2345 because it is sorted as 2345A.
    highcard = sorted_cards[-1].rank
    if highcard == 1:
        if sorted_cards[-2].rank == 5:
            # 2345A
            highcard = 5
        else:
            # TJQKA
            highcard = 14

    return highcard


def get_5_card_ranking(cards):
    assert len(cards) == 5

    # sort the cards by rank, with ace being high
    cards = sorted(cards, key=ace_high_rank)

    # iterate over the pairs of cards searching for sequences and matching
    # suits
    is_flush = True
    is_straight = True
    for c1, c2 in zip(cards[:-1], cards[1:]):
        if c1.suit != c2.suit:
            is_flush = False
        if not is_consecutive(c1, c2):
            is_straight = False

    # CHECK FOR STRAIGHT FLUSH
    if is_flush and is_straight:
        highcard = straight_high_card(cards)
        return ranking(ranking.straight_flush, [highcard])

    # count number of cards of each rank
    counts = collections.Counter()
    for c1 in cards:
        counts[c1.rank] += 1

    sorted_counts = counts.most_common()
    most_rank, most_count = sorted_counts[0]
    assert most_count < 5

    # CHECK FOR FOUR OF A KIND
    if most_count == 4:
        # we have a four of a kind.  we know 'rank' is the rank; we just
        # gotta figure out the kicker.
        highcard = ace_high_rank(most_rank)

        assert len(sorted_counts) == 2
        next_rank, next_count = sorted_counts[1]
        assert next_count == 1
        kicker = ace_high_rank(next_rank)

        return ranking(ranking.four_of_a_kind, [highcard, kicker])

    # CHECK FOR FULL HOUSE
    if most_count == 3 and len(sorted_counts) == 2:
        highcard = ace_high_rank(most_rank)

        next_rank, next_count = sorted_counts[1]
        assert next_count == 2
        kicker = ace_high_rank(next_rank)

        return ranking(ranking.full_house, [highcard, kicker])

    # CHECK FOR FLUSH
    if is_flush:
        highcards = reversed([ace_high_rank(c) for c in cards])
        return ranking(ranking.flush, highcards)

    # CHECK FOR STRAIGHT
    if is_straight:
        highcard = straight_high_card(cards)
        return ranking(ranking.straight, [highcard])

    # CHECK FOR THREE-OF-A-KIND
    if most_count == 3:
        highcard = ace_high_rank(most_rank)
        kickers = sorted([ace_high_rank(r)
                          for r, c in sorted_counts[1:]], reverse=True)
        return ranking(ranking.three_of_a_kind, [highcard] + kickers)

    # CHECK FOR ONE OR TWO PAIRS
    if most_count == 2:
        next_rank, next_count = sorted_counts[1]
        if next_count == 2:
            # two pair
            assert len(sorted_counts) == 3
            highcards = sorted([ace_high_rank(most_rank),
                                ace_high_rank(next_rank)], reverse=True)
            kicker_rank, kicker_count = sorted_counts[2]
            assert kicker_count == 1
            kicker = ace_high_rank(kicker_rank)
            return ranking(ranking.two_pair, highcards + [kicker])
        else:
            # one pair
            assert len(sorted_counts) == 4
            highcard = ace_high_rank(most_rank)
            kickers = sorted([ace_high_rank(r) for r, c in sorted_counts[1:]],
                             reverse=True)
            return ranking(ranking.one_pair, [highcard] + kickers)

    # otherwise, we have a high card
    assert len(sorted_counts) == 5
    return ranking(ranking.high_card,
                   reversed([ace_high_rank(c) for c in cards]))


class hand():
    def __init__(self):
        self.cards = []

    def __repr__(self):
        return '[' + ''.join(repr(card) for card in self.cards) + ']'

    @staticmethod
    def fromstring(s):
        result = hand()
        for rank, suit in zip(s[0::2], s[1::2]):
            result.addcard(cards.card.fromstring(rank+suit))
        return result

    def clone(self):
        result = hand()
        result.cards = [card.clone() for card in self.cards]
        return result

    def addcard(self, card):
        self.cards.append(card)

    def is_ready(self):
        return len(self.cards) >= 5

    def get_card_count(self):
        return len(self.cards)

    def get_ranking(self):
        assert self.is_ready()
        best_so_far = None
        for _5cards in itertools.combinations(self.cards, 5):
            ranking = get_5_card_ranking(_5cards)
            if best_so_far is None or (ranking > best_so_far):
                best_so_far = ranking
        return best_so_far

    def get_description(self):
        return self.get_ranking().get_description()
