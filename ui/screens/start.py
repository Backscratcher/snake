# -*- coding: utf-8 -*-

import curses

from configurator import settings
from ui.screens.base import (
    BaseScreen,
    ConfirmationMixin,
    FigletFormatMixin,
    MenuFormatMixin,
    ScreenRedirection,
    screen_registry,
)
from ui.screens.defaults import EXIT_SCREEN, PLAY_SCREEN, START_SCREEN


class StartScreen(
        ConfirmationMixin, MenuFormatMixin, FigletFormatMixin, BaseScreen):
    screen_id = START_SCREEN
    menu_routing = {
        PLAY_SCREEN: "Play",
        EXIT_SCREEN: "Exit",
    }

    def __init__(self, *args, initial_y=5, **kwargs):
        super().__init__(*args, initial_y=5, **kwargs)

    def render(self, stdscr):
        # reset the cursor to initial_state
        self.cursor_y = self.initial_y
        screen_height, screen_width = stdscr.getmaxyx()
        self.format_figlet(
            stdscr, text="S n a k e", color=settings.COLOR_YELLOW_BLACK,
            x=screen_width // 2
        )
        self.format_menu(stdscr)
        return self.cursor_y

    def handle(self, stdscr, key):
        """Navigate through menu with `self.menu_selected_option` and"""
        if key == curses.KEY_UP and self.menu_selected_option > 1:
            self.menu_selected_option -= 1
        elif key == curses.KEY_DOWN and self.menu_selected_option < len(self.menu_routing):
            self.menu_selected_option += 1
        elif key == curses.KEY_ENTER or key == 10:
            if self.menu_selected_option == EXIT_SCREEN:
                exit_redirect = self.confirmation_loop(stdscr)
                if exit_redirect:
                    return ScreenRedirection(screen_id=EXIT_SCREEN)
            elif self.menu_selected_option == PLAY_SCREEN:
                return ScreenRedirection(screen_id=PLAY_SCREEN)


screen_registry[StartScreen.screen_id] = StartScreen
