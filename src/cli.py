import argparse
import logging

logger = logging.getLogger("monitor4web")


def cli_arg_parse() -> argparse.Namespace:
    """
    Parse command-line arguments for the monitor4web tool.

    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="monitor4web",
        description="",
        exit_on_error=False,
    )

    parser.add_argument(
        "--create-db",
        action=argparse.BooleanOptionalAction,
        help="Create the database needed, to save the access attempts",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="monitor4web 0.1",
    )

    parser.add_argument(
        "-u",
        "--url",
        help="Url of the website that should be monitored",
        required=True,
    )

    parser.add_argument(
        "--retry-attempts",
        type=int,
        default=1,
        help="Number of times should be tried to access the website",
    )

    parser.add_argument(
        "--check-website",
        action=argparse.BooleanOptionalAction,
        help="Number of times should be tried to access the website",
    )

    parser.add_argument(
        "--start-date",
        help="Starting date of monitoring, format: YYYY-MM-DD h:m:s",
    )

    parser.add_argument(
        "--end-date",
        help="Starting date of monitoring, format: YYYY-MM-DD h:m:s",
    )

    try:
        args = parser.parse_args()
        logger.debug(f"Parsed arguments: {args}")
    except argparse.ArgumentError as e:
        logger.debug(f"Invalid argument.")
        parser.print_help()
        raise SystemExit(2)

    return args