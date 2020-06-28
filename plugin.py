import asyncio
import subprocess
import sys
from abc import ABC
from pathlib import Path
from typing import List

import utils
from galaxy.api.consts import Platform
from galaxy.api.plugin import Plugin, create_and_run_plugin, logger
from galaxy.api.types import Authentication
import os

# TODO: make configurable
dolphin_exe = Path(r"D:\Dolphin-x64\Dolphin.exe")
dolphin_dir = r"D:\Dolphin Games"


class GOGDolphinPlugin(Plugin, ABC):
    def __init__(self, reader, writer, token):
        self.manifest_data = utils.get_manifest()

        super().__init__(Platform(self.manifest_data['platform']), self.manifest_data['version'], reader, writer, token)
        self.games: List[utils.DolphinGame] = []
        # self.game_times = get_the_game_times()

    async def authenticate(self, stored_credentials=None):
        return Authentication("id", "name")  # TODO: better set up here

    async def launch_game(self, game_id):
        for game in self.games:
            if game.game_id == game_id:
                dolphin_path = str(dolphin_exe if game.dolphin_path is None else game.dolphin_path)
                logger.critical(f'launching {game_id} via path: {dolphin_path}')
                subprocess.Popen([dolphin_path, "-b", "-e", str(game.path)])
                    # subprocess.Popen(
                    #     [os.path.dirname(os.path.realpath(__file__)) + r'\TimeTracker.exe', game_id, game_id])

                break
        return

    async def get_game_time(self, game_id, context=None):
        pass

    def tick(self):
        pass
        # async def update_local_games():
        #     loop = asyncio.get_running_loop()
        #     new_local_games_list = await loop.run_in_executor(None, self.local_games_list)
        #     notify_list = self.backend_client.get_state_changes(self.local_games_cache, new_local_games_list)
        #     self.local_games_cache = new_local_games_list
        #     for local_game_notify in notify_list:
        #         self.update_local_game_status(local_game_notify)
        #
        # asyncio.create_task(update_local_games())

    async def get_owned_games(self):
        self.games = self.get_dolphin_games()
        return [utils.dgame2game(g) for g in self.games]

    async def get_local_games(self):
        self.games = self.get_dolphin_games()
        return [utils.dgame2local(g) for g in self.games]

    def get_dolphin_games(self):
        games = []
        for root, dirs, files in os.walk(dolphin_dir):
            for file in files:
                full_path = Path(root) / file
                # only add games for the given platform
                if utils.get_game_platform(full_path).value == self.manifest_data["platform"]:
                    games.append(utils.DolphinGame(full_path))
                # TODO look at custom config here

        return games

    async def install_game(self, game_id):
        pass

    async def uninstall_game(self, game_id):
        pass


def main():
    create_and_run_plugin(GOGDolphinPlugin, sys.argv)


# run plugin event loop
if __name__ == "__main__":
    main()
