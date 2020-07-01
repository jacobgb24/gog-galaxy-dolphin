"""
This utilities file generates the output binaries that should be placed in the GOG plugins folder.
Two binaries are generated, one for gamecube and another for wii. The only necessary changes are
the directory name and manifest.
"""
import json
import shutil
import argparse
import os

import utils
from galaxy.api.consts import Platform

gamecube = {"platform": Platform.NintendoGameCube.value, "guid": "c732be30-0407-463f-bc30-6d8b3809fef4"}
wii = {"platform": Platform.NintendoWii.value, "guid": "c732be30-0407-463f-bc30-6d8b3809fef5"}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generates output plugins")
    output = parser.add_mutually_exclusive_group()
    output.add_argument('-o', '--output-gog', help="directory for gog plugins to output directly to", default=None)
    output.add_argument('-z', '--zip', action='store_true', help="Set to zip up when done for github release")
    args = parser.parse_args()

    base_manifest = utils.get_manifest()

    if args.output_gog is not None and not args.zip:
        base_dir = args.output_gog
    else:
        base_dir = base_manifest["name"]

    gc_path = f'{base_dir}/gog-dolphin-{gamecube["platform"]}-{gamecube["guid"]}'
    wii_path = f'{base_dir}/gog-dolphin-{wii["platform"]}-{wii["guid"]}'

    ignored_files = shutil.ignore_patterns(f'{base_manifest["name"]}*', ".*", "__*", "manifest.json", __file__)

    # gc
    shutil.rmtree(gc_path, ignore_errors=True)
    shutil.copytree(".", gc_path, ignore=ignored_files)
    gc_manifest = base_manifest.copy()
    gc_manifest["name"] = base_manifest["name"] + f"_Gamecube"
    gc_manifest.update(gamecube)
    with open(f"{gc_path}/manifest.json", "w") as m:
        json.dump(gc_manifest, m, indent=2)

    # wii
    shutil.rmtree(wii_path, ignore_errors=True)
    shutil.copytree(".", wii_path, ignore=ignored_files)
    wii_manifest = base_manifest.copy()
    wii_manifest["name"] = base_manifest["name"] + f"_Wii"
    wii_manifest.update(wii)
    with open(f"{wii_path}/manifest.json", "w") as m:
        json.dump(wii_manifest, m, indent=2)

    if args.zip:
        zip_name = f'{base_dir}_v{base_manifest["version"]}'
        if os.path.exists(f'{zip_name}.zip'):
            os.remove(f'{zip_name}.zip')
        shutil.make_archive(zip_name, 'zip', base_dir)
        shutil.rmtree(base_dir)








