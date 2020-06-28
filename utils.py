import json
from dataclasses import dataclass
from binascii import hexlify
import os
from pathlib import Path

from galaxy.api.consts import LocalGameState, LicenseType, Platform
from galaxy.api.types import Game, LocalGame, LicenseInfo


@dataclass
class DolphinGame:
    game_id: str
    game_title: str
    path: Path
    dolphin_path: str = None

    def __init__(self, path: Path):
        self.path = path
        self.game_id = get_game_id(path)
        self.game_title = get_game_title(path)


def get_manifest() -> dict:
    with open(Path(__file__).parent / "manifest.json", 'r') as manifest:
        return json.load(manifest)


def dgame2local(game: DolphinGame) -> LocalGame:
    return LocalGame(game.game_id, LocalGameState.Installed)


def dgame2game(game: DolphinGame) -> Game:
    return Game(game.game_id, game.game_title, None, LicenseInfo(LicenseType.SinglePurchase, None))


def get_game_id(game_file: Path) -> str:
    with game_file.open('rb') as f:
        return f.read(6).decode()


def get_game_title(game_file: Path) -> str:
    # TODO try db first
    return game_file.stem


def get_game_platform(game_file: Path) -> Platform:
    if game_file.suffix == "gcm":
        return Platform.NintendoGameCube
    if game_file.suffix == "wbfs":
        return Platform.NintendoWii
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
