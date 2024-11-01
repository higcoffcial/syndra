import argparse
import os
from pathlib import Path

from classes import MediaInfoDict, PlexSettings
from utils import strtobool

DEFAULT_IGNORE_SIZE = 0  # in MB
DEFAULT_IGNORE_DURATION = 0  # in seconds


def parse_ignore_params(args: argparse.Namespace) -> MediaInfoDict:
    size: int | None = args.ignore_size or int(os.getenv("SYNDRA_IGNORE_SIZE", DEFAULT_IGNORE_SIZE))
    duration: int | None = args.ignore_duration or int(os.getenv("SYNDRA_IGNORE_DURATION", DEFAULT_IGNORE_DURATION))
    return MediaInfoDict(size=size, duration=duration)


def parse_plex_params(args: argparse.Namespace) -> PlexSettings:
    plex_url: str | None = args.plex_url or os.getenv("SYNDRA_PLEX_URL")
    plex_token: str | None = args.plex_token or os.getenv("SYNDRA_PLEX_TOKEN")

    if not plex_url or not plex_token:
        exit("Plex URL and token must be provided either as arguments or environment variables.")

    return PlexSettings(plex_url=plex_url, plex_token=plex_token)


def parse_domain_url(args: argparse.Namespace) -> str:
    # get domain url from command line arguments first
    # if no domain url were provided, try to get them from environment variables
    url: str = args.url or os.getenv("SYNDRA_URL", "")

    # if no domain url were found, build from web server details
    if not url:
        host = os.getenv("WEB_HOST")
        port = os.getenv("WEB_PORT")
        ssl = strtobool(os.getenv("WEB_SSL"))  # True/False but also return None if not set or invalid value

        # for cli users ensure --url is provided
        if not all([host, port, ssl is not None]):
            message = (
                "ERROR: Must provide --url value, else set SYNDRA_URL environment variable "
                "or set WEB_HOST and WEB_PORT and WEB_SSL environment variables"
            )
            exit(message)

        port = port if port not in ["80", "443"] else ""
        protocol = "https" if ssl else "http"
        url = f"{protocol}://{host}{':' if port else ''}{port}"

    return url


def parse_out_file(args: argparse.Namespace) -> Path:
    # get out file from command line arguments first
    # if no out file were provided, try to get them from environment variables
    out_file_str: str = args.out

    if not out_file_str:
        out_file_str = os.getenv("SYNDRA_OUT", "deovr")

    out_path = Path(out_file_str)

    # ensure out file is a file path and not a directory
    if out_path.is_dir():
        exit(f"ERROR: {out_path} is a directory, please provide a file path instead, i.e. {out_path / '<file_name>'}")

    # create parent directories if not exists
    if not out_path.parent.exists():
        out_path.parent.mkdir(parents=True, exist_ok=True)

    return out_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="syndra", description="Generate json for DeoVR")

    parser.add_argument("--out", "-o", nargs="?", type=str, help="Output /path/file_name [default: deovr]")
    parser.add_argument("--url", "-u", nargs="?", type=str, help="Domain name of the video file server")
    parser.add_argument("--ext", "-e", nargs="*", type=str, help="VR video file extensions")

    ignore_size_help = "Ignore files smaller than X MB (megabytes) (set to 0 to disable) [default: 0]"
    parser.add_argument("--ignore-size", "-s", nargs="?", type=int, help=ignore_size_help)
    ignore_dur_help = "Ignore files shorter than X seconds (set to 0 to disable) [default: 0]"
    parser.add_argument("--ignore-duration", "-d", nargs="?", type=int, help=ignore_dur_help)

    parser.add_argument("--loop", "-l", nargs="?", default=0, type=int, help="Generate every X seconds")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    parser.add_argument("--plex-url", nargs="?", type=str, help="Url to your plex server")
    parser.add_argument("--plex-token", nargs="?", type=str, help="Your Plex token")
    return parser.parse_args()