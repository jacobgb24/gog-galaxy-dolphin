"""
This utilities file generates the output binaries that should be placed in the GOG plugins folder.
Two binaries are generated, one for gamecube and another for wii. The only necessary changes are
the directory name and manifest.
"""
import json
import shutil
import argparse
import os
import sys

import utils
from galaxy.api.consts import Platform

gamecube = {"platform": Platform.NintendoGameCube.value, "guid": "c732be30-0407-463f-bc30-6d8b3809fef4"}
wii = {"platform": Platform.NintendoWii.value, "guid": "c732be30-0407-463f-bc30-6d8b3809fef5"}

if __name__ == '__main__':

    if sys.platform == 'win32':
        GOG_DIR = os.environ['localappdata'] + '\\GOG.com\\Galaxy\\plugins\\installed'
        LOG_DIR = os.environ['programdata'] + '\\GOG.com\\Galaxy\\logs'
    elif sys.platform == 'darwin':
        GOG_DIR = os.path.realpath("~/Library/Application Support/GOG.com/Galaxy/plugins/installed")
        LOG_DIR = os.path.realpath("/Users/Shared/GOG.com/Galaxy/Logs")
    else:
        GOG_DIR = None
        LOG_DIR = None

    parser = argparse.ArgumentParser(description="Generates output plugins. "
                                                 "By default places in GOG location. Modify with `-o`")
    output = parser.add_mutually_exclusive_group()
    output.add_argument('-o', '--output-dir', help="Directory to output to. Default is GOG installed folder",
                        default=GOG_DIR)
    output.add_argument('-z', '--zip', action='store_true', help="Output a zip to current dir for github release")
    output.add_argument('-c', '--clear-logs', action='store_true', help="If set, attempts to remove log files")
    args = parser.parse_args()

    base_manifest = utils.get_manifest()

    if args.output_dir is not None and not args.zip:
        base_dir = args.output_dir
    else:
        base_dir = base_manifest["name"]

    if args.clear_logs:
        print("Removing log files")
        for f in [f'{LOG_DIR}/plugin-{gamecube["platform"]}-{gamecube["guid"]}.log',
                  f'{LOG_DIR}/plugin-{wii["platform"]}-{gamecube["guid"]}.log',
                  f'{LOG_DIR}/GalaxyClient.log']:
            try:
                os.remove(f)
            except (FileNotFoundError, PermissionError) as e:
                print(f"Can't delete log for {f}")
                print(f'    {e}')
                continue

    gc_path = f'{base_dir}/gog-dolphin-{gamecube["platform"]}-{gamecube["guid"]}'
    wii_path = f'{base_dir}/gog-dolphin-{wii["platform"]}-{wii["guid"]}'

    ignored_files = shutil.ignore_patterns(f'{base_manifest["name"]}*', ".*", "__*", "manifest.json", __file__)

    # gc
    print("Creating ncube files...")
    print(f"  path: {gc_path}")
    shutil.rmtree(gc_path, ignore_errors=True)
    shutil.copytree(".", gc_path, ignore=ignored_files)
    gc_manifest = base_manifest.copy()
    gc_manifest["name"] = base_manifest["name"] + f"_Gamecube"
    gc_manifest.update(gamecube)
    with open(f"{gc_path}/manifest.json", "w") as m:
        json.dump(gc_manifest, m, indent=2)

    # wii
    print("Creating nwii files...")
    print(f"  path: {wii_path}")
    shutil.rmtree(wii_path, ignore_errors=True)
    shutil.copytree(".", wii_path, ignore=ignored_files)
    wii_manifest = base_manifest.copy()
    wii_manifest["name"] = base_manifest["name"] + f"_Wii"
    wii_manifest.update(wii)
    with open(f"{wii_path}/manifest.json", "w") as m:
        json.dump(wii_manifest, m, indent=2)

    if args.zip:
        print("Outputting to zip")
        zip_name = f'{base_dir}_v{base_manifest["version"]}'
        if os.path.exists(f'{zip_name}.zip'):
            os.remove(f'{zip_name}.zip')
        shutil.make_archive(zip_name, 'zip', base_dir)
        shutil.rmtree(base_dir)

    print("Done!")
