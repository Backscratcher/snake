# -*- coding: utf-8 -*-

import curses
import sys
from curses import textpad

import pyfiglet

from configurator import settings

from ui.screens.defaults import EXIT_SCREEN

screen_registry = {
    EXIT_SCREEN: None
}


class BaseScreen:
    screen_id = None

    def __init__(self, *args, initial_y=0, **kwargs):
        self.initial_y = initial_y
        self.cursor_y = initial_y
        screen_registry[self.screen_id] = self.__class__

    def render(self, stdscr):
        """Render screen related components."""
        raise NotImplementedError

    def handle(self, stdscr, key):
        """Handle user input via key, handle redirections and possible actions
        that user can make.
        """
        raise NotImplementedError


class MenuFormatMixin:
    menu_routing = {}

    def __init__(self, *args, **kwargs):
        self.menu_selected_option = 1
        super().__init__(*args, **kwargs)

    def format_menu(self, stdscr):
        """Show menu, to make things easier always show it in the middle of the
        screen.
        """
        screen_height, screen_width = stdscr.getmaxyx()
        half_width = screen_width // 2
        for id, menu_option in self.menu_routing.items():
            x = half_width - len(menu_option) // 2
            y = self.cursor_y + id
            stdscr.addstr(
                y,
                x,
                menu_option,
                curses.color_pair(
                    settings.COLOR_BLACK_WHITE
                    if id == self.menu_selected_option else 0
                )
            )
            self.cursor_y += 1


class FigletFormatMixin:
    def format_figlet(self, stdscr, text, color, y=0, x=0, font="big"):
        screen_height, screen_width = stdscr.getmaxyx()
        text = pyfiglet.figlet_format(text, font=font)
        text_splitted = text.splitlines()
        y = y if y else self.cursor_y
        for index, line in enumerate(text_splitted, y):
            stdscr.addstr(
                index,
                x - len(line) // 2 if x > len(line) // 2 else x,
                line,
                curses.color_pair(color)
            )
        self.cursor_y += len(text_splitted)


class ConfirmationMixin:
    def confirmation_loop(self, stdscr, text="Do you want to exit?"):
        selected = "yes"
        while True:
            key = stdscr.getch()

            if key == curses.KEY_RIGHT and selected == "yes":
                selected = "no"
            elif key == curses.KEY_LEFT and selected == "no":
                selected = "yes"
            elif key == curses.KEY_ENTER or key == 10:
                return True if selected == "yes" else False

            self.format_confirmation(
                stdscr=stdscr,
                text=text,
                selected=selected,
            )

    def format_confirmation(self, stdscr, text, selected):
        stdscr.clear()
        screen_height, screen_width = stdscr.getmaxyx()
        textpad.rectangle(
            stdscr,
            screen_height // 2 - 4,
            screen_width // 2 - len(text),
            screen_height // 2 + 4,
            screen_width // 2 + len(text),

        )
        stdscr.addstr(
            screen_height // 2,
            screen_width // 2 - len(text) // 2,
            text,
        )
        options_width = len(text) // 2

        option = "yes"
        y = screen_height // 2 + 1
        x = screen_width // 2 - options_width // 2 + len(option)
        stdscr.addstr(
            y,
            x,
            option,
            curses.color_pair(
                settings.COLOR_BLACK_WHITE if option == selected
                else 0
            )
        )

        option = "no"
        x = screen_width // 2 + options_width // 2 - len(option)
        stdscr.addstr(
            y,
            x,
            option,
            curses.color_pair(
                settings.COLOR_BLACK_WHITE if option == selected
                else 0
            )
        )
        stdscr.refresh()
        self.cursor_y = screen_height // 2 + 1


class ScreenRedirection:
    def __init__(self, screen_id, **kwargs):
        self.screen_id = screen_id
        self.screen = screen_registry[self.screen_id]
        self.kwargs = kwargs

    def redirect(self, **kwargs):
        if self.screen_id == EXIT_SCREEN:
            # This is the special case of the redirection since it does not
            # have a screen to be redirected to, so we just hook to the
            # redirect and terminate the program.
            curses.endwin()
            sys.exit(0)

        kwargs.update(**self.kwargs)
        return self.screen(**kwargs)
