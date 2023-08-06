#!/usr/bin/env python3
# noqa: E402
# ****************************************************************************
# Copyright (C) 2021-2022 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pycursorsio project, which is MIT-licensed.
# ****************************************************************************
"""Command-line interface and main game."""

import os
import os.path
import typing as t
from asyncio import run as run_async, sleep
from os import environ
from platform import python_implementation, python_version
from sys import stderr

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import aiostream.stream as aiostream  # noqa: E402

import click  # noqa: E402

import pygame  # noqa: E402

from . import __version__ as pycursorsio_version  # noqa: E402
from .m28n import M28NAPI  # noqa: E402
from .state import (  # noqa: E402
    Button, Detector, Text, Wall, Warp, create_game_state,
)

__all__ = ['cli']


class Assets:
    """Class for loading assets."""

    def __init__(self):
        assets_folder = os.path.join(os.path.dirname(__file__), 'assets')

        self._fontpath = os.path.join(assets_folder, 'NovaSquare.ttf')
        self._fontsizes = {}

        self._icon = pygame.image.load(os.path.join(
            assets_folder,
            'favicon.ico',
        ))
        self._cursor = pygame.image.load(os.path.join(
            assets_folder,
            'cursor.png',
        ))

        self._circlecache = {}

    @property
    def icon(self) -> pygame.Surface:
        return self._icon

    @property
    def cursor(self) -> pygame.Surface:
        return self._cursor

    @property
    def cursor_offset(self) -> t.Tuple[int, int]:
        return (5, 5)

    def font(self, size: int) -> pygame.font.Font:
        if size not in self._fontsizes:
            self._fontsizes[size] = pygame.font.Font(self._fontpath, size)

        return self._fontsizes[size]

    def _circlepoints(self, r: float) -> t.Sequence[t.Tuple[int, int]]:
        r = int(round(r))
        if r in self._circlecache:
            return self._circlecache[r]

        x, y, e = r, 0, 1 - r
        self._circlecache[r] = points = []
        while x >= y:
            points.append((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1

        points += [(y, x) for x, y in points if x > y]
        points += [(-x, y) for x, y in points if x]
        points += [(x, -y) for x, y in points if y]
        points.sort()
        return points

    def text(
        self, text: str, size: int,
        color: t.Tuple[int, int, int] = (0, 0, 0),
    ) -> pygame.surface.Surface:
        return self.font(size).render(text, True, color)

    def text_outline(
        self, text: str, size: int,
        color: t.Tuple[int, int, int] = (255, 255, 255),
        outline_color: t.Tuple[int, int, int] = (0, 0, 0),
        outline_size: int = 2,
    ) -> pygame.Surface:
        # Gotta admit, this code comes from here:
        # <https://stackoverflow.com/a/54365870>
        font = self.font(size)

        textsurface = font.render(text, True, color).convert_alpha()
        w = textsurface.get_width() + 2 * outline_size
        h = font.get_height()

        osurf = pygame.Surface((w, h + 2 * outline_size)).convert_alpha()
        osurf.set_alpha(int(.5 * 255))
        osurf.fill((0, 0, 0, 0))

        surf = osurf.copy()

        osurf.blit(
            font.render(text, True, outline_color).convert_alpha(),
            (0, 0),
        )
        for dx, dy in self._circlepoints(outline_size):
            surf.blit(osurf, (dx + outline_size, dy + outline_size))

        del osurf

        finalsurface = pygame.Surface(
            (w, h + 2 * outline_size),
            pygame.SRCALPHA,
        )
        finalsurface.blit(surf, (0, 0))
        finalsurface.blit(textsurface, (outline_size, outline_size))

        del surf, textsurface
        return finalsurface


async def amain(url: str) -> None:
    """Run the game asynchronously."""
    if not url:
        server = await M28NAPI().find_server_preference(
            'cursors',
            secure=False,
        )
        if server is None:
            print('ERROR: no server found using the M28N API!', file=stderr)
            return

        print('Using the following server found using the M28 API:')
        print(f'   name: {server.domain:<16}   region: {server.region_name}')
        print(f'   ipv4: {server.ipv4:<16}   ipv6: {server.ipv6}')

        host = server.ipv4 if server.ipv4 else f'[{server.ipv6}]'
        url = f'ws://{host}:2828/'

    # Initialize the game engines.
    pygame.display.init()
    pygame.font.init()

    assets = Assets()

    async with create_game_state(url) as state:
        # FIXME: for now, we can't grab the cursor because it fucks up
        # with the collisions. As said in the pygame mouse documentation:
        #
        # > If the mouse cursor is hidden, and input is grabbed to the
        # > current display the mouse will enter a virtual input mode,
        # > where the relative movements of the mouse will never be stopped
        # > by the borders of the screen. See the functions
        # > ``pygame.mouse.set_visible()`` and ``pygame.event.set_grab()``
        # > to get this configured.
        #
        #  -- from <http://www.pygame.org/docs/ref/mouse.html>
        #
        # Indeed, we use a custom cursor image by making the cursor
        # invisible and blitting the cursor surface at the cursor position,
        # and we want to grab the cursor so that it doesn't escape the window,
        # which can be annoying for the user; that case applies to us.
        #
        # However, we also use ``pygame.mouse.set_pos()``, which doesn't
        # seem to apply to this virtual input pointer, breaking all of our
        # system that relies on this function.
        #
        # So for now, grabbing is disabled, and there is no way to lock the
        # cursor into the window...
        #
        #  -- Thomas Touhey <thomas@touhey.fr>, November 7th, 2020
        _should_grab = False

        # Initialize our window and the cursor.
        screen = pygame.display.set_mode(
            (state.width, state.height),
            pygame.DOUBLEBUF,
        )
        pygame.display.set_caption('cursors.io python client')
        pygame.display.set_icon(assets.icon)

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(_should_grab)

        async def pygame_events() -> t.AsyncIterator[pygame.event.Event]:
            """Generate pygame events.

            It's just an approximation of making the event getting
            function from pygame asynchronous, by just checking on
            it every 50 ms, allowing for other events to be checked
            on during every sleep.
            """
            while True:
                event = pygame.event.poll()
                if event.type == pygame.NOEVENT:
                    await sleep(.005)
                    continue

                yield event

        async def game_events() -> t.AsyncIterator[pygame.event.Event]:
            """Generate websocket events.

            When a frame is received, a USEREVENT is sent to
            the main function. USEREVENTs only represent network
            events, drawing events are represented as NOEVENT;
            see ``regular_events()``.
            """
            async for data in state.handle_packets():
                is_position_set, = data
                yield pygame.event.Event(pygame.USEREVENT, data={
                    'is_position_set': is_position_set,
                })

        async def regular_events() -> t.AsyncIterator[pygame.event.Event]:
            """Generate regular events.

            Useful for displaying a constant number of times the content of
            the window, so as to improve our performances (instead of just
            drawing every time an event occurs, which can slow
            down our processing of network and local events).
            """
            tm = 1.0 / 60  # number of fps

            while True:
                yield pygame.event.Event(pygame.NOEVENT)
                await sleep(tm)

        async with aiostream.merge(
            regular_events(),
            game_events(),
            pygame_events(),
        ).stream() as streamer:
            # Here, a few state variables not managed by the GameState()
            # because not really part of the game but more of how to
            # treat the input.
            #
            # ``blocked_x``, ``blocked_y``
            #    Allows for the user to block the x or the y coordinate of
            #    the mouse to only move the cursor horizontally or vertically,
            #    which can be really useful in some places.
            #
            # ``paused``
            #    If the game is in pause mode or not. In pause mode, the game
            #    state still is refreshed in the background, but the user
            #    inputs are not taken into account and, if the cursor was
            #    grabbed, it is not anymore, so that the user can do tasks in
            #    other windows without disconnecting from the game.
            blocked_x, blocked_y = None, None
            paused = False

            # Main event treatment loop.
            #
            # The only event leading to the drawing section is NOEVENT,
            # which is produced by ``regular_events()`` approximately 60 times
            # every second.
            async for event in streamer:
                if event.type == pygame.QUIT:
                    break
                elif event.type == pygame.NOEVENT:
                    # Is a display event, so let's show'em what we do best!
                    pass
                elif event.type == pygame.USEREVENT:
                    if event.data['is_position_set'] and not paused:
                        pygame.mouse.set_pos(state.position)

                    continue
                elif paused:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        paused = False
                        pygame.event.set_grab(_should_grab)
                        pygame.mouse.set_visible(False)
                        pygame.mouse.set_pos(state.position)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # Two times escape, it's a quit!
                            break

                    continue
                else:
                    if event.type == pygame.MOUSEMOTION:
                        x, y = event.pos
                        ox, oy = x, y

                        if blocked_x is not None:
                            x = blocked_x
                        if blocked_y is not None:
                            y = blocked_y

                        x, y = state.set_position(x, y)
                        if (x, y) != (ox, oy):
                            pygame.mouse.set_pos((x, y))

                        await state.send_mouse_position()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            await state.send_mouse_click()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LCTRL:
                            blocked_x = state.position[0]
                        elif event.key == pygame.K_LALT:
                            blocked_y = state.position[1]
                        elif event.key == pygame.K_ESCAPE:
                            paused = True
                            pygame.event.set_grab(False)
                            pygame.mouse.set_visible(True)
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LCTRL:
                            blocked_x = None
                        elif event.key == pygame.K_LALT:
                            blocked_y = None
                    elif event.type == pygame.ACTIVEEVENT:
                        if event.state == 1 and not event.gain:
                            # Window has been unfocused.
                            paused = True
                            pygame.event.set_grab(False)
                            pygame.mouse.set_visible(True)
                        elif event.state == 1 and event.gain:
                            # Window has been focused.
                            # Let's redraw.
                            pass

                    continue

                # The display code!
                # What we want to draw is, in order:
                #
                # - the elements of the level, also called "objects":
                #   text elements, walls, warps, detectors, buttons.
                # - the bottom texts representing some help lines and
                #   the player count.
                # - the drawn lines by the users.
                # - the click animations.
                # - the other cursors.
                # - our own cursor, with a yellow circle identifying it.
                screen.fill((255, 255, 255))

                for object in state.objects:
                    if isinstance(object, Text):
                        rndr = assets.text(object.text, object.size)
                        x, y = object.x, object.y
                        if object.centered:
                            x -= rndr.get_width() // 2
                        y -= rndr.get_height()
                        screen.blit(rndr, (x, y))
                    elif isinstance(object, Wall):
                        x, y = object.x, object.y
                        w, h = object.width, object.height
                        color = object.color
                        pygame.draw.rect(screen, color, (x, y, w, h))
                    elif isinstance(object, Warp):
                        rect = pygame.Surface((object.width, object.height))
                        rect.fill((255, 0, 0) if object.bad else (0, 255, 0))
                        rect.set_alpha(int(.2 * 255))
                        screen.blit(rect, (object.x, object.y))
                    elif isinstance(object, Detector):
                        x, y = object.x, object.y
                        w, h = object.width, object.height

                        rect = pygame.Surface((w, h))
                        rect.fill(object.color)
                        rect.set_alpha(int(.2 * 255))
                        screen.blit(rect, (x, y))

                        if w < 80 or h < 80:
                            fontsize = 30
                        else:
                            fontsize = 60

                        rndr = assets.text(f'{object.count}', fontsize)
                        rndr.set_alpha(int(.5 * 255))
                        tx = x + w // 2 - rndr.get_width() // 2
                        ty = y + h // 2 - rndr.get_height() // 2

                        screen.blit(rndr, (tx, ty))
                    elif isinstance(object, Button):
                        x, y = object.x, object.y
                        w, h = object.width, object.height
                        pressed = object.pressed
                        b = 8 if pressed else 12

                        # We draw the button's base.
                        button = pygame.Surface((w, h))
                        button.fill(object.color)

                        work = pygame.Surface((w, h), pygame.SRCALPHA)
                        work.fill((0, 0, 0))
                        work.set_alpha(int(.2 * 255))
                        button.blit(work, (0, 0))
                        del work

                        # We draw the button's top.
                        work = pygame.Surface((w - 2 * b, h - 2 * b))
                        work.fill(object.color)
                        button.blit(work, (b, b))
                        del work

                        # We draw the grid.
                        work = pygame.Surface((w, h), pygame.SRCALPHA)
                        pygame.draw.line(
                            work,
                            (0, 0, 0),
                            (0, 0),
                            (b, b),
                            width=2,
                        )
                        pygame.draw.line(
                            work,
                            (0, 0, 0),
                            (w - 1, 0),
                            (w - b - 1, b),
                            width=2,
                        )
                        pygame.draw.line(
                            work,
                            (0, 0, 0),
                            (0, h - 1),
                            (b, h - b - 1),
                            width=2,
                        )
                        pygame.draw.line(
                            work,
                            (0, 0, 0),
                            (w - 1, h - 1),
                            (w - b - 1, h - b - 1),
                            width=2,
                        )
                        pygame.draw.polygon(
                            work,
                            (0, 0, 0),
                            (
                                (0, 0),
                                (w - 1, 0),
                                (w - 1, h - 1),
                                (0, h - 1),
                            ),
                            width=2,
                        )
                        pygame.draw.polygon(
                            work,
                            (0, 0, 0),
                            (
                                (b, b),
                                (w - b - 1, b),
                                (w - b - 1, h - b - 1),
                                (b, h - b - 1),
                            ),
                            width=2,
                        )
                        work.set_alpha(int(.1 * 255))
                        button.blit(work, (0, 0))
                        del work

                        # We write the text.
                        if w <= 100 or h <= 100:
                            fontsize = 35
                            fontpad = 16
                        else:
                            fontsize = 45
                            fontpad = 13

                        rndr = assets.text(f'{object.count}', fontsize)
                        rndr.set_alpha(int(.5 * 255))

                        button.blit(rndr, (
                            w // 2 - rndr.get_width() // 2,
                            h // 2 - fontpad,
                        ))
                        del rndr

                        # Let us make it darker if the button is pressed.
                        if pressed:
                            work = pygame.Surface(
                                (w - 2 * b, h - 2 * b),
                                pygame.SRCALPHA,
                            )
                            work.fill((0, 0, 0))
                            work.set_alpha(int(.15 * 255))
                            button.blit(work, (b, b))
                            del work

                        # Let's blit the final button to the screen!
                        screen.blit(button, (x, y))

                # Display the information about the game.
                surface = assets.text_outline(
                    f'{state.player_count} players online',
                    12,
                )
                x = (
                    screen.get_width() - state.border_size - 6
                    - surface.get_width()
                )
                y = (
                    screen.get_height() - state.border_size - 6
                    - surface.get_height()
                )
                screen.blit(surface, (x, y))
                del surface

                surface = assets.text_outline('Use shift+click to draw', 12)
                x = state.border_size + 6
                y = (
                    screen.get_height() - state.border_size - 6
                    - surface.get_height()
                )
                screen.blit(surface, (x, y))
                del surface

                for line in state.drawn_lines:
                    w = abs(line.start_x - line.end_x + 1)
                    h = abs(line.start_y - line.end_y + 1)
                    x = min(line.start_x, line.end_x)
                    y = min(line.start_y, line.end_y)

                    rect = pygame.Surface((w, h), pygame.SRCALPHA)
                    pygame.draw.line(
                        rect,
                        (121, 121, 121),
                        (line.start_x - x, line.start_y - y),
                        (line.end_x - x, line.end_y - y),
                    )
                    rect.set_alpha(int(line.alpha * 255))
                    screen.blit(rect, (x, y))

                for obj in state.clicks:
                    x, y = obj.x, obj.y
                    radius = obj.radius
                    alpha = obj.alpha

                    rect = pygame.Surface(
                        (radius * 2, radius * 2),
                        pygame.SRCALPHA,
                    )
                    pygame.draw.circle(
                        rect,
                        (0, 0, 0),
                        (radius, radius),
                        radius,
                        width=3,
                    )
                    rect.set_alpha(int(.3 * alpha * 255))
                    screen.blit(rect, ((
                        x - rect.get_width() // 2,
                        y - rect.get_height() // 2,
                    )))
                    del rect

                cur_off_x, cur_off_y = assets.cursor_offset

                for cursor in state.cursors:
                    screen.blit(
                        assets.cursor,
                        (cursor.x - cur_off_x, cursor.y - cur_off_y),
                    )

                x, y = state.position
                x, y = x - cur_off_x, y - cur_off_y

                rect = pygame.Surface((40, 40), pygame.SRCALPHA)
                pygame.draw.circle(
                    rect,
                    (255, 255, 0),
                    (20, 20),
                    20,
                )
                rect.set_alpha(int(.2 * 255))

                cx = x + assets.cursor.get_width() // 2 - 23
                cy = y + assets.cursor.get_height() // 2 - 23

                screen.blit(rect, (cx, cy))
                screen.blit(assets.cursor, (x, y))

                if paused:
                    grey = pygame.Surface(
                        (screen.get_width(), screen.get_height()),
                        pygame.SRCALPHA,
                    )
                    grey.fill((128, 128, 128))
                    grey.set_alpha(int(.5 * 255))
                    screen.blit(grey, (0, 0))
                    del grey

                pygame.display.flip()

    pygame.quit()


# ---
# CLI interface.
# ---


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(
    version=pycursorsio_version,
    message=(
        f'pycursorsio version {pycursorsio_version}, '
        + f'running on {python_implementation()} {python_version()}'
    ),
)
@click.argument('url', default='', envvar='URL')
def cli(url: str) -> None:
    """Run the game using the given host and port.

    The given host must be an IPv4 address, an IPv6 address surrounded
    by brackets, or a domain name. By default, it will be found through
    the M28 API, using the 'cursors' endpoint, as the official web
    client does.

    The given port must be a valid TCP port, expressed as an integer.
    By default, it uses the same hardcoded port as the official web
    client, which is 2828.
    """
    run_async(amain(url))
