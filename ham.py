import os
import shutil

from pathlib import Path
from zipfile import ZipFile

import json

class HAMPack:
    name = None
    files = []

    abspath = None

    def __init__(self, name: str = None, new: bool = True):
        self.abspath = os.path.abspath(os.getcwd())

        if os.path.exists("hampack.json") and new:
            raise FileExistsError(f"HAM pack seems to be already initialized at {self.abspath}")

        if new:
            self.name = name

            data = {
                    "name": self.name,
                    "files": self.files
            }

            with open("hampack.json", "w") as f:
                f.write(json.dumps(data, indent=4))
        else:
            with open("hampack.json", "r") as f:
                j = json.loads(f.read())

                self.name = j["name"]
                self.files = j["files"]

    def register(self, file):
        with open(f"{self.abspath}/hampack.json", "r+") as f:
            j = json.loads(f.read())

            j["files"].append(file)
            self.files = j["files"]

            f.seek(0)
            f.write(json.dumps(j, indent=4))
            f.truncate()

    def unregister(self, file):
        with open(self.abspath / "hampack.json", "r+") as f:
            j = json.loads(f.read())

            del j.files[j.files.index(file)]
            self.files = j["files"]

            f.seek(0)
            f.write(json.dumps(j, indent=4))
            f.truncate()

    def conflicts_list(self, of):
        intersections = list(set(of).intersection(self.files))

        return intersections

    def conflicts(self, project):
        of = project.files

        intersections = list(set(of).intersection(self.files))

        return intersections

class HAMZip:
    pack_name = None

    name = None
    files = []

    def __init__(self, pack_name):
        if not os.path.exists(pack_name) or not pack_name.endswith(".ham"):
            raise FileNotFoundError("Pack not found or is invalid (should have .ham file extension)!")

        self.pack_name = pack_name

        self.get_data()

    def get_data(self):
        with ZipFile(self.pack_name, 'r') as zf:
            with zf.open("hampack.json", 'r') as f:
                j = json.loads(f.read())

                self.name = j["name"]
                self.files = j["files"]

class Game:
    directory = None
    packs_file = None

    history = []
    current_pack = None

    def __init__(self, directory):
        self.directory = directory

        self.packs_file = f"{self.directory}/hampacks.json"

        if not os.path.exists(self.packs_file):
            with open(self.packs_file, "w") as f:
                f.write(json.dumps({"history": [], "current_pack": None}, indent=4))
        else:
            with open(self.packs_file, "r") as f:
                j = json.loads(f.read())

                self.history = j["history"]
                self.current_pack = j["current_pack"]

    def install(self, pack, destination="valve_addon"):
        full_destination = f"{self.directory}/{destination}"

        zipf = isinstance(pack, HAMZip)

        if self.current_pack and self.current_pack["install_dir"] != "valve" and self.current_pack["install_dir"] != "/":
            shutil.rmtree(f"{self.directory}/{self.current_pack['install_dir']}")

        if self.current_pack:
            self.history.append(self.current_pack)
        self.current_pack = {"name": pack.name, "install_dir": destination}

        if not os.path.exists(full_destination):
            os.mkdir(full_destination)

        if zipf:
            zf = ZipFile(pack.pack_name, 'r')

        l = len(pack.files)
        for i, f in enumerate(pack.files):
            print(f"Installing pack: {i + 1} / {l}")

            pd = os.path.dirname(f)
            if not os.path.exists(f"{full_destination}/{pd}"):
                os.makedirs(f"{full_destination}/{pd}")

            if not zipf:
                shutil.copyfile(f, f"{full_destination}/{pd}/{os.path.basename(f)}")
            else:
                zf.extract(f, f"{full_destination}")

        if zipf:
            zf.close()

        with open(self.packs_file, "w") as f:
            f.write(json.dumps({"history": self.history, "current_pack": self.current_pack}))
            f.truncate()

    def uninstall(self):
        if not self.current_pack:
            raise FileNotFoundError("No HAM pack installed!")

        if self.current_pack["install_dir"] == "valve" or self.current_pack["install_dir"] == "/":
            raise ValueError(f"Invalid install dir for current HAM pack detected (\'self.current_pack['install_dir']\'). Manual editing is required.")

        shutil.rmtree(f"{self.directory}/{self.current_pack['install_dir']}")

        if self.current_pack:
            self.history.append(self.current_pack)
        self.current_pack = None

        with open(self.packs_file, "w") as f:
            f.write(json.dumps({"history": self.history, "current_pack": self.current_pack}))
            f.truncate()
