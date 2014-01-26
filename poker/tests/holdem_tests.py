
import mock
import unittest

import poker.holdem as holdem


class HoldEmTest(unittest.TestCase):
    def test_flow(self):
        callback = mock.MagicMock()
        game = holdem.HoldEm([str(i) for i in range(3)], callback)

        game.deal()
        self.assertEqual(game.pot, 3)
        callback.assert_has_calls([
            mock.call('small_blind', 1, holdem.HoldEm.small_blind),
            mock.call('big_blind', 2, holdem.HoldEm.big_blind),
            mock.call('next_to_act', 0, 2)])
        callback.reset_mock()

        game.putmoneyin(2)
        self.assertEqual(game.pot, 5)
        callback.assert_has_calls([
            mock.call('call', 0, 2),
            mock.call('next_to_act', 1, 1)])
        callback.reset_mock()

        game.fold()
        self.assertEqual(game.pot, 5)
        callback.assert_has_calls([
            mock.call('fold', 1),
            mock.call('option', 2, 0)])
        callback.reset_mock()

        game.putmoneyin(0)
        self.assertEqual(game.pot, 5)
        callback.assert_has_calls([
            mock.call('check', 2, 0),
            mock.call('flop'),
            mock.call('next_to_act', 2, 0)])
        callback.reset_mock()

        game.putmoneyin(2)
        self.assertEqual(game.pot, 7)
        callback.assert_has_calls([
            mock.call('bet', 2, 2),
            mock.call('next_to_act', 0, 2)])
        callback.reset_mock()

        game.putmoneyin(2)
        self.assertEqual(game.pot, 9)
        callback.assert_has_calls([
            mock.call('call', 0, 2),
            mock.call('turn'),
            mock.call('next_to_act', 2, 0)])
        callback.reset_mock()

        game.putmoneyin(0)
        self.assertEqual(game.pot, 9)
        callback.assert_has_calls([
            mock.call('check', 2, 0),
            mock.call('next_to_act', 0, 0)])
        callback.reset_mock()

        game.putmoneyin(0)
        self.assertEqual(game.pot, 9)
        callback.assert_has_calls([
            mock.call('check', 0, 0),
            mock.call('river'),
            mock.call('next_to_act', 2, 0)])
        callback.reset_mock()

        game.putmoneyin(2)
        self.assertEqual(game.pot, 11)
        callback.assert_has_calls([
            mock.call('bet', 2, 2),
            mock.call('next_to_act', 0, 2)])
        callback.reset_mock()

        game.putmoneyin(4)
        self.assertEqual(game.pot, 15)
        callback.assert_has_calls([
            mock.call('raise', 0, 2),
            mock.call('next_to_act', 2, 2)])
        callback.reset_mock()

        game.fold()
        self.assertEqual(game.pot, 15)
        callback.assert_has_calls([
            mock.call('fold', 2),
            mock.call('win', 0, 15),
            mock.call('end')])
        callback.reset_mock()

    def test_showdown(self):
        pass

    def test_split_pot(self):
        pass
