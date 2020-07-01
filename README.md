# GOG Dolphin
This is an integration for GOG Galaxy using the [public api](https://github.com/gogcom/galaxy-integrations-python-api).
This codebase supports both Gamecube and Wii games, but through two copies (as GOG requires one platform per integration).

## Current Features
* Import Gamecube and Wii games easily into GOG Galaxy
* File names don't matter as the plugin will read the file directly to determine the ID
* Integration walks user through setting paths to dolphin and games on first connect
* Single code-base for both Gamecube and Wii simplifies updates and maintainability


## Installation
Either generate the plugins via `generate_plugins.py` or download from the [releases page](https://github.com/jacobgb24/gog-galaxy-dolphin/releases).
Place the two plugin folders into the correct location for GOG.

Windows: `%localappdata%\GOG.com\Galaxy\plugins\installed`

macOS: `~/Library/Application Support/GOG.com/Galaxy/plugins/installed`

Restart GOG, Go to settings -> Add games and friends -> connect platforms.
Click connect for each platform and follow the instructions presented in the window.

#### Manual Config
If manual configuration is needed, this can be done by editing `user_config.json`.

## TODO / Planned Features
This project early on and subject to change.
These are the main things that are planned to be worked on:

* Allow custom configuration via a json file. 
Most notably, the ability to have duplicate copies of a game, but with different instances of dolphin (e.g. for netplay).
* Add playtime tracking.
Likely through [Galaxy-Utils](https://github.com/tylerbrawl/Galaxy-Utils) or a tweaked version of it.
* Ensure that functions for the GOG plugin are properly implemented.
Specifically, handling tick updates, shutdowns, etc.
* Test on MacOS and ensure everything is working properly.
* Better handling of config file (file not existing, keys missing, etc.).
* Built in support for Project Slippi (this should utilize custom config, but could be streamlined). 
