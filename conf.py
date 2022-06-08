import os
import sys
import toml


__VERSION__ = "v3"
__VERSIONTAG__ = "Satanic Shindig"


BASE = {
    'name': 'Link',
    'prefix': '$',
    'description': 'This old boat is very rikety',
    'timezone': 'UTC',
    'activity': 'with fire',
    'ownerID': 0,
    'token': '',
    'secret': '',
    'profile': {
        'dailyAmount': 5000,
        'dailyCooldown': 86400
    }
}


def recSetAttr(object, dic):
    for key, value in dic.items():
        if isinstance(value, dict):
            setattr(object, key, recSetAttr(SubConf(), value))
        else:
            setattr(object, key, value)
    return object


def ensure(path):
    try:
        os.makedirs(path)
        print(f"Directory {path} does not exist, creating.")
        return path
    except FileExistsError:
        return path
    except PermissionError:
        print(f"Error creating {path}.")
        print("FATAL. SHUTTING DOWN.")
        sys.exit(-1)


class SubConf:
    def __init__(self):
        pass


class Conf:
    def __init__(self):
        try:
            self._conf = toml.load("conf.toml")
        except FileNotFoundError:
            print("conf.toml not found, generating...")
            self._conf = BASE
            with open("conf.toml", "w") as confFile:
                toml.dump(self._conf, confFile)
        self._constructPaths()
        self = recSetAttr(self, self._conf)
        self.validate()

    def _constructPaths(self):
        self._conf['VERSION'] = __VERSION__
        self._conf['VERSIONTAG'] = __VERSIONTAG__

        root = os.getcwd()
        self._conf['rootDir'] = root
        self._conf['storageDir'] = ensure(os.path.join(root, "storage/"))
        self._conf['tempDir'] = ensure(os.path.join(self._conf['storageDir'], "temp/"))
        self._conf['assetDir'] = os.path.join(root, "assets/")
        self._conf['clipDir'] = os.path.join(self._conf['assetDir'], "clips/")
        self._conf['pfpDir'] = os.path.join(self._conf['assetDir'], "pfp/")
        self._conf['imgDir'] = os.path.join(self._conf['assetDir'], "images/")

        ormroot = ensure(os.path.join(self._conf['storageDir'], "database/"))
        self._conf['orm'] = {}
        self._conf['orm']['rootDir'] = ormroot
        self._conf['orm']['memberDir'] = ensure(os.path.join(ormroot, "members/"))
        self._conf['orm']['botDir'] = ensure(os.path.join(ormroot, "bot/"))

    def validate(self):
        valid = True

        for attr in ['token', 'secret', 'ownerID']:
            if not getattr(self, attr, None):
                print(f"{attr} is not in conf.toml.")
                valid = False

        if not valid:
            print("Critical settings are missing. Fatal, shutting down.")
            sys.exit(-1)

conf = Conf()
