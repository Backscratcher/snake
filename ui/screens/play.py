# -*- coding: utf-8 -*-

import curses
import random
from curses import textpad
from dataclasses import dataclass

from configurator import settings
from ui.screens.base import (
    BaseScreen,
    ConfirmationMixin,
    FigletFormatMixin,
    screen_registry,
    ScreenRedirection,
)
from ui.screens.defaults import EXIT_SCREEN, PLAY_SCREEN, START_SCREEN


@dataclass
class RectangleBoxBorder:
    start: tuple
    end: tuple


@dataclass
class GameObject:
    y: int
    x: int
    character: str
    _type: str

    def __eq__(self, other):
        return (
            isinstance(other, GameObject) and
            self.y == other.y and self.x == other.x
        )


class Snake:
    def __init__(self, head, length=3, direction=curses.KEY_UP):
        self.head = GameObject(*head, character="@", _type="head")
        self.body = [
            GameObject(
                y=self.head.y + index, x=self.head.x, character="#", _type="body"
            )
            for index in range(1, length)
        ]
        self.body.insert(0, self.head)
        self.direction = direction

    def __len__(self):
        return len(self.body)

    def __iter__(self):
        return iter(self.body)

    def __contains__(self, game_object):
        for node in self.body:
            if node.y == game_object.y and node.x == game_object.x and node._type == "body":
                return True
        return False

    def move(self, key, food):
        # snake cannot move in the opposite direction
        if key in settings.snake_directions and key != settings.snake_illegal_turns[self.direction]:
            self.direction = key

        new_node = GameObject(y=self.head.y, x=self.head.x, character="#", _type="body")
        if self.direction == curses.KEY_UP:
            self.head.y -= 1
        elif self.direction == curses.KEY_LEFT:
            self.head.x -= 1
        elif self.direction == curses.KEY_RIGHT:
            self.head.x += 1
        elif self.direction == curses.KEY_DOWN:
            self.head.y += 1

        did_eat = False
        self.body.insert(1, new_node)
        if food == self.head:
            did_eat = True
        else:
            self.body.pop()
        return did_eat


class PlayScreen(ConfirmationMixin, FigletFormatMixin, BaseScreen):
    screen_id = PLAY_SCREEN

    def __init__(self, *args, **kwargs):
        stdscr = kwargs.pop("stdscr")
        super().__init__(*args, initial_y=5, **kwargs)
        self.score = 0
        screen_height, screen_width = stdscr.getmaxyx()
        self.snake = Snake(
            head=(
                screen_height // 2 + random.randint(1, 10),
                screen_width // 2 - random.randint(1, 10),
            )
        )
        self.food = None

    def render(self, stdscr):
        self.cursor_y = self.initial_y
        screen_height, screen_width = stdscr.getmaxyx()
        self.format_figlet(
            stdscr,
            text=f"Score : {self.score}",
            color=settings.COLOR_YELLOW_BLACK,
            x=screen_width // 2,
        )
        # game screen
        self.rectangle_borders = RectangleBoxBorder(
            start=(self.cursor_y + 1, screen_width // 4),
            end=(
                self.cursor_y + 1 + screen_height * 2 // 3,
                screen_width // 2 + screen_width // 4,
            ),
        )
        textpad.rectangle(
            stdscr,
            self.rectangle_borders.start[0],
            self.rectangle_borders.start[1],
            self.rectangle_borders.end[0],
            self.rectangle_borders.end[1],
        )
        for node in self.snake:
            stdscr.addstr(node.y, node.x, node.character)
        self.spawn_food(stdscr)

    def handle(self, stdscr, key):
        did_eat = self.snake.move(key=key, food=self.food)
        if did_eat:
            self.score += 1
            self.food = None
            stdscr.timeout(100 - (len(self.snake) // 4))

        screen_height, screen_width = stdscr.getmaxyx()
        if (self.snake.head.y in [self.rectangle_borders.start[0], self.rectangle_borders.end[0]] or 
            self.snake.head.x in [self.rectangle_borders.start[1], self.rectangle_borders.end[1]] or
            self.snake.head in self.snake):
            exit_redirect = self.confirmation_loop(
                stdscr,
                text=f"You scored {self.score}. Would you like to try again ?",
            )
            if exit_redirect:
                return ScreenRedirection(screen_id=START_SCREEN)
            return ScreenRedirection(screen_id=EXIT_SCREEN)

    def spawn_food(self, stdscr):
        while self.food is None:
            self.food = GameObject(
                y=random.randint(
                    self.rectangle_borders.start[0] + 1,
                    self.rectangle_borders.end[0] - 1
                ),
                x=random.randint(
                    self.rectangle_borders.start[1] + 1,
                    self.rectangle_borders.end[1] - 1,
                ),
                character="*",
                _type="food",
            )
            if self.food in self.snake:
                self.food = None
        stdscr.addstr(
            self.food.y,
            self.food.x,
            self.food.character,
        )


screen_registry[PlayScreen.screen_id] = PlayScreen
