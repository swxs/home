# -*- coding: utf-8 -*-
# @FILE    : consts.py
# @AUTH    : model_creater


from enum import IntEnum, StrEnum


class FileInfo_Policy(IntEnum):
    ALIOSS = 1


class AccessMode(StrEnum):
    INLINE = "inline"
    DOWNLOAD = "download"


IMAGE_EXTENSIONS = frozenset(
    {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
        ".svg",
        ".bmp",
        ".ico",
    }
)


class ShareLinkStatus(IntEnum):
    ACTIVE = 1
    REVOKED = 2
