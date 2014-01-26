#!/usr/bin/env python3

from poker.interactive import HoldEmInterpreter


def main():
    interpreter = HoldEmInterpreter()
    interpreter.cmdloop()


if __name__ == '__main__':
    main()
