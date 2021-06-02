# GOG Dolphin
This is an integration for GOG Galaxy using the [public api](https://github.com/gogcom/galaxy-integrations-python-api).
This codebase supports both Gamecube and Wii games, but through two copies (as GOG requires one platform per integration).

## Current Features
* Import Gamecube and Wii games easily into GOG Galaxy
* File names don't matter as the plugin will read the file directly to determine the ID
* Integration walks user through setting paths to dolphin and games on first connect
* Single code-base for both Gamecube and Wii simplifies updates and maintainability


## Installation
Either clone and generate the plugins via `python3 generate_plugins.py` or download from the 
[releases page](https://github.com/jacobgb24/gog-galaxy-dolphin/releases).
Place the two plugin folders into the correct location for GOG.

Windows: `%localappdata%\GOG.com\Galaxy\plugins\installed`

macOS: `~/Library/Application Support/GOG.com/Galaxy/plugins/installed`

Restart GOG, Go to Settings -> Integrations.
Click connect for each platform and follow the instructions presented in the window.

#### Manual Config
If manual configuration is needed, this can be done by editing `user_config.json`.


## TODO / Planned Features
This project early on and subject to change.
These are the main things that are planned to be worked on:

- [ ] Allow custom configuration via a json file. 
~~Most notably, the ability to have duplicate copies of a game, but with different instances of dolphin (e.g. for netplay).~~
This doesn't seem possible since IDs GOG doesn't recognize will be marked as spam and hidden.
- [ ] Add playtime tracking.
Likely through [Galaxy-Utils](https://github.com/tylerbrawl/Galaxy-Utils) or a tweaked version of it.
- [ ] Ensure that functions for the GOG plugin are properly implemented.
Specifically, handling tick updates, shutdowns, etc.
- [ ] Test on MacOS and ensure everything is working properly.
- [ ] Better handling of config file (file not existing, keys missing, etc.).
- [x] Built in support for Project Slippi (this should utilize custom config, but could be streamlined).
- [ ] Don't hard-code GOG plugin (use pip to generate directories).
- [ ] Pass data to startup_config to be able to show slippi just for gamecube and show example paths for user OS.

## Notes

### Checking GoG database for game
Look at json response for following URL. Specifically if `type` is `spam`, the game won't show.
```
https://gamesdb.gog.com/platforms/<PLATFORM>/external_releases/<GAMEID>
```
Where platform is `nwii` or `ncube` and gameid is what is listed in Dolphin

### Log locations:
Windows: `"C:\ProgramData\GOG.com\Galaxy\logs\`

MacOS: `/Users/Shared/GOG.com/Galaxy/Logs`

Logs of interest are `GalaxyClient.log` and `plugin-<ncube|nwii>*.log`

### General Debug process
* Disconnect plugin
* Run `python3 generate_plugins.py -c`
* Connect plugin
* View logs