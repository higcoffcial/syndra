from plexapi.server import PlexServer
from classes import StereoMode, ScreenType, MediaInfoDict, Scene

def __ignore_scene(media_info: MediaInfoDict, ignore_params: MediaInfoDict) -> bool:
    return media_info["size"] < ignore_params["size"] or media_info["duration"] < ignore_params["duration"]


def __get_media_info_from_plex(item) -> MediaInfoDict:
    duration = int(item.duration / 1000) if item.duration else 0  # in seconds
    size = int(item.media[0].parts[0].size / 1024 / 1024) if item.media[0].parts[0].size else 0  # in MB
    return MediaInfoDict(size=size, duration=duration)


def get_plex_scenes(plex_server: PlexServer, ignore_params: MediaInfoDict) -> list[Scene]:
    from utils import logger
    scenes = []

    for library in plex_server.library.sections():
        if library.type == "movie":
            for item in library.all():
                media_info = __get_media_info_from_plex(item)
                if __ignore_scene(media_info, ignore_params):
                    continue

                if item.media and item.media[0].parts:
                    part_id = item.media[0].parts[0].id
                    video_url = f"{plex_server._baseurl}/library/parts/{part_id}/file?X-Plex-Token={plex_server._token}"
                else:
                    logger.warning(f"Could not retrieve stream URL for {item.title}")
                    continue

                scene = Scene(
                    title=item.title,
                    videoLength=media_info["duration"],
                    thumbnailUrl=item.thumbUrl,
                    video_url=video_url,
                    is3d=True, # might be required to be true - who knows :P
                    stereoMode=StereoMode.SIDE_BY_SIDE,
                    screenType=ScreenType.FLAT
                )

                scenes.append(scene)
    return scenes


