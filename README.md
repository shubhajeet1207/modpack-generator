# modpack-generator

To make a simple manifest.json, it would download mod information from CurseForge website.

## Settings

### config.json

```json
{
  "author": "author's name",
  "forge": "forge version, e.g. 14.23.5.2808. Version should be specific.",
  "pack": "modpack name",
  "version": "pack version number"
}
```


### mods.txt

```
# Minecraft [minecraft version, e.g. 1.12]
mod-one
mod-two
mod-three
mod-four
```

The name in the URL on CurseForge is the format these modifications must be in, like:

```
Ender IO -> ender-io
Thermal Expansion -> thermalexpansion
```


## For Generating manifest.json

After configuring the files mentioned above you can run the main.py file for testing.

```bash
pip install -r requirements.txt
$ python main.py
```
