
from io import StringIO
import random
import unittest

from poker.interactive import HoldEmInterpreter


class InteractiveTest(unittest.TestCase):
    def test_split3(self):
        # better would be to stack the deck to get what we want somehow, but
        # this works well enough to give us consistency across runs of the unit
        # tests.
        random.seed(1)
        interpreter = HoldEmInterpreter()
        number_of_winners = 0

        def callback(event, index=None, amount=None):
            nonlocal number_of_winners
            interpreter.holdem_callback(event, index, amount)

            if event == 'showdown':
                number_of_winners = 0
            elif event == 'win':
                number_of_winners += 1

        interpreter.holdem.callback = callback
        while number_of_winners < 3:
            interpreter.onecmd('deal')
            while not interpreter.holdem.winners:
                interpreter.onecmd('call')
            self.assertGreater(number_of_winners, 0)

    def test_bogus_commands(self):
        interpreter = HoldEmInterpreter()
        old_stdout = interpreter.stdout

        # cannot call until you deal
        interpreter.stdout = StringIO()
        interpreter.onecmd('call')
        self.assertEqual(interpreter.stdout.getvalue(),
                         'no hand is currently being played; try "deal".\n')

        interpreter.stdout = old_stdout
        interpreter.onecmd('deal')

        # cannot check when you owe money.  this works because the player is
        # p0, and p1 and p2 are the small and big blinds, respectively.
        interpreter.stdout = StringIO()
        interpreter.onecmd('check')
        self.assertEqual(interpreter.stdout.getvalue(),
                         'that move is not currently allowed.\n')

        # completely bogus commands
        interpreter.stdout = StringIO()
        interpreter.onecmd('foobar')
        self.assertEqual(interpreter.stdout.getvalue(),
                         '*** Unknown syntax: foobar\n')

        # empty line should do nothing
        interpreter.stdout = StringIO()
        interpreter.onecmd('')
        self.assertEqual(interpreter.stdout.getvalue(), '')
