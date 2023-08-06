#  Copyright (C) 2016  Equinor ASA, Norway.
#
#  This file is part of ERT - Ensemble based Reservoir Tool.
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
import ctypes

from cwrap import BaseCClass

from ert._c_wrappers.enkf.config import FieldConfig


class BlockDataConfig(BaseCClass):
    TYPE_NAME = "block_data_config"

    def __init__(self):
        raise NotImplementedError("Cannot instantiate BlockDataConfig!")

    @classmethod
    def from_param(cls, c_class_object):
        if c_class_object is None:
            return ctypes.c_void_p()
        elif isinstance(c_class_object, FieldConfig):
            return FieldConfig.from_param(c_class_object)

        else:
            raise ValueError("Currently ONLY field data is supported")
