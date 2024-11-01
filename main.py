import argparse
import logging
import os
import time

from plexapi.server import PlexServer

from utils import logger, strtobool, parse_args, parse_domain_url, parse_ignore_params, parse_out_file, parse_plex_params, get_plex_scenes, gen_json_file
from classes import Library, Scenes

def generate(args: argparse.Namespace) -> None:
    logger.info("Generating DeoVR JSON...")

    out_file = parse_out_file(args)
    logger.info(f"Output file: {out_file}")

    url = parse_domain_url(args)
    logger.info(f"Domain URL: {url}")

    ignore_params = parse_ignore_params(args)
    logger.info(f"Ignore Parameters: {ignore_params}")

    plex_settings = parse_plex_params(args)
    plex_server = PlexServer(plex_settings['plex_url'], plex_settings['plex_token'])
    logger.info(f"Plex Server: {plex_server.diagnostics}")

    scene_list = get_plex_scenes(plex_server, ignore_params)
    library = Library(name="Library", list=scene_list)
    scenes = Scenes(scenes=[library])
    logger.debug(f"Scenes: {scenes}")
    logger.info(f"Generating for {len(scene_list)} scenes ...")

    gen_json_file(scenes, out_file)
    logger.info(f"DeoVR JSON generated successfully: {out_file.resolve()}")


if __name__ == "__main__":
    parsed_args = parse_args()
    verbose = parsed_args.verbose or strtobool(os.getenv("SYNDRA_VERBOSE"))
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    loop = parsed_args.loop or int(os.getenv("SYNDRA_LOOP", 0))
    while True:
        logger.info("=" * 50)
        generate(parsed_args)

        if not loop:
            break

        logger.info(f"Sleeping for {loop} seconds ...")
        time.sleep(loop)
