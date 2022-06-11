import json

from data import CustomJSONEncoder
from downloader import download
from parser import load_mods, load_config


def main():
    version, mods = load_mods()
    config = load_config()
    mod_objs = []

    for mod in mods:
        file_id = None
        if "=" in mod:
            mod, file_id = mod.split("=")
        obj, depends = download(version, mod)

        if file_id is not None:
            obj.file_id = file_id

        for item in [obj, *depends]:
            if item not in mod_objs and item is not None:
                mod_objs.append(item)

    __import__("pprint").pprint(mod_objs)

    with open("manifest.json", "w") as f:
        json.dump({
            "minecraft": {
                "version": config["mc_version"],
                "modLoaders": [
                    {
                        "id": "forge-" + config["forge"],
                        "primary": True
                    }
                ]
            },
            "manifestType": "minecraftModpack",
            "manifestVersion": 1,
            "name": config["pack"],
            "version": config["version"],
            "author": config["author"],
            "files": mod_objs,
            "overrides": "overrides"
        }, f, cls=CustomJSONEncoder, indent=4)


if __name__ == "__main__":
    main()
