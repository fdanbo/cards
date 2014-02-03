
import mock
import unittest

import cards
import poker.holdem as holdem


def create_stacked_deck(hands_wanted_strings, upcards_wanted_string):
    # create an actual deck to pull the cards from; this is so that we don't
    # duplicate cards, and end up with the correct number of cards in the
    # deck.
    unused_cards = cards.Deck(shuffle=False)

    hands_wanted = []
    for s in hands_wanted_strings:
        h = cards.Hand(s)
        hands_wanted.append(h)
        for c in h:
            unused_cards.popcard(c.rank, c.suit)

    upcards_wanted = cards.Hand(upcards_wanted_string)
    for c in upcards_wanted:
        unused_cards.popcard(c.rank, c.suit)

    newdeck = cards.Deck(deckcount=0)

    def addcard(c=None):
        if c:
            newdeck.append(c)
        else:
            # deal something out of unused_cards
            c = unused_cards.pop()
            newdeck.append(c)

    for hand in hands_wanted:
        addcard(hand[0])
    for hand in hands_wanted:
        addcard(hand[1])

    # burn, flop, burn, turn, burn, river.
    addcard()
    for i in range(3):
        addcard(upcards_wanted.pop())
    addcard()
    addcard(upcards_wanted.pop())
    addcard()
    addcard(upcards_wanted.pop())

    # add the remaining cards from the deck
    while len(unused_cards):
        addcard(unused_cards.deal())

    return newdeck


class HoldEmTest(unittest.TestCase):
    def test_flow(self):
        callback = mock.MagicMock()
        game = holdem.HoldEm([str(i) for i in range(3)], callback)

        # deal; post the blinds
        game.deal()
        self.assertEqual(game.pot, 3)
        self.assertEqual(len(game.upcards), 0)
        callback.assert_has_calls([
            mock.call('small_blind', 1, holdem.HoldEm.small_blind),
            mock.call('big_blind', 2, holdem.HoldEm.big_blind),
            mock.call('next_to_act', 0, 2)])
        callback.reset_mock()
        self.assertEqual(game.get_player_sb(), game.get_player(1))
        self.assertEqual(game.get_player_bb(), game.get_player(2))

        # blinds were player 1 and 2; player 0 calls
        game.putmoneyin(2)
        self.assertEqual(game.pot, 5)
        callback.assert_has_calls([
            mock.call('call', 0, 2),
            mock.call('next_to_act', 1, 1)])
        callback.reset_mock()

        # player 1 (small blind) folds.  only players 0 and 2 are left.
        game.fold()
        self.assertEqual(game.pot, 5)
        callback.assert_has_calls([
            mock.call('fold', 1),
            mock.call('option', 2, 0)])
        callback.reset_mock()

        # player 2 has the option; check. deal the flop.
        self.assertEqual(len(game.upcards), 0)
        game.putmoneyin(0)
        self.assertEqual(game.pot, 5)
        self.assertEqual(len(game.upcards), 3)
        callback.assert_has_calls([
            mock.call('check', 2, 0),
            mock.call('flop'),
            mock.call('next_to_act', 2, 0)])
        callback.reset_mock()

        # player 2 is first to act.  bet.
        game.putmoneyin(2)
        self.assertEqual(game.pot, 7)
        callback.assert_has_calls([
            mock.call('bet', 2, 2),
            mock.call('next_to_act', 0, 2)])
        callback.reset_mock()

        # player 0 calls. deal the turn.
        game.putmoneyin(2)
        self.assertEqual(game.pot, 9)
        self.assertEqual(len(game.upcards), 4)
        callback.assert_has_calls([
            mock.call('call', 0, 2),
            mock.call('turn'),
            mock.call('next_to_act', 2, 0)])
        callback.reset_mock()

        # player 2 checks
        game.putmoneyin(0)
        self.assertEqual(game.pot, 9)
        callback.assert_has_calls([
            mock.call('check', 2, 0),
            mock.call('next_to_act', 0, 0)])
        callback.reset_mock()

        # player 0 checks. deal the river.
        game.putmoneyin(0)
        self.assertEqual(game.pot, 9)
        self.assertEqual(len(game.upcards), 5)
        callback.assert_has_calls([
            mock.call('check', 0, 0),
            mock.call('river'),
            mock.call('next_to_act', 2, 0)])
        callback.reset_mock()

        # player 2 is first to act. bet.
        game.putmoneyin(2)
        self.assertEqual(game.pot, 11)
        callback.assert_has_calls([
            mock.call('bet', 2, 2),
            mock.call('next_to_act', 0, 2)])
        callback.reset_mock()

        # player 0 raises.
        game.putmoneyin(4)
        self.assertEqual(game.pot, 15)
        callback.assert_has_calls([
            mock.call('raise', 0, 2),
            mock.call('next_to_act', 2, 2)])
        callback.reset_mock()

        # player 2 folds -- player 0 wins.
        game.fold()
        self.assertEqual(game.pot, 15)
        callback.assert_has_calls([
            mock.call('fold', 2),
            mock.call('win', 0, 15),
            mock.call('end')])
        callback.reset_mock()

        # make sure the player banks are updated correctly.  by default the
        # banks start at 0.
        self.assertEqual(game.get_player(0).bank, 7)
        self.assertEqual(game.get_player(1).bank, -1)
        self.assertEqual(game.get_player(2).bank, -6)

        # start another hand; make sure the button moved.
        game.deal()
        self.assertEqual(game.pot, 3)
        self.assertEqual(len(game.upcards), 0)
        callback.assert_has_calls([
            mock.call('small_blind', 2, holdem.HoldEm.small_blind),
            mock.call('big_blind', 0, holdem.HoldEm.big_blind),
            mock.call('next_to_act', 1, 2)])
        self.assertEqual(game.get_player_sb(), game.get_player(2))
        self.assertEqual(game.get_player_bb(), game.get_player(0))
        callback.reset_mock()

    def test_showdown(self):
        # here are the hands I want to have
        hands = [
            # straight, flush, full house.  Note that this is the order that
            # the hands will come out of the deck after the button, so the
            # order is actually p1, p2, p0 (button)
            'T♡J♠', 'A♠T♠', '7♡8♢'
        ]

        # and here's what I want to show up on the table
        upcards = '7♠8♡9♠2♠7♣'

        callback = mock.MagicMock()
        game = holdem.HoldEm([str(i) for i in range(3)], callback)

        # stack the deck
        stacked_deck = create_stacked_deck(hands, upcards)

        # have the best hand fold, to test to make sure that he's not
        # considered in the showdown.
        game.deal(deck=stacked_deck)

        # make sure the stacked deck worked.  note hand order p1/p2/p0
        self.assertEqual(str(game.players[0].hand), hands[2])
        self.assertEqual(str(game.players[1].hand), hands[0])
        self.assertEqual(str(game.players[2].hand), hands[1])

        # pre-flop
        game.putmoneyin(2)
        game.putmoneyin(1)
        game.putmoneyin(0)
        # flop
        game.putmoneyin(2)
        game.putmoneyin(2)
        game.putmoneyin(2)
        # turn
        game.putmoneyin(0)
        game.putmoneyin(2)
        game.putmoneyin(2)
        game.putmoneyin(2)
        # river
        game.putmoneyin(2)  # player 1 bets (straight)
        game.putmoneyin(2)  # player 2 calls (flush)
        game.fold()         # player 0 folds (full house)

        callback.assert_has_calls([
            mock.call('small_blind', 1, holdem.HoldEm.small_blind),
            mock.call('big_blind', 2, holdem.HoldEm.big_blind),
            # pre-flop
            mock.call('next_to_act', 0, 2),
            mock.call('call', 0, 2),
            mock.call('next_to_act', 1, 1),
            mock.call('call', 1, 1),
            mock.call('option', 2, 0),
            mock.call('check', 2, 0),
            # flop
            mock.call('flop'),
            mock.call('next_to_act', 1, 0),
            mock.call('bet', 1, 2),
            mock.call('next_to_act', 2, 2),
            mock.call('call', 2, 2),
            mock.call('next_to_act', 0, 2),
            mock.call('call', 0, 2),
            # turn
            mock.call('turn'),
            mock.call('next_to_act', 1, 0),
            mock.call('check', 1, 0),
            mock.call('next_to_act', 2, 0),
            mock.call('bet', 2, 2),
            mock.call('next_to_act', 0, 2),
            mock.call('call', 0, 2),
            mock.call('next_to_act', 1, 2),
            mock.call('call', 1, 2),
            # river
            mock.call('river'),
            mock.call('next_to_act', 1, 0),
            mock.call('bet', 1, 2),
            mock.call('next_to_act', 2, 2),
            mock.call('call', 2, 2),
            mock.call('next_to_act', 0, 2),
            mock.call('fold', 0),
            # showdown
            mock.call('showdown'),
            mock.call('win', 2, 22),
            mock.call('end')
        ])

    def test_split_pot(self):
        # split a hand among three of the four players.  remember again the
        # deal order: p1/p2/p3/p0
        hands = ['K♡J♠', 'K♠T♡', '7♡8♢', '8♡K♢']
        upcards = 'A♠A♡Q♠2♠A♣'
        callback = mock.MagicMock()
        game = holdem.HoldEm([str(i) for i in range(4)], callback)

        stacked_deck = create_stacked_deck(hands, upcards)

        # just because it's a lot I'm going to skip checking the callbacks
        # until the end.
        game.deal(stacked_deck)
        game.putmoneyin(2)
        game.putmoneyin(2)
        game.putmoneyin(1)
        game.putmoneyin(0)  # option
        # flop
        for i in range(4):
            game.putmoneyin(0)
        # turn. bet/call just to mix things up.
        for i in range(4):
            game.putmoneyin(2)
        # river. hold off on the last one so that we can check the callbacks.
        for i in range(3):
            game.putmoneyin(0)

        callback.reset_mock()

        game.putmoneyin(0)
        callback.assert_has_calls([
            mock.call('check', 0, 0),
            mock.call('showdown'),
            mock.call('split_pot'),
            mock.call('win', 1, 6),
            mock.call('win', 2, 5),
            mock.call('win', 0, 5),
            mock.call('end')
        ])
