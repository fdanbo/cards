
import cards
import collections
import functools
import itertools


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

    # ranking is one of the constants above.  high_card_indices is a list of
    # integers that should be considered to further rank the hand, in that
    # order.  because they're integers, aces should come in as 14 -- and if you
    # have a 5-high straight, only a 5 should appear.
    def __init__(self, ranking, high_card_indices):
        self.ranking = ranking
        self.high_card_indices = list(high_card_indices)

    def __eq__(self, rhs):
        return (self.ranking == rhs.ranking and
                self.high_card_indices == rhs.high_card_indices)

    def __lt__(self, rhs):
        if self.ranking < rhs.ranking:
            return True
        elif self.ranking == rhs.ranking:
            return self.high_card_indices < rhs.high_card_indices
        else:
            return False

    def __repr__(self):
        ranks = [cards.index_to_rank(i) for i in self.high_card_indices]

        if self.ranking == ranking.high_card:
            desc = '{} high'.format(ranks[0])
        if self.ranking == ranking.one_pair:
            desc = 'pair of {}s'.format(ranks[0])
        if self.ranking == ranking.two_pair:
            desc = 'two pair, {}s and {}s'.format(ranks[0], ranks[1])
        if self.ranking == ranking.three_of_a_kind:
            desc = 'three {}s'.format(ranks[0])
        if self.ranking == ranking.straight:
            desc = '{}-high straight'.format(ranks[0])
        if self.ranking == ranking.flush:
            desc = '{}-high flush'.format(ranks[0])
        if self.ranking == ranking.full_house:
            desc = 'full house, {}s over {}s'.format(ranks[0], ranks[1])
        if self.ranking == ranking.four_of_a_kind:
            desc = 'four {}s'.format(ranks[0])
        if self.ranking == ranking.straight_flush:
            desc = '{}-high straight flush'.format(ranks[0])

        return '{} [{}]'.format(desc, ''.join(
            [cards.index_to_rank(i) for i in self.high_card_indices]))


STRAIGHT_RANKSTRINGS = frozenset(['A2345', '23456', '34567', '45678', '56789',
                                  '6789T', '789TJ', '89TJQ', '9TJQK', 'TJQKA'])


def sort_by_index(ranks):
    return sorted([cards.ace_high_index(r) for r in ranks],
                  reverse=True)


def get_5_card_ranking(cardlist):
    assert len(cardlist) == 5

    # sort the cards by rank, with ace being high
    cardlist = sorted(cardlist, key=lambda c: c.ace_high_index())
    rankstring = ''.join(c.rank for c in cardlist)

    # special case: if we have 2345A, reorder to A2345
    if rankstring == '2345A':
        cardlist.insert(0, cardlist.pop())
        rankstring = 'A2345'

    is_flush = len(set(c.suit for c in cardlist)) <= 1
    is_straight = rankstring in STRAIGHT_RANKSTRINGS

    # CHECK FOR STRAIGHT FLUSH
    if is_flush and is_straight:
        highindex = cardlist[-1].ace_high_index()
        return ranking(ranking.straight_flush, [highindex])

    # count number of cards of each rank
    counts = collections.Counter(c.rank for c in cardlist)

    sorted_counts = counts.most_common()
    most_rank, most_count = sorted_counts[0]
    assert most_count < 5

    # CHECK FOR FOUR OF A KIND
    if most_count == 4:
        # we have a four of a kind
        highindex = cards.ace_high_index(most_rank)
        assert len(sorted_counts) == 2
        next_rank, next_count = sorted_counts[1]
        assert next_count == 1
        kicker = cards.ace_high_index(next_rank)
        return ranking(ranking.four_of_a_kind, [highindex, kicker])

    # CHECK FOR FULL HOUSE
    if most_count == 3 and len(sorted_counts) == 2:
        highindex = cards.ace_high_index(most_rank)
        next_rank, next_count = sorted_counts[1]
        assert next_count == 2
        kicker = cards.ace_high_index(next_rank)
        return ranking(ranking.full_house, [highindex, kicker])

    # CHECK FOR FLUSH
    if is_flush:
        highindices = reversed([c.ace_high_index() for c in cardlist])
        return ranking(ranking.flush, highindices)

    # CHECK FOR STRAIGHT
    if is_straight:
        highindex = cardlist[-1].ace_high_index()
        return ranking(ranking.straight, [highindex])

    # CHECK FOR THREE-OF-A-KIND
    if most_count == 3:
        highindex = cards.ace_high_index(most_rank)
        kickers = sort_by_index(r for r, c in sorted_counts[1:])
        assert len(kickers) == 2
        return ranking(ranking.three_of_a_kind, [highindex] + kickers)

    # CHECK FOR ONE OR TWO PAIRS
    if most_count == 2:
        next_rank, next_count = sorted_counts[1]
        if next_count == 2:
            # two pair
            assert len(sorted_counts) == 3
            highindices = sort_by_index([most_rank, next_rank])
            kicker_rank, kicker_count = sorted_counts[2]
            assert kicker_count == 1
            kicker = cards.ace_high_index(kicker_rank)
            return ranking(ranking.two_pair, highindices + [kicker])
        else:
            # one pair
            assert len(sorted_counts) == 4
            highindex = cards.ace_high_index(most_rank)
            kickers = sort_by_index(r for r, c in sorted_counts[1:])
            return ranking(ranking.one_pair, [highindex] + kickers)

    # otherwise, we have a high card
    assert len(sorted_counts) == 5
    return ranking(ranking.high_card,
                   reversed([c.ace_high_index() for c in cardlist]))


def get_7_card_ranking(cardlist):
    best_so_far = None
    for _5cards in itertools.combinations(cardlist, 5):
        ranking = get_5_card_ranking(_5cards)
        if best_so_far is None or (ranking > best_so_far):
            best_so_far = ranking
    return best_so_far
