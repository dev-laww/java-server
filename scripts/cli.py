import argparse

from .utils.logging import get_logger
from .utils.server import start_server, stop_server, get_status

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Manage the Minecraft server.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="Start the Minecraft server")
    start_parser.add_argument(
        "--timeout", type=int, default=60, help="Timeout in seconds to wait for the server to start"
    )

    stop_parser = subparsers.add_parser("stop", help="Stop the Minecraft server")
    status_parser = subparsers.add_parser("status", help="Get the status of the Minecraft server")

    args = parser.parse_args()

    if args.command == "start":
        start_server(timeout=args.timeout)
    elif args.command == "stop":
        stop_server()
    elif args.command == "status":
        status = get_status()
        if status:
            logger.info(status)
        else:
            logger.warning("Server is not running or could not retrieve status.")
