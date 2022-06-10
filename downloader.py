import re
from functools import lru_cache
from typing import List, Tuple, Union

import requests
from bs4 import BeautifulSoup

from data import ModInfo


URL = "https://www.curseforge.com/{0}"
DEPENDENCY_URL = "https://www.curseforge.com/{0}/relations/dependencies?filter-related-dependencies=3"
NO_VERSION = "No file found for mod {1} with minecraft version {0}"

FILE_ID = re.compile(r"(?P<file_id>\d+)/download")


def find_file_id(mc_version: str, soup: BeautifulSoup) -> int:

    elements = [item for item in soup.find_all('a') if mc_version == item.text.strip()]

    if not elements:
        pass

    subheaders = soup.find_all(class_="e-sidebar-subheader")

    sidebar_inner = subheaders[0].parent

    correct = [header for header in subheaders if mc_version in list(header.children)[1].text]

    found = False

    for item in sidebar_inner.children:
        if not hasattr(item, "children"):
            continue

        if item in correct:
            found = True

        elif found:
            latest = list(item.children)[1]
            download_div = list(list(latest.children)[3].children)[1]
            url = list(download_div.children)[1].attrs["href"]
            match = FILE_ID.search(url)
            return int(match.group("file_id"))


def find_project_id(soup: BeautifulSoup) -> int:
    elements = [item for item in soup.find_all('div') if "Project ID" == item.text]
    line = elements[0].parent
    project_id = list(line.children)[3].text
    return int(project_id)


def find_dependencies(mc_version: str, old_mod_name: str) -> List[ModInfo]:
    url = DEPENDENCY_URL.format(old_mod_name.lower().replace(" ", "-"))
    body = requests.get(url).text
    soup = BeautifulSoup(body, "lxml")
    dep_list = soup.find(class_="project-relations")
    divs = dep_list.find_all(class_="name-wrapper")
    mod_names = [list(div.children)[1].attrs["href"] for div in divs]

    mod_names = [mod.split("/")[-1] for mod in mod_names]

    mods = []
    for mod_name in mod_names:
        print("Downloading dependency:", mod_name, "for mod", old_mod_name)
        mod, deps = download(mc_version, mod_name, is_dep=True)
        for item in [mod, *deps]:
            if item not in mods and item is not None:
                mods.append(item)
    return mods


@lru_cache(maxsize=None)
def download(mc_version: str, mod_name: str, is_dep=False) -> Tuple[Union[ModInfo, None], List[ModInfo]]:
    if not is_dep:
        print("Downloading:", mod_name)

    url = URL.format(mod_name.lower().replace(" ", "-"))

    body = requests.get(url).text

    soup = BeautifulSoup(body, "lxml")

    file_id = find_file_id(mc_version, mod_name, soup)

    if file_id is None and is_dep:
        print("Out of date mod:", mod_name)
        return None, []

    project_id = find_project_id(soup)

    deps = find_dependencies(mc_version, mod_name)

    return ModInfo(mod_name, project_id, file_id, True), deps


if __name__ == "__main__":
    result = download("Minecraft 1.12")
    print(result)