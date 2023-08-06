#!/usr/bin/env python3
# ****************************************************************************
# Copyright (C) 2022 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pycursorsio project, which is MIT-licensed.
# ****************************************************************************
"""Protocol client for the cursors.io game."""

import typing as t
from contextlib import asynccontextmanager
from math import sqrt
from time import monotonic

from .client import (
    GameClient, ServerPacket, ServerPacketType, ShapeType, create_client,
)

__all__ = [
    'Button', 'Click', 'Cursor', 'Detector', 'DrawnLine', 'GameState',
    'Text', 'Wall', 'Warp', 'create_game_state',
]


class Text:
    """A text object, non-solid."""

    def __init__(self, x: int, y: int, size: int, centered: bool, text: str):
        self._x = x
        self._y = y
        self._size = size
        self._centered = centered
        self._text = text

    @property
    def x(self) -> int:
        """Get the X coordinate of the text to display."""
        return self._x

    @property
    def y(self) -> int:
        """Get the Y coordinate of the text to display."""
        return self._y

    @property
    def size(self) -> int:
        """Get the font size."""
        return self._size

    @property
    def centered(self) -> bool:
        """Get whether the text should be centered or not."""
        return self._centered

    @property
    def text(self) -> str:
        """Get the text to display."""
        return self._text


class Wall:
    """A wall, i.e. a solid object."""

    def __init__(
        self, x: int, y: int, w: int, h: int,
        color: t.Tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._color = color

    def __repr__(self):
        attrs = ('x', 'y', 'width', 'height', 'color')
        attrs = ', '.join(f'{n} = {getattr(self, n)!r}' for n in attrs)
        return f'{self.__class__.__name__}({attrs})'

    @property
    def x(self) -> int:
        """Get the X coordinate of the top-left corner of the wall."""
        return self._x

    @property
    def y(self) -> int:
        """Get the Y coordinate of the top-left corner of the wall."""
        return self._y

    @property
    def width(self) -> int:
        """Get the width of the wall."""
        return self._w

    @property
    def w(self) -> int:
        """Get the width of the wall."""
        return self._w

    @property
    def height(self) -> int:
        """Get the height of the wall."""
        return self._h

    @property
    def h(self) -> int:
        """Get the height of the wall."""
        return self._h

    @property
    def color(self) -> t.Tuple[int, int, int, int]:
        """Get the color of the wall."""
        return self._color


class Warp:
    """A warp object, i.e. a zone which teleports a player."""

    def __init__(self, x: int, y: int, w: int, h: int, bad: bool):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._bad = bad

    def __repr__(self):
        attrs = ('x', 'y', 'width', 'height', 'bad')
        attrs = ', '.join(f'{n}={getattr(self, n)!r}' for n in attrs)
        return f'{self.__class__.__name__}({attrs})'

    @property
    def x(self) -> int:
        """Get the X coordinate of the top-left corner of the warp."""
        return self._x

    @property
    def y(self) -> int:
        """Get the Y coordinate of the top-left corner of the warp."""
        return self._y

    @property
    def width(self) -> int:
        """Get the width of the warp."""
        return self._w

    @property
    def w(self) -> int:
        """Get the width of the warp."""
        return self._w

    @property
    def height(self) -> int:
        """Get the height of the warp."""
        return self._h

    @property
    def h(self) -> int:
        """Get the height of the warp."""
        return self._h

    @property
    def bad(self) -> bool:
        """Get whether the warp is a death zone or not."""
        return self._bad


class Detector:
    """A detector, i.e. a zone where standing can activate something."""

    def __init__(
        self, x: int, y: int, w: int, h: int,
        count: int, color: int,
    ):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._count = count
        self._color = color

    def __repr__(self):
        attrs = ('x', 'y', 'width', 'height', 'count', 'color')
        attrs = ', '.join(f'{n}={getattr(self, n)!r}' for n in attrs)
        return f'{self.__class__.__name__}({attrs})'

    @property
    def x(self) -> int:
        """Get the X coordinate of the top-left corner of the detector."""
        return self._x

    @property
    def y(self) -> int:
        """Get the Y coordinate of the top-left corner of the detector."""
        return self._y

    @property
    def width(self) -> int:
        """Get the width of the top-left corner of the detector."""
        return self._w

    @property
    def w(self) -> int:
        """Get the width of the top-left corner of the detector."""
        return self._w

    @property
    def height(self) -> int:
        """Get the height of the top-left corner of the detector."""
        return self._h

    @property
    def h(self) -> int:
        """Get the height of the top-left corner of the detector."""
        return self._h

    @property
    def count(self) -> int:
        """Get the count currently displayed on the detector."""
        return self._count

    @property
    def color(self) -> int:
        """Get the 32-bit sRGB color of the detector."""
        return self._color


class Button:
    """A button, which when clicked enough can activate something."""

    def __init__(
        self, x: int, y: int, w: int, h: int,
        count: int, color: int, last_click: t.Optional[float],
    ):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._count = count
        self._color = color
        self._lastclick = last_click

    @property
    def x(self) -> int:
        """Get the X coordinate of the top-left corner of the button."""
        return self._x

    @property
    def y(self) -> int:
        """Get the Y coordinate of the top-left corner of the button."""
        return self._y

    @property
    def width(self) -> int:
        """Get the width of the current button."""
        return self._w

    @property
    def w(self) -> int:
        """Alias for width."""
        return self._w

    @property
    def height(self) -> int:
        """Get the height of the current button."""
        return self._h

    @property
    def h(self) -> int:
        """Alias for height."""
        return self._h

    @property
    def count(self) -> int:
        """Get the count currently displayed on the button."""
        return self._count

    @property
    def color(self) -> int:
        """Get the 32-bit sRGB color of the detector."""
        return self._color

    @property
    def last_click(self) -> t.Optional[float]:
        """Get the monotonic timestamp of last click."""
        return self._lastclick

    @property
    def pressed(self) -> bool:
        """Get whether the button is currently pressed or not."""
        return (
            self._lastclick is not None
            and (monotonic() - self._lastclick) < .150
        )


class Cursor:
    """A cursor, which represents another player."""

    def __init__(
        self, start_time: float,
        old_x: int, old_y: int,
        new_x: int, new_y: int,
    ):
        self._start = start_time
        self._current = start_time
        self._oldx = old_x
        self._oldy = old_y
        self._newx = new_x
        self._newy = new_y

    @property
    def advancement(self) -> float:
        """Get the advancement from 0 to 1 of the cursor offline vector."""
        elapsed = self._current - self._start
        anim_start = 0.0
        anim_end = 0.1

        value = (anim_end - elapsed) / (anim_end - anim_start)
        return 1 - min(max(value, 0.0), 1.0)

    @property
    def x(self) -> int:
        """Get the X coordinate of the cursor."""
        return int(self._oldx + (self._newx - self._oldx) * self.advancement)

    @property
    def y(self) -> int:
        """Get the Y coordinate of the cursor."""
        return int(self._oldy + (self._newy - self._oldy) * self.advancement)

    def set_current_time(self, value: float) -> None:
        """Set the current time for defining the animation advancement."""
        self._current = value


class DrawnLine:
    """A drawn line by a player."""

    def __init__(
        self, start_time: float,
        start_x: int, start_y: int, end_x: int, end_y: int,
    ):
        self._start = start_time
        self._current = start_time
        self._sx = start_x
        self._sy = start_y
        self._ex = end_x
        self._ey = end_y

    @property
    def alpha(self) -> float:
        """Get the current alpha value, from 0 to 1."""
        elapsed = self._current - self._start
        fading_start = 0.0
        fading_end = 5.0

        value = (fading_end - elapsed) / (fading_end - fading_start)
        return min(max(value, 0.0), 1.0)

    @property
    def start_x(self) -> int:
        """Get the X coordinate of the starting position."""
        return self._sx

    @property
    def start_y(self) -> int:
        """Get the Y coordinate of the starting position."""
        return self._sy

    @property
    def end_x(self) -> int:
        """Get the X coordinate of the ending position."""
        return self._ex

    @property
    def end_y(self) -> int:
        """Get the Y coordinate of the ending position."""
        return self._ey

    def set_current_time(self, value: float) -> None:
        """Set the current monotonic timestamp for defining current alpha."""
        self._current = value

    def has_faded(self) -> bool:
        """Get whether the line has completely faded or not."""
        return self.alpha == 0.0


class Click:
    """A click, i.e. a visual representation of a player clicking."""

    def __init__(self, start_time: float, x: int, y: int):
        self._start = start_time
        self._current = start_time
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        """Get the current X coordinate."""
        return self._x

    @property
    def y(self) -> int:
        """Get the current Y coordinate."""
        return self._y

    @property
    def advancement(self) -> float:
        """Get the advancement of the current animation from 0 to 1."""
        elapsed = self._current - self._start
        fading_start = 0.0
        fading_end = 0.5

        value = (fading_end - elapsed) / (fading_end - fading_start)
        return 1 - min(max(value, 0.0), 1.0)

    @property
    def radius(self) -> int:
        """Get the current radius."""
        return int(25 * self.advancement)

    @property
    def alpha(self) -> float:
        """Get the current alpha value."""
        return 1.0 - self.advancement

    def set_current_time(self, value: float) -> None:
        """Set the current montonic timestamp for defining advancement."""
        self._current = value

    def has_faded(self) -> bool:
        """Get whether the click animation has faded or not."""
        return self.advancement == 1.0


class GameState:
    """An object managing a game through a client and local interactions."""

    def __init__(self, client: GameClient, border_size: int = 10):
        self._width = 800 + border_size * 2
        self._height = 600 + border_size * 2
        self._border_size = border_size
        self._client = client

        self._levelid = 0
        self._playerid = 0
        self._playercount = 0
        self._position = (0, 0)
        self._objects: t.Dict[int, t.Union[
            Text, Wall, Warp, Detector, Button,
        ]] = {}
        self._cursors: t.Dict[int, Cursor] = {}
        self._lines: t.List[DrawnLine] = []
        self._clicks: t.List[Click] = []
        self._deathcount = 0

    @property
    def width(self) -> int:
        """Get the width of the current canvas."""
        return self._width

    @property
    def height(self) -> int:
        """Get the height of the current canvas."""
        return self._height

    @property
    def border_size(self) -> int:
        """Get the current border size."""
        return self._border_size

    @property
    def player_id(self) -> int:
        """Get the identifier of the current player."""
        return self._playerid

    @property
    def player_count(self) -> int:
        """Get the current player count."""
        return self._playercount

    @property
    def position(self) -> t.Tuple[int, int]:
        """Get the current player position."""
        return self._position

    @property
    def objects(self) -> t.Iterator[t.Union[
        Text, Wall, Warp, Button, Detector,
    ]]:
        """Iterate over level objects."""
        sw, sh = self.width, self.height
        b = self._border_size

        # First, yield the border, as the following walls:
        #
        #    1111111111
        #    3        4
        #    3        4
        #    3        4
        #    2222222222
        #
        yield Wall(0, 0, sw, b)
        yield Wall(0, sh - b, sw, b)
        yield Wall(0, b, b, sh - b - b)
        yield Wall(sw - b, b, b, sh - b - b)

        # Then yield the 'real' objects.
        for obj in self._objects.values():
            yield obj

    @property
    def drawn_lines(self) -> t.Iterator[DrawnLine]:
        """Iterate over drawn lines."""
        curtime = monotonic()
        for line in list(self._lines):
            line.set_current_time(curtime)
            if line.has_faded():
                self._lines.remove(line)
                continue

            yield line

    @property
    def clicks(self) -> t.Iterator[Click]:
        """Iterate over clicks."""
        curtime = monotonic()
        for click in list(self._clicks):
            click.set_current_time(curtime)
            if click.has_faded():
                self._clicks.remove(click)
                continue

            yield click

    @property
    def cursors(self) -> t.Iterator[Cursor]:
        """Iterate over cursors."""
        curtime = monotonic()
        for cursor in self._cursors.values():
            cursor.set_current_time(curtime)
            yield cursor

    def handle_packet(self, packet: ServerPacket) -> None:
        """Handle the provided packet."""
        off_x = self._border_size
        off_y = self._border_size
        curtime = monotonic()

        if packet.type_ == ServerPacketType.LEVEL_LOAD:
            self._cursors = {}
            self._objects = {}
            self._lines = []
            self._clicks = []

        if packet.player_count is not None:
            self._playercount = packet.player_count

        if packet.player_id is not None:
            self._playerid = packet.player_id

        if packet.player_placement is not None:
            self._position = (
                packet.player_placement.x,
                packet.player_placement.y,
            )

        if packet.player_death_count is not None:
            self._deathcount = packet.player_death_count

        if packet.level_id is not None:
            self._levelid = packet.level_id

        if packet.cursors is not None:
            cursor_ids = set(self._cursors.keys())
            for obj in packet.cursors:
                id_ = obj.id_
                if id_ == self._playerid:
                    continue

                cursor_ids.discard(id_)
                x, y = obj.x + off_x, obj.y + off_y

                cursor = self._cursors.get(id_)
                if cursor is not None:
                    ox, oy = cursor.x, cursor.y
                else:
                    ox, oy = x, y

                self._cursors[id_] = Cursor(curtime, ox, oy, x, y)

            for cursor_id in cursor_ids:
                del self._cursors[cursor_id]

        if packet.removed_cursors is not None:
            for iobj in packet.removed_cursors:
                if iobj.id_ in self._cursors:
                    del self._cursors[iobj.id_]

        if packet.clicks is not None:
            for pos in packet.clicks:
                x, y = pos.x + off_x, pos.y + off_y
                self._clicks.append(Click(curtime, x, y))

        if packet.shapes is not None:
            for shape in packet.shapes:
                previous = self._objects.get(shape.id_, None)

                if shape.type_ == ShapeType.TO_DELETE:
                    # This object is ignored in the original script.
                    # Just to be sure, let's delete this object if it exists.
                    if shape.id_ in self._objects:
                        del self._objects[shape.id_]
                elif shape.type_ == ShapeType.TEXT:
                    if (
                        shape.size is None or shape.centered is None
                        or shape.text is None
                    ):
                        raise ValueError('Missing property for text')

                    self._objects[shape.id_] = Text(
                        shape.x + off_x, shape.y + off_y,
                        shape.size, shape.centered,
                        shape.text,
                    )
                elif shape.type_ == ShapeType.WALL:
                    if (
                        shape.w is None or shape.h is None
                        or shape.color is None
                    ):
                        raise ValueError('Missing property for wall')

                    r, g, b = shape.color

                    self._objects[shape.id_] = Wall(
                        shape.x + off_x, shape.y + off_y,
                        shape.w, shape.h,
                        (r, g, b, 0),
                    )
                elif shape.type_ == ShapeType.WARP:
                    if shape.w is None or shape.h is None or shape.bad is None:
                        raise ValueError('Missing property for warp')

                    self._objects[shape.id_] = Warp(
                        shape.x + off_x, shape.y + off_y,
                        shape.w, shape.h, shape.bad,
                    )
                elif shape.type_ == ShapeType.DETECTOR:
                    if (
                        shape.w is None or shape.h is None
                        or shape.count is None or shape.color is None
                    ):
                        raise ValueError('Missing property for detector')

                    r, g, b = shape.color
                    rgb = (r << 16) | (g << 8) | b

                    self._objects[shape.id_] = Detector(
                        shape.x + off_x, shape.y + off_y,
                        shape.w, shape.h, shape.count, rgb,
                    )
                elif shape.type_ == ShapeType.BUTTON:
                    if (
                        shape.w is None or shape.h is None
                        or shape.color is None or shape.count is None
                    ):
                        raise ValueError('Missing property for button')

                    last_click = None
                    if previous is not None:
                        if not isinstance(previous, Button):
                            raise ValueError(
                                f'Object with id {shape.id_} has changed '
                                + f'from {previous!r} to Button',
                            )

                        last_click = previous.last_click
                        if (
                            previous.count is not None
                            and previous.count > shape.count
                        ):
                            last_click = curtime

                    r, g, b = shape.color
                    rgb = (r << 16) | (g << 8) | b

                    self._objects[shape.id_] = Button(
                        shape.x + off_x, shape.y + off_y,
                        shape.w, shape.h,
                        shape.count, rgb, last_click,
                    )

        if packet.lines is not None:
            for vec in packet.lines:
                sx, sy = vec.start_x + off_x, vec.start_y + off_y
                ex, ey = vec.end_x + off_x, vec.end_y + off_y
                self._lines.append(DrawnLine(curtime, sx, sy, ex, ey))

    def set_position(self, x: int, y: int) -> t.Tuple[int, int]:
        """Set the position.

        This function returns the updated position that have been
        calculated locally using collisions.
        """
        ox, oy = self._position
        px, py = x, y
        fx, fy = x, y

        # Define the internal functions.

        def dst(x: float, y: float) -> float:
            """Get the distance between the origin and the given point.

            Makes use of Pythagora's theorem.
            """
            nonlocal ox, oy

            return sqrt(abs(ox - x) ** 2 + abs(oy - y) ** 2)

        def project_y(new_x: int) -> int:
            """Get the projected Y coordinate.

            Get the y coordinate of the first point to encounter
            the vertical line determined by the ``new_x`` abscissa,
            on the OP vector, where O has the (ox, oy) coordinates
            and P has the (px, py) coordinates.

            This formula uses Thales' theorem, and is based on
            the fact that there is an intersection; this should
            be checked beforehand.
            """
            nonlocal ox, oy, px, py

            return int(oy + (oy - py) * (new_x - ox) / (px - ox))

        def project_x(new_y: int) -> int:
            """Get the projected X coordinate.

            Get the x coordinate of the first point to encounter
            the horizontal line determined by the ``new_y`` ordinate,
            on the OP vector, where O has the (ox, oy) coordinates
            and P has the (px, py) coordinates.

            Roughly the equivalent of the ``project_y`` function.
            """
            nonlocal ox, oy, px, py

            return int(ox + (ox - px) * (new_y - oy) / (py - oy))

        # First of all, we want to check if the point is within the
        # bounds of the map.
        new_x = None
        if fx < 0:
            new_x = 0
        elif fx >= self._width:
            new_x = self._width - 1

        if new_x is not None:
            fx = new_x
            fy = project_y(fx)

        new_y = None
        if fy < 0:
            new_y = 0
        elif fy >= self._height:
            new_y = self._height - 1

        if new_y is not None:
            fy = new_y
            fx = project_x(fy)

        # Check with all of the walls.
        fdst = dst(fx, fy)

        for wall in self.objects:
            if not isinstance(wall, Wall):
                continue

            # First, let's check horizontally.
            new_x = None
            if ox < px and ox < wall.x:
                new_x = wall.x - 1
            elif ox > px and ox > wall.x + wall.w - 1:
                new_x = wall.x + wall.w

            if new_x is not None:
                # Calculate the projected y coordinates using Thales' theorem,
                # and check if it's within the shape.
                new_y = project_y(new_x)
                if new_y in range(wall.y, wall.y + wall.h):
                    new_dst = dst(new_x, new_y)
                    if new_dst < fdst:
                        fx, fy, fdst = new_x, new_y, new_dst

            # Then, even if the horizontal checks did pass, let's
            # check vertically.
            new_y = None
            if oy < py and oy < wall.y:
                new_y = wall.y - 1
            elif oy > py and oy > wall.y + wall.h - 1:
                new_y = wall.y + wall.h

            if new_y is not None:
                # Calculate the projected x coordinate using Thales' theorem,
                # the same way we have done it with x.
                new_x = project_x(new_y)
                if new_x in range(wall.x, wall.x + wall.w):
                    new_dst = dst(new_x, new_y)
                    if new_dst < fdst:
                        fx, fy, fdst = new_x, new_y, new_dst

        # Okay, set the new position.
        self._position = (fx, fy)
        return (fx, fy)

    async def send_mouse_position(self) -> None:
        """Send the current mouse position."""
        x, y = self.position
        x, y = x - self._border_size, y - self._border_size
        if x not in range(0, 800) or y not in range(0, 600):
            return

        await self._client.send_mouse_position(x, y, self._levelid)

    async def send_mouse_click(self) -> None:
        """Send a mouse click on the current position."""
        x, y = self.position
        x, y = x - self._border_size, y - self._border_size
        if x not in range(0, 800) or y not in range(0, 600):
            return

        await self._client.send_mouse_click(x, y, self._levelid)

    async def send_line(self, origin_pos: t.Tuple[int, int]) -> None:
        """Send a line from the last position to the current position."""
        x, y = self.position
        x, y = x - self._border_size, y - self._border_size
        if x not in range(0, 800) or y not in range(0, 600):
            return

        ox, oy = origin_pos
        ox, oy = ox - self._border_size, oy - self._border_size
        if ox not in range(0, 800) or oy not in range(0, 600):
            return

        if ox == x and oy == y:
            return

        await self._client.send_line(ox, oy, x, y)

    async def handle_packets(self) -> t.AsyncIterator[t.Tuple[bool]]:
        """Handle received packets."""
        async for packet in self._client.recv():
            self.handle_packet(packet)
            is_position_set = packet.type_ in (
                ServerPacketType.LEVEL_LOAD,
                ServerPacketType.PLAYER,
            )

            yield (is_position_set,)


@asynccontextmanager
async def create_game_state(url: str) -> t.AsyncIterator[GameState]:
    """Get the game client connected to a URL.

    :param url: The URL to connect to, starting with 'ws://' or 'wss://'.
    """
    async with create_client(url) as client:
        yield GameState(client)
