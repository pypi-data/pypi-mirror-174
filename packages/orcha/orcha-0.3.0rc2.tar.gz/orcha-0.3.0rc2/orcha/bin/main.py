#                                   MIT License
#
#              Copyright (c) 2021 Javier Alonso <jalonso@teldat.com>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#      copies of the Software, and to permit persons to whom the Software is
#            furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
#                 copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#                                    SOFTWARE.
"""
Main application entry point. Here, a single method is exposed which prepares
the environment for running the application with the installed plugins. Notice
that `orcha.main` won't work if no plugin is installed. For more information,
see: :class:`BasePlugin`.
"""
import argparse
import errno
import multiprocessing
import sys

import orcha.properties

from ..plugins import ListPlugin, query_plugins
from ..utils.logging_utils import get_logger
from ..utils.packages import version

# application universal logger
log = get_logger()


def main():
    """Main application entry point. Multiple arguments are defined which allows
    further customization of the server/client process:

    --listen-address ADDRESS  defines the IP address used when serving/connecting the
                              application. By default, it is ``127.0.0.1``.
    --port N                  indicates which port is used during communication.
                              By default, it is **50000**.
    --key KEY                 defines the authentication key used during communication.
                              This field is not mandatory but **it is recommended to define it**
                              as it will be necessary for other processes to communicate with the
                              service itself.

    The application automatically detects the plugins that are installed in the system. It
    is important that the installed plugins follows the name convention in order to be
    correctly identified. In other case, the subcommands won't appear here. For more
    details, see :class:`BasePlugin`.

    Returns:
        int: execution return code. Multiple return codes are possible:

              + ``0`` means that the execution was successful.
              + ``1`` refers to a standard error happened during execution.
              + ``127`` indicates that no plugins were found or no plugins
                can handle the parsed command line options.

    .. versionchanged:: 0.1.11
        + ``key`` parameter is now required, the internally generated one won't be used anymore.
        + Orcha clients in Python <= 3.7 now have their internal digest fixed, not throwing an
          exception anymore.

    .. versionchanged:: 0.1.12
        + ``key`` parameter is not mandatory (again) - some plugins may not require it for
          their basic functionality.
    """
    parser = argparse.ArgumentParser(
        description="Orcha command line utility for handling services",
        prog="orcha",
    )
    parser.add_argument(
        "--listen-address",
        metavar="ADDRESS",
        type=str,
        default="127.0.0.1",
        help="Listen address of the service",
    )
    parser.add_argument(
        "--port",
        metavar="N",
        type=int,
        default=50000,
        help="Listen port of the service",
    )
    parser.add_argument(
        "--key",
        metavar="KEY",
        type=str,
        default=None,
        help="Authentication key used for verifying clients",
    )
    parser.add_argument("--version", action="version", version=f"orcha - {version('orcha')}")
    subparsers = parser.add_subparsers(
        title="available commands",
        required=True,
        metavar="command",
    )

    discovered_plugins = query_plugins()
    plugins = [plugin(subparsers) for plugin in discovered_plugins]

    # add our embedded ListPlugin to the list of available plugins
    plugins.append(ListPlugin(subparsers))

    args: argparse.Namespace = parser.parse_args()
    orcha.properties.listen_address = args.listen_address
    orcha.properties.port = args.port
    if args.key is not None:
        orcha.properties.authkey = args.key.encode()
        log.debug("fixing internal digest key")
        multiprocessing.current_process().authkey = args.key.encode()

    for arg, value in vars(args).items():
        orcha.properties.extras[arg] = value

    for plugin in plugins:
        if plugin.can_handle(args.owner):
            return plugin.handle(args)

    return errno.ENOENT


if __name__ == "__main__":
    sys.exit(main())
