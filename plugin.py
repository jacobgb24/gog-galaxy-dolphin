import asyncio
import subprocess
import sys
from abc import ABC
from pathlib import Path
from typing import List, Dict, Union
import shlex

import utils
from galaxy.api.consts import Platform
from galaxy.api.plugin import Plugin, create_and_run_plugin, logger
from galaxy.api.types import Authentication, NextStep
import os


class GOGDolphinPlugin(Plugin, ABC):
    def __init__(self, reader, writer, token):
        self.manifest_data = utils.get_manifest()
        self.config_data = utils.get_config()

        super().__init__(Platform(self.manifest_data['platform']), self.manifest_data['version'], reader, writer, token)
        self.games: List[utils.DolphinGame] = []
        # self.game_times = get_the_game_times()

    async def authenticate(self, stored_credentials=None) -> Union[NextStep, Authentication]:
        if not self.config_data['dolphin_path'] or not self.config_data['games_path']:
            return NextStep('web_session', utils.SETUP_WEB_PARAMS)
        return Authentication("Dolphin", "Dolphin")  # don't care about authentication values

    async def pass_login_credentials(self, step: str, credentials: Dict[str, str], cookies: List[Dict[str, str]]) \
            -> Union[NextStep, Authentication]:
        paths = utils.parse_get_params(credentials["end_uri"])
        logger.critical(f'CREDS: {paths}')
        self.config_data.update(paths)
        utils.write_config(self.config_data)
        return Authentication("Dolphin", "Dolphin")  # don't care about authentication values

    async def launch_game(self, game_id):
        for game in self.games:
            if game.game_id == game_id:
                dolphin_exe = Path(r"D:\Dolphin-x64\Dolphin.exe")

                dolphin_path = Path(self.config_data['dolphin_path'] if game.dolphin_path is None else game.dolphin_path)
                logger.critical(f'launching {game_id} via path: `{dolphin_path}` before we had `{dolphin_exe}`')
                logger.critical(f'game path: `{game.path}`')
                process_str = f'{utils.path2subopen(dolphin_path)} -b -e {utils.path2subopen(game.path)}'
                subprocess.Popen(shlex.split(process_str))
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
        path = Path(self.config_data['games_path'])
        for file in [f for f in path.glob('**/*') if f.is_file()]:
            # only add games for the given platform
            if utils.get_game_platform(file).value == self.manifest_data["platform"]:
                games.append(utils.DolphinGame(file))
            # TODO look at custom config here

        return games

    # need these stubbed out for API
    async def install_game(self, game_id):
        pass

    async def uninstall_game(self, game_id):
        pass


def main():
    create_and_run_plugin(GOGDolphinPlugin, sys.argv)


# run plugin event loop
if __name__ == "__main__":
    main()
