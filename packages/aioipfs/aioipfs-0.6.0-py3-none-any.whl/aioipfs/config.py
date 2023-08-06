import os.path
from pathlib import Path

from yaml.loader import Loader
import yaml


default_config = '''
nodes:
  default:
    rpc_api_multiaddr: "/ip4/127.0.0.1/tcp/5001"
'''


def load_config(cfgpath: Path = None):
    if cfgpath is None:
        cfgpath = Path(os.path.expanduser('~')).joinpath('.aioipfs.yml')

    if not cfgpath.is_file():
        cfgpath.touch()
        with open(cfgpath, 'wt') as fd:
            fd.write(default_config)

    try:
        with open(cfgpath, 'rt') as fd:
            cfg = yaml.load(fd, Loader=Loader)

        assert cfg is not None
        assert isinstance(cfg['nodes'], dict)
    except Exception:
        return {}
    else:
        return cfg


def configure_node(cfgpath: Path = None):
    if cfgpath is None:
        cfgpath = Path(os.path.expanduser('~')).joinpath('.aioipfs.yml')

    if not cfgpath.is_file():
        cfgpath.touch()
        with open(cfgpath, 'wt') as fd:
            fd.write(default_config)

    try:
        with open(cfgpath, 'rt') as fd:
            cfg = yaml.load(fd, Loader=Loader)

        assert cfg is not None
        assert isinstance(cfg['nodes'], dict)
    except Exception:
        return {}
    else:
        return cfg
