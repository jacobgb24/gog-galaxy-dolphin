import json
import shlex
import sys
from dataclasses import dataclass
from binascii import hexlify
import os
from pathlib import Path
from typing import Union
import urllib.parse as urlparse
from urllib.parse import parse_qs

from galaxy.api.consts import LocalGameState, LicenseType, Platform
from galaxy.api.types import Game, LocalGame, LicenseInfo


@dataclass
class DolphinGame:
    game_id: str
    game_title: str
    path: Path
    dolphin_path: str = None

    def __init__(self, path: Path, custom_config: dict):
        self.path = path
        self.game_id = get_game_id(path)
        self.game_title = path.stem
        for entry in custom_config['custom_launchers']:
            if entry['gameid'] == self.game_id:
                self.dolphin_path = entry['dolphin']


def get_local_file_path(file_name: str) -> Union[Path, os.PathLike]:
    return Path(__file__).parent / file_name


def get_manifest() -> dict:
    with open(get_local_file_path("manifest.json"), 'r') as manifest:
        return json.load(manifest)


def get_config() -> dict:
    with open(get_local_file_path("user_config.json"), 'r') as config:
        return json.load(config)


def write_config(new_config: dict) -> None:
    with open(get_local_file_path("user_config.json"), 'w') as config:
        return json.dump(new_config, config, indent=2)


def dgame2local(game: DolphinGame) -> LocalGame:
    return LocalGame(game.game_id, LocalGameState.Installed)


def dgame2game(game: DolphinGame) -> Game:
    return Game(game.game_id, game.game_title, None, LicenseInfo(LicenseType.SinglePurchase, None))


def get_game_id(game_file: Path) -> str:
    """ gets the game id for the given file by reading the first bytes """
    with game_file.open('rb') as f:
        return f.read(6).decode()


def get_game_platform(game_file: Path) -> Platform:
    """
    gets the platform for a given file. Looks at magic strings in file otherwise tries file size to determine
    """
    # magic strings from dolphin
    # https://github.com/dolphin-emu/dolphin/blob/eca6cc51f977ceaae7a12883a5b7a587ee0d45f6/Source/Core/DiscIO/Volume.cpp#L46
    with game_file.open('rb') as f:
        if hexlify(f.read(32)[28:]) == b'c2339f3d':
            return Platform.NintendoGameCube
        f.seek(0)
        if hexlify(f.read(28)[24:]) == b'5d1c9ea3':
            return Platform.NintendoWii

    if game_file.stat().st_size < 2147483648:
        return Platform.NintendoGameCube
    else:
        return Platform.NintendoWii


def parse_get_params(uri: str) -> dict:
    """ parse url params returned from startup_config.html """
    parsed = urlparse.urlparse(uri)
    return {k: v[0].strip('\'\"') for k, v in parse_qs(parsed.query).items()}


def path2subopen(path: Path) -> str:
    """ converts a path into a safe string for subprocess calls"""
    return shlex.quote(str(path))


SETUP_WEB_PARAMS = {
    "window_title": "Set Dolphin Paths",
    "window_width": 640,
    "window_height": 480,
    "start_uri": f'file:///{get_local_file_path("startup_config.html")}?'
                 f'platform={get_manifest()["platform"]}&os={sys.platform}',
    "end_uri_regex": ".*/done.*"
}
