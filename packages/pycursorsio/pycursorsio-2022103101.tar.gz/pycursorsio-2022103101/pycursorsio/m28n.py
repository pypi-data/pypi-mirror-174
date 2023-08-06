#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2021-2022 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pycursorsio project, which is MIT-licensed.
# *****************************************************************************
"""M28 Network API.

Client for the M28 network API, for gathering the servers' IP addresses for
given game servers.
"""

import typing as t
from asyncio import FIRST_COMPLETED, wait as wait_async

from aiohttp import ClientSession

from websockets.legacy.client import connect as connect_ws

__all__ = ['M28NAPI', 'M28NServer', 'M28NError']


class M28NError(Exception):
    """An error from the M28N API."""

    def __init__(self, message: t.Optional[str]):
        self._message = message

    def __str__(self):
        return self._message


class M28NServer:
    """A server as seen by the M28 API.

    The data are the following:

    ``id``
        The ID of the server, which can lead to the server's domain
        as ``<theid>.s.m28n.net``. Serves for secure connections, where
        the server name is required.

    ``region_name``
        The name of the region in which the server is located. This
        is used for latency calculations, in order to find out which
        server is the "closest" or the one that performs best for the
        client.

    ``ipv4``
        The IP version 4 address of the server, for direct accessing.
        Why not use the domain of the server, you may ask? Probably for
        obfuscating this to the client which goes into their browser
        inspector to find out which server is being used.
        It's called "Security through obscurity", and it's not recommended.

    ``ipv6``
        The IP version 6 address of the server, for direct accessing.
        Same as above, although bear in mind that some servers may not
        have any IPv6 address!
    """

    def __init__(
        self, id_: t.Optional[str], region_name: t.Optional[str],
        ipv4: t.Optional[str], ipv6: t.Optional[str],
    ):
        self._id = id_
        self._region_name = region_name
        self._ipv4 = ipv4
        self._ipv6 = ipv6

    def __repr__(self):
        attrs = ('domain', 'region_name', 'ipv4', 'ipv6')
        attrs = ', '.join(f'{n}={getattr(self, n)!r}' for n in attrs)
        return f'{self.__class__.__name__}({attrs})'

    @property
    def id_(self) -> t.Optional[str]:
        """Get the identifier for the M28 server."""
        return self._id

    @property
    def domain(self) -> t.Optional[str]:
        """Get the domain name for the M28 server."""
        if self.id_ is None:
            return None
        return f'{self.id_}.s.m28n.net'

    @property
    def region_name(self) -> t.Optional[str]:
        """Get the region name for the M28 server."""
        return self._region_name

    @property
    def ipv4(self) -> t.Optional[str]:
        """Get the IPv4 address for the M28 server."""
        return self._ipv4

    @property
    def ipv6(self) -> t.Optional[str]:
        """Get the IPv6 address for the M28 server."""
        return self._ipv6


class M28NAPI:
    """M28 API client.

    Can return servers owned by the M28 company for its different games.
    """

    def __init__(self, base_url: str = 'https://api.n.m28.io'):
        self._base = base_url

    def __repr__(self):
        return f'{self.__class__.__name__}(base_url={self.base_url!r})'

    @property
    def base_url(self) -> str:
        """Get the base URL for the M28 Network API client."""
        return self._base

    async def get_server(self, id_: str) -> M28NServer:
        """Get the data of the given server."""
        url = f'{self._base}/server/{id_}'

        async with ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                if response.status not in range(200, 300):
                    raise M28NError(data.get(
                        'error',
                        f'Non 2xx status code ({response.status})',
                    ))

                return M28NServer(
                    data.get('id'),
                    None,
                    data.get('ipv4'),
                    data.get('ipv6'),
                )

    async def find_servers(
        self, endpoint: str,
        version: t.Optional[str] = None,
    ) -> t.AsyncIterator[M28NServer]:
        """Find a list of servers for the given endpoint.

        Known endpoints are:

        ``latency``
            Latency servers, for evaluating the speed towards
            various regions.

        ``cursors``
            Servers for the cursors.io game.

        ``diepio-<mode>``
            Servers with various gameplays for the diep.io game, with <mode>
            being 'ffa', 'survival', 'teams', '4teams', 'dom', 'tag',
            'maze' or 'sandbox'.

        ``florrio``
            Servers for the florr.io game.

        ``digdig-<mode>``
            Servers for the digdig.io game, with <mode> being 'ffa', 'teams',
            'tag', 'br' or 'maze'.
        """
        url = f'{self._base}/endpoint/{endpoint}/findEach/'
        if version is not None:
            url += f'?version={version}'

        async with ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                if response.status not in range(200, 300):
                    raise M28NError(
                        f'on endpoint {endpoint!r}: '
                        + data.get(
                            'error',
                            f'got {response.status} status code',
                        ),
                    )

                # If the endpoint doesn't exist, there isn't any
                # "servers" member in the result.
                if 'servers' not in data:
                    return

                for server_name, server in data['servers'].items():
                    yield M28NServer(
                        server.get('id'),
                        server_name,
                        server.get('ipv4'),
                        server.get('ipv6'),
                    )

    async def find_server_preference(
        self, endpoint: str,
        secure: bool = True,
        probes: int = 10,
        timeout: t.Optional[t.Union[int, float]] = None,
        version: t.Optional[str] = None,
    ) -> t.Optional[M28NServer]:
        """Find the best suited server using the M28 method.

        Said method is the following:

        * Get the list of all servers for the given endpoint.
        * Get the list of 'latency' servers representing their
          regions (with the same region names as the ones for
          the given endpoint).
        * Ping the list of the used 'latency' servers until a
          certain amount of exchanges (send/receive pairs)
          have been made.
        * Return the server for which the representative
          'legacy' server has finished the exchanges first.
        """
        if not isinstance(probes, int) or probes <= 0:
            raise ValueError('probes: expected an integer > 0')
        if timeout is None:
            if secure:
                timeout = 7000
            else:
                timeout = 5000
        elif not isinstance(timeout, int) or timeout <= 0:
            raise ValueError('timeout: expected None or an integer > 0')
        if not isinstance(secure, bool):
            raise ValueError('secure: expected a boolean')

        # Get the servers for the endpoint.
        servers = [
            server
            async for server in self.find_servers(endpoint, version=version)
        ]

        if not servers:
            # We don't have any servers corresponding to that endpoint!
            # We cannot choose among zero servers, so we'll return None.
            return None

        if len(servers) == 1:
            # We only have one server, so no need to compare the servers.
            return servers[0]

        # Let's get the corresponding latency servers.
        servers_by_region_name = {
            server.region_name: server
            for server in servers
        }
        latency_servers = [
            server
            async for server in self.find_servers('latency')
            if server.region_name is not None
            and server.region_name in servers_by_region_name
        ]

        if not latency_servers:
            # No latency servers available for the regions
            # referenced in the endpoint servers!
            # We'll just return the first server we've got.
            return servers[0]

        if len(latency_servers) == 1:
            region_name = latency_servers[0].region_name
            if region_name is not None:
                # We've only got the latency server for one server,
                # so any comparison is pointless! Let's just
                # return the corresponding server, it should be
                # good enough.
                return next(
                    server for server in servers
                    if server.region_name == region_name
                )

        # Well, it seems that we have at least two latency servers
        # corresponding to our cases!
        max_probes = probes
        probes_by_region = {
            region_name: 0
            for region_name in servers_by_region_name.keys()
        }

        async def update_server_score(server: M28NServer) -> None:
            nonlocal probes_by_region

            url = 'wss://' if secure else 'ws://'
            if server.domain is not None:
                url += server.domain
            elif server.ipv4 is not None:
                url += server.ipv4
            elif server.ipv6 is not None:
                url += '[' + server.ipv6 + ']'
            else:
                # No IP address to reach.
                return

            url += '/'

            async with connect_ws(url) as ws:
                probes = 0
                while True:
                    await ws.send(b'\0')
                    msg = await ws.recv()
                    if msg[0] != 0:
                        continue

                    probes += 1
                    probes_by_region[server.region_name] = probes
                    if probes == max_probes:
                        return

        _, pending = await wait_async(
            [update_server_score(server) for server in latency_servers],
            timeout=timeout,
            return_when=FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

        # Get the winning server!
        winning_region_name = sorted(
            probes_by_region.items(),
            key=lambda x: -x[1],
        )[0][0]

        return servers_by_region_name[winning_region_name]
