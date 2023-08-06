#!/usr/bin/env python3
# ****************************************************************************
# Copyright (C) 2022 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pycursorsio project, which is MIT-licensed.
# ****************************************************************************
"""Protocol client for the cursors.io game."""

import typing as t
from contextlib import asynccontextmanager
from enum import Enum
from logging import getLogger
from struct import calcsize, pack, unpack_from

from websockets.legacy.client import (
    WebSocketClientProtocol, connect as connect_ws,
)

from .utils import log_data

__all__ = [
    'GameClient', 'ServerPacket', 'ServerPacketType', 'Shape',
    'ShapeType', 'create_client',
]

_logger = getLogger(__name__)


class ShapeType(Enum):
    """Shape type."""

    TEXT = 0
    WALL = 1
    WARP = 2
    DETECTOR = 3
    BUTTON = 4
    TO_DELETE = 255


class Vector:
    """Vector with start and end coordinates."""

    start_x: int
    """The starting X coordinate."""

    start_y: int
    """The starting Y coordinate."""

    end_x: int
    """The ending X coordinate."""

    end_y: int
    """The ending Y coordinate."""


class Placement:
    """Coordinates for placing something."""

    x: int
    """The X coordinate for the object."""

    y: int
    """The Y coordinate for the object."""


class Object:
    """Object with an identifier."""

    id_: int
    """The object identifier."""


class PlacedObject(Object, Placement):
    """Object with an identifier and coordinates."""

    pass


class Shape(PlacedObject):
    """Shape."""

    type_: ShapeType
    """Raw shape type."""

    w: t.Optional[int] = None
    """The width of the shape."""

    h: t.Optional[int] = None
    """The height of the shape."""

    color: t.Optional[t.Tuple[int, int, int]] = None
    """The color of the shape."""

    count: t.Optional[int] = None
    """The count currently displayed on a warp."""

    bad: t.Optional[bool] = None
    """Whether the warp is bad or not."""

    size: t.Optional[int] = None
    """The size of the text."""

    centered: t.Optional[bool] = None
    """Whether the text is centered around its coordinates or not."""

    text: t.Optional[str] = None
    """Text placed within the shape."""


class ServerPacketType(Enum):
    """Packet type identifier."""

    PLAYER_ID = 0
    GAME_STATUS = 1
    LEVEL_LOAD = 4
    PLAYER = 5


class ServerPacket:
    """Server packet."""

    __slots__ = (
        'type_', 'player_count', 'player_id', 'player_placement',
        'player_death_count', 'level_id', 'cursors', 'clicks',
        'removed_cursors', 'shapes', 'lines',
    )

    type_: ServerPacketType
    """Type of packet."""

    player_count: t.Optional[int]
    """The current player count.

    Set for GAME_STATUS packets.
    """

    player_id: t.Optional[int]
    """The identifier of the player.

    Set for PLAYER_ID packets.
    """

    player_placement: t.Optional[Placement]
    """Current placement for the player.

    Set for LEVEL_LOAD and PLAYER packets.
    """

    player_death_count: t.Optional[int]
    """Current death count for the player.

    Set for the PLAYER packets.
    """

    level_id: t.Optional[int]
    """Identifier of the level.

    Set for the LEVEL_LOAD packets.
    """

    cursors: t.Optional[t.Sequence[PlacedObject]]
    """Cursors to place.

    Set for the GAME_STATUS packets.
    """

    removed_cursors: t.Optional[t.Sequence[Object]]
    """Cursors to remove.

    Set for the GAME_STATUS packets.
    """

    clicks: t.Optional[t.Sequence[Placement]]
    """Newly placed clicks.

    Set for the GAME_STATUS packets.
    """

    shapes: t.Optional[t.Sequence[Shape]]
    """Shapes to update or place.

    Set for the GAME_STATUS and LEVEL_LOAD packets.
    """

    lines: t.Optional[t.Sequence[Vector]]
    """New lines to draw.

    Set for the GAME_STATUS packets.
    """

    def __init__(self):
        self.player_count = None
        self.player_id = None
        self.player_placement = None
        self.player_death_count = None
        self.level_id = None
        self.cursors = None
        self.removed_cursors = None
        self.clicks = None
        self.shapes = None
        self.lines = None


class _BufferUnpacker:
    """Object to unpack raw data."""

    def __init__(self, buf: bytes):
        self.buf = buf
        self.offset = 0

    def unpack(self, fmt: str) -> t.Tuple:
        """Unpack elements from the given format."""
        fmt = '<' + fmt

        length = calcsize(fmt)
        left = len(self.buf) - self.offset
        if left < length:
            raise ValueError(f'Expected {length} bytes, only got {left}')

        results = unpack_from(fmt, buffer=self.buf, offset=self.offset)
        self.offset += length
        return results

    def get_text(self) -> str:
        """Get an ASCII string."""
        offset = self.offset
        result = self.buf.find(b'\0', offset)
        if result < 0:
            self.offset = len(self.buf)
            return self.buf[offset:].decode('ascii')

        self.offset = result + 1
        return self.buf[offset:result].decode('ascii')

    def get_color(self) -> t.Tuple[int, int, int]:
        """Get an sRGB color."""
        x, = self.unpack('L')
        return ((x >> 16) & 255, (x >> 8) & 255, x & 255)


class GameClient:
    """Manages the local game state."""

    def __init__(self, ws: WebSocketClientProtocol):
        self.ws = ws

    def extract_shapes(self, buf: _BufferUnpacker) -> t.Sequence[Shape]:
        """Extract shapes from raw data.."""
        shape_count, = buf.unpack('H')
        shapes = []

        for _ in range(shape_count):
            shape = Shape()
            shape.id_, raw_type = buf.unpack('LB')

            try:
                shape.type_ = ShapeType(raw_type)
            except ValueError:
                raise AssertionError(f'Unknown shape type: {raw_type}')

            if shape.type_ == ShapeType.TO_DELETE:
                pass
            elif shape.type_ == ShapeType.TEXT:
                x, y, shape.size, cent = buf.unpack('HHBB')
                shape.x, shape.y = x * 2, y * 2
                shape.centered = cent != 0
                shape.text = buf.get_text()
            elif shape.type_ == ShapeType.WALL:
                x, y, w, h = buf.unpack('HHHH')
                shape.x, shape.y = x * 2, y * 2
                shape.w, shape.h = w * 2, h * 2
                shape.color = buf.get_color()
            elif shape.type_ == ShapeType.WARP:
                x, y, w, h, bad = buf.unpack('HHHHB')
                shape.x, shape.y = x * 2, y * 2
                shape.w, shape.h = w * 2, h * 2
                shape.bad = bad != 0
            elif shape.type_ == ShapeType.DETECTOR:
                x, y, w, h = buf.unpack('HHHH')
                shape.x, shape.y = x * 2, y * 2
                shape.w, shape.h = w * 2, h * 2
                shape.count, = buf.unpack('H')
                shape.color = buf.get_color()
            elif shape.type_ == ShapeType.BUTTON:
                x, y, w, h = buf.unpack('HHHH')
                shape.x, shape.y = x * 2, y * 2
                shape.w, shape.h = w * 2, h * 2
                shape.count, = buf.unpack('H')
                shape.color = buf.get_color()
            else:
                raise AssertionError(f'Unhandled shape type: {shape.type_}')

            shapes.append(shape)

        return shapes

    def extract_packet(self, buf: _BufferUnpacker) -> ServerPacket:
        """Extract a packet from raw data."""
        packet = ServerPacket()
        raw_type, = buf.unpack('B')

        try:
            packet.type_ = ServerPacketType(raw_type)
        except ValueError:
            raise AssertionError(f'Unknown packet type: {raw_type}')

        if packet.type_ == ServerPacketType.PLAYER_ID:
            packet.player_id, = buf.unpack('L')
        elif packet.type_ == ServerPacketType.GAME_STATUS:
            cursor_count, = buf.unpack('H')
            packet.cursors = []
            for _ in range(cursor_count):
                cursor = PlacedObject()
                cursor.id_, x, y = buf.unpack('LHH')
                cursor.x, cursor.y = x * 2, y * 2
                packet.cursors.append(cursor)

            click_count, = buf.unpack('H')
            packet.clicks = []
            for _ in range(click_count):
                click = Placement()
                x, y = buf.unpack('HH')
                click.x, click.y = x * 2, y * 2
                packet.clicks.append(click)

            removed_cursor_count, = buf.unpack('H')
            packet.removed_cursors = []
            for _ in range(removed_cursor_count):
                removed_cursor = Object()
                removed_cursor.id_, = buf.unpack('L')
                packet.removed_cursors.append(removed_cursor)

            packet.shapes = self.extract_shapes(buf)

            line_count, = buf.unpack('H')
            packet.lines = []
            for _ in range(line_count):
                line = Vector()
                sx, sy = buf.unpack('HH')
                ex, ey = buf.unpack('HH')

                line.start_x, line.start_y = sx * 2, sy * 2
                line.end_x, line.end_y = ex * 2, ey * 2
                packet.lines.append(line)

            try:
                packet.player_count, = buf.unpack('L')
            except ValueError:
                packet.player_count = 0
        elif packet.type_ == ServerPacketType.LEVEL_LOAD:
            placement = Placement()
            x, y = buf.unpack('HH')
            placement.x, placement.y = x * 2, y * 2
            packet.player_placement = placement
            packet.shapes = self.extract_shapes(buf)

            try:
                packet.level_id, = buf.unpack('L')
            except ValueError:
                packet.level_id, = buf.unpack('H')
        elif packet.type_ == ServerPacketType.PLAYER:
            placement = Placement()
            x, y = buf.unpack('HH')
            placement.x, placement.y = x * 2, y * 2
            packet.player_placement = placement

            try:
                packet.player_death_count, = buf.unpack('L')
            except ValueError:
                packet.player_death_count, = buf.unpack('H')
        else:
            raise AssertionError(f'Unhandled packet type: {packet.type_}')

        return packet

    async def send_packet(self, data: bytes) -> None:
        """Send a raw packet through the websocket."""
        _logger.debug('Sending the following packet:')
        log_data(_logger, data)
        await self.ws.send(data)

    async def send_mouse_position(self, x: int, y: int, level_id: int) -> None:
        """Send a client packet to move our cursor."""
        packet = pack('<BHHL', 1, x // 2, y // 2, level_id)
        await self.send_packet(packet)

    async def send_mouse_click(self, x: int, y: int, level_id: int) -> None:
        """Send a client packet to click."""
        packet = pack('<BHHL', 2, x // 2, y // 2, level_id)
        await self.send_packet(packet)

    async def send_line(
        self, start_x: int, start_y: int, end_x: int, end_y: int,
    ) -> None:
        """Send a client packet to draw a line."""
        packet = pack('<BHHHH', 3, start_x, start_y, end_x, end_y)
        await self.send_packet(packet)

    async def recv(self) -> t.AsyncIterator[ServerPacket]:
        """Receive messages as an synchronous iterator."""
        while True:
            data = await self.ws.recv()
            if isinstance(data, str):
                data = data.encode()

            _logger.debug('Received the following packet:')
            log_data(_logger, data)
            yield self.extract_packet(_BufferUnpacker(data))


@asynccontextmanager
async def create_client(url: str) -> t.AsyncIterator[GameClient]:
    """Get the game client connected to a URL.

    :param url: The URL to connect to, starting with 'ws://' or 'wss://'.
    """
    async with connect_ws(url) as ws:
        yield GameClient(ws)
