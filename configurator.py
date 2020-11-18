# -*- coding: utf-8 -*-

import curses


class Configurator:
    ALIGNMENT_LEFT = 1
    ALIGNMENT_CENTER = 2
    ALIGNMENT_RIGHT = 3

    ALIGNMENTS = [
        ALIGNMENT_LEFT, ALIGNMENT_CENTER, ALIGNMENT_RIGHT
    ]

    COLOR_YELLOW_BLACK = 1
    COLOR_BLACK_WHITE = 2

    _configured = False

    def configure(self):
        if self._configured:
            raise Exception("Settings are already configured!")
        self.prepare_colors()
        self._configured = True

    @property
    def snake_directions(self):
        return [
            curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT
        ]

    @property
    def snake_illegal_turns(self):
        return {
            curses.KEY_UP: curses.KEY_DOWN,
            curses.KEY_LEFT: curses.KEY_RIGHT,
            curses.KEY_RIGHT: curses.KEY_LEFT,
            curses.KEY_DOWN: curses.KEY_UP,
        }

    def prepare_colors(self):
        curses.start_color()
        curses.init_pair(
            self.COLOR_YELLOW_BLACK, curses.COLOR_YELLOW, curses.COLOR_BLACK,
        )
        curses.init_pair(
            self.COLOR_BLACK_WHITE, curses.COLOR_BLACK, curses.COLOR_WHITE,
        )


settings = Configurator()
