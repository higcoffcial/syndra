import enum
from typing import Any, NotRequired, TypedDict

class MediaInfoDict(TypedDict):
    size: int  # in MB
    duration: int  # in seconds


class StereoMode(enum.StrEnum):
    MONOSCOPIC = "off"
    SIDE_BY_SIDE = "sbs"
    TOP_BOTTOM = "tb"
    CUSTOM_UV = "cuv"


class ScreenType(enum.StrEnum):
    FLAT = "flat"
    EQUIRECT_180 = "dome"
    EQUIRECT_360 = "sphere"
    FISHEYE_180 = "fisheye"
    FISHEYE_190 = "rf52"
    FISHEYE_200 = "mkx200"


# https://deovr.com/app/doc#multiple-videos-deeplink
class Scene(TypedDict):
    id: NotRequired[int]
    title: str
    videoLength: int  # in seconds
    video_url: str  # required atm but could be set optional if encodings are used instead
    thumbnailUrl: str
    is3d: bool  # always true
    stereoMode: StereoMode
    screenType: ScreenType
    encodings: NotRequired[list[dict[str, Any]]]  # either encodings or video_url
    videoThumbnail: NotRequired[str]  # url
    videoPreview: NotRequired[str]  # url
    corrections: NotRequired[dict[str, int | float]]
    timeStamps: NotRequired[list[dict[str, Any]]]
    skipIntro: NotRequired[int]  # in seconds
    path: NotRequired[str]  # only for images mode


class Library(TypedDict):
    name: str
    list: list[Scene]


class Scenes(TypedDict):
    scenes: list[Library]