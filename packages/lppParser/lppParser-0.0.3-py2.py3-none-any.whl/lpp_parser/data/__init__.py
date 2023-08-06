import pathlib
import json

_CWDIR = pathlib.Path(__file__).parent


with open(_CWDIR.joinpath("elem_z_map.json"), "r") as fp:
    ELEM_Z_MAP = json.load(fp)

