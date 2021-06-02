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
        return Authentication("Dolphin-ID", "Dolphin")  # don't care about authentication values

    async def pass_login_credentials(self, step: str, credentials: Dict[str, str], cookies: List[Dict[str, str]]) \
            -> Union[NextStep, Authentication]:
        paths = utils.parse_get_params(credentials["end_uri"])
        logger.info(f'Got paths from setup: {paths}')
        self.config_data.update(paths)
        # add in entry to launch melee via slippi if user set that field
        if 'slippi_path' in paths:
            self.config_data['custom_launchers'].append({'gameid': "GALE01", 'dolphin': paths['slippi_path']})
            del self.config_data['slippi_path']
        utils.write_config(self.config_data)
        return Authentication("Dolphin-ID", "Dolphin")  # don't care about authentication values

    async def launch_game(self, game_id):
        for game in self.games:
            if game.game_id == game_id:
                dolphin_path = self.config_data['dolphin_path'] if game.dolphin_path is None else game.dolphin_path
                logger.info(f'launching {game_id} via path: `{dolphin_path}`')
                process_str = f'{utils.path2subopen(dolphin_path)} -b -e {utils.path2subopen(game.path)}'
                subprocess.Popen(shlex.split(process_str))
                break
        return

    # async def get_game_time(self, game_id, context=None):
    #     pass

    # def tick(self):
    #     logger.info("tick called")

    async def get_owned_games(self):
        self.games = self.get_dolphin_games()
        return [utils.dgame2game(g) for g in self.games]

    async def get_local_games(self):
        self.games = self.get_dolphin_games()
        return [utils.dgame2local(g) for g in self.games]

    def get_dolphin_games(self):
        games = []
        path = Path(self.config_data['games_path'])
        logger.info(self.config_data)
        logger.info(f"Getting games from path: {path.resolve()}")
        for file in [f for f in path.glob('**/*') if f.is_file()]:
            # only add games for the given platform
            if utils.get_game_platform(file).value == self.manifest_data["platform"]:
                games.append(utils.DolphinGame(file, self.config_data))
        logger.info(f'Found games: {games}')
        return games


def main():
    create_and_run_plugin(GOGDolphinPlugin, sys.argv)


# run plugin event loop
if __name__ == "__main__":
    main()
