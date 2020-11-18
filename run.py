# -*- coding: utf-8 -*-

import curses
import curses.ascii

from configurator import settings
from ui.screens.base import ScreenRedirection, screen_registry
from ui.screens.defaults import START_SCREEN


class SnakeGame:
    def __init__(self):
        self.initial_screen = screen_registry[START_SCREEN]

    def run(self, stdscr):
        settings.configure()
        screen = self.initial_screen(initial_y=5)
        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.timeout(100)
        while True:
            stdscr.clear()
            screen.render(stdscr)
            key = stdscr.getch()
            result = screen.handle(stdscr, key)
            if isinstance(result, ScreenRedirection):
                screen = result.redirect(stdscr=stdscr)
            stdscr.refresh()


if __name__ == '__main__':
    game = SnakeGame()
    curses.wrapper(game.run)
