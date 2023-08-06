#  Copyright (C) 2011  Equinor ASA, Norway.
#
#  The file '__init__.py' is part of ERT - Ensemble based Reservoir Tool.
#
#  ERT is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ERT is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html>
#  for more details.
"""
Ert - Ensemble Reservoir Tool - a package for reservoir modeling.
"""
import os.path
import warnings

import ecl  # This needs to be here for ... reasons

warnings.filterwarnings(action="always", category=DeprecationWarning, module=r"res|ert")

from cwrap import Prototype  # noqa

try:
    from ._version import version as __version__
except ImportError:
    pass


def _load_lib():
    import ctypes

    import ert._clib

    lib = ctypes.CDLL(ert._clib.__file__)  # pylint: disable=no-member

    # Configure site_config to be a ctypes.CFUNCTION with type:
    # void set_site_config(char *);
    site_config = lib.set_site_config
    site_config.restype = None
    site_config.argtypes = (ctypes.c_char_p,)

    # Find share/ert
    from pathlib import Path

    path = Path(__file__).parent
    for p in path.parents:
        npath = p / "ert" / "shared" / "share" / "ert" / "site-config"
        if npath.is_file():
            path = npath
            break
    else:
        raise ImportError("Could not find `share/ert/site-config`")

    # Set site-config to point to [PREFIX]/share/ert/site-config
    site_config(str(path).encode("utf-8"))

    return lib


class ResPrototype(Prototype):
    lib = _load_lib()

    def __init__(self, prototype, bind=True):
        super().__init__(ResPrototype.lib, prototype, bind=bind)


RES_LIB = ResPrototype.lib

from ecl.util.util import updateAbortSignals  # noqa

updateAbortSignals()


def root():
    """
    Will print the filesystem root of the current ert package.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
