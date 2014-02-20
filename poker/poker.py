
import cards
import collections
import functools
import itertools


@functools.total_ordering
class Ranking():
    high_card = 1
    one_pair = 2
    two_pair = 3
    three_of_a_kind = 4
    straight = 5
    flush = 6
    full_house = 7
    four_of_a_kind = 8
    straight_flush = 9

    # ranking is one of the constants above, and high_cards is an iterable of
    # ranks of cards to compare, in that order.  eg for JJ44K high_cards is
    # J4K.
    def __init__(self, ranking, high_cards):
        self.ranking = ranking
        self.high_cards = list(high_cards)

    def __eq__(self, rhs):
        return (self.ranking == rhs.ranking and
                self.high_cards == rhs.high_cards)

    def __lt__(self, rhs):
        if self.ranking < rhs.ranking:
            return True
        elif self.ranking == rhs.ranking:
            # convert the rank strings into a 2-14 integer for ordering.  We
            # didn't have to do this above, since equality works perfectly well
            # for the rank string.
            hc1 = [cards.AceHighIndex(r) for r in self.high_cards]
            hc2 = [cards.AceHighIndex(r) for r in rhs.high_cards]
            return hc1 < hc2
        else:
            return False

    def __repr__(self):
        if self.ranking == Ranking.high_card:
            desc = '{} high'.format(*self.high_cards)
        elif self.ranking == Ranking.one_pair:
            desc = 'pair of {}s'.format(*self.high_cards)
        elif self.ranking == Ranking.two_pair:
            desc = 'two pair, {}s and {}s'.format(*self.high_cards)
        elif self.ranking == Ranking.three_of_a_kind:
            desc = 'three {}s'.format(*self.high_cards)
        elif self.ranking == Ranking.straight:
            desc = '{}-high straight'.format(*self.high_cards)
        elif self.ranking == Ranking.flush:
            desc = '{}-high flush'.format(*self.high_cards)
        elif self.ranking == Ranking.full_house:
            desc = 'full house, {}s over {}s'.format(*self.high_cards)
        elif self.ranking == Ranking.four_of_a_kind:
            desc = 'four {}s'.format(*self.high_cards)
        elif self.ranking == Ranking.straight_flush:
            desc = '{}-high straight flush'.format(*self.high_cards)

        return '{} [{}]'.format(desc, ''.join(self.high_cards))


STRAIGHT_STRINGS = frozenset(['A2345', '23456', '34567', '45678', '56789',
                              '6789T', '789TJ', '89TJQ', '9TJQK', 'TJQKA'])


def get_5_card_ranking(hand):
    assert len(hand) == 5

    # sort the cards by rank, with ace being high
    hand.sort(key=cards.RankFirstOrderings.AceHigh)
    rankstring = ''.join(c.rank for c in hand)

    # special case: if we have 2345A, reorder to A2345
    if rankstring == '2345A':
        hand.insert(0, hand.pop(-1))
        rankstring = ''.join(c.rank for c in hand)
        assert rankstring == 'A2345'

    is_flush = len(set(c.suit for c in hand)) <= 1
    is_straight = rankstring in STRAIGHT_STRINGS

    # CHECK FOR STRAIGHT FLUSH
    if is_flush and is_straight:
        return Ranking(Ranking.straight_flush, [hand[-1].rank])

    # count number of cards of each rank
    counts = collections.Counter(c.rank for c in hand)

    sorted_counts = counts.most_common()
    most_rank, most_count = sorted_counts[0]
    assert most_count < 5

    # for the purpose of ranking, we sort in reverse order, so that kickers
    # compare as something like 'AT94' not '49TA'.  Note that we never call
    # sorted_by_rank in the case of a straight, since aces can be low in that
    # case -- this is just for kickers for pairs and such.
    def sorted_by_rank(l):
        return sorted(l, key=cards.AceHighIndex, reverse=True)

    # CHECK FOR FOUR OF A KIND
    if most_count == 4:
        # we have a four of a kind
        assert len(sorted_counts) == 2
        next_rank, next_count = sorted_counts[1]
        assert next_count == 1
        return Ranking(Ranking.four_of_a_kind, [most_rank, next_rank])

    # CHECK FOR FULL HOUSE
    if most_count == 3 and len(sorted_counts) == 2:
        next_rank, next_count = sorted_counts[1]
        assert next_count == 2
        return Ranking(Ranking.full_house, [most_rank, next_rank])

    # CHECK FOR FLUSH
    if is_flush:
        ranks = reversed([c.rank for c in hand])
        return Ranking(Ranking.flush, ranks)

    # CHECK FOR STRAIGHT
    if is_straight:
        return Ranking(Ranking.straight, [hand[-1].rank])

    # CHECK FOR THREE-OF-A-KIND
    if most_count == 3:
        kickers = sorted_by_rank(r for r, c in sorted_counts[1:])
        assert len(kickers) == 2
        return Ranking(Ranking.three_of_a_kind, [most_rank] + kickers)

    # CHECK FOR ONE OR TWO PAIRS
    if most_count == 2:
        next_rank, next_count = sorted_counts[1]
        if next_count == 2:
            # two pair
            assert len(sorted_counts) == 3
            pair_cards = sorted_by_rank([most_rank, next_rank])
            kicker_rank, kicker_count = sorted_counts[2]
            assert kicker_count == 1
            return Ranking(Ranking.two_pair, pair_cards + [kicker_rank])
        else:
            # one pair
            assert len(sorted_counts) == 4
            kickers = sorted_by_rank(r for r, c in sorted_counts[1:])
            return Ranking(Ranking.one_pair, [most_rank] + kickers)

    # otherwise, we have a high card
    assert len(sorted_counts) == 5
    return Ranking(Ranking.high_card,
                   sorted_by_rank(c.rank for c in hand))


def get_7_card_ranking(hand):
    # TODO: there's a much more efficient way to do this than checking every
    # possible combination, particularly if there are more than 7 cards.  but
    # this works well enough, I might never change it.
    best_so_far = None
    for _5cards in itertools.combinations(hand[:], 5):
        _5card_hand = cards.Hand(_5cards)
        ranking = get_5_card_ranking(_5card_hand)
        if best_so_far is None or (ranking > best_so_far):
            best_so_far = ranking
    return best_so_far
