#  Copyright (C) 2012  Equinor ASA, Norway.
#
#  The file 'gen_kw_config.py' is part of ERT - Ensemble based Reservoir Tool.
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
import os
from typing import TYPE_CHECKING, Dict, List, TypedDict

from cwrap import BaseCClass
from ecl.util.util import StringList

from ert._c_wrappers import ResPrototype

if TYPE_CHECKING:

    class PriorDict(TypedDict):
        key: str
        function: str
        parameters: Dict[str, float]


class GenKwConfig(BaseCClass):
    TYPE_NAME = "gen_kw_config"

    _free = ResPrototype("void  gen_kw_config_free( gen_kw_config )")
    _alloc_empty = ResPrototype(
        "void* gen_kw_config_alloc_empty( char*, char* )", bind=False
    )
    _get_template_file = ResPrototype(
        "char* gen_kw_config_get_template_file(gen_kw_config)"
    )
    _set_template_file = ResPrototype(
        "void  gen_kw_config_set_template_file(gen_kw_config , char*)"
    )
    _get_parameter_file = ResPrototype(
        "char* gen_kw_config_get_parameter_file(gen_kw_config)"
    )
    _set_parameter_file = ResPrototype(
        "void  gen_kw_config_set_parameter_file(gen_kw_config, char*)"
    )
    _alloc_name_list = ResPrototype(
        "stringlist_obj gen_kw_config_alloc_name_list(gen_kw_config)"
    )
    _should_use_log_scale = ResPrototype(
        "bool  gen_kw_config_should_use_log_scale(gen_kw_config, int)"
    )
    _get_key = ResPrototype("char* gen_kw_config_get_key(gen_kw_config)")
    _get_tag_fmt = ResPrototype("char* gen_kw_config_get_tag_fmt(gen_kw_config)")
    _size = ResPrototype("int   gen_kw_config_get_data_size(gen_kw_config)")
    _iget_name = ResPrototype("char* gen_kw_config_iget_name(gen_kw_config, int)")
    _get_function_type = ResPrototype(
        "char* gen_kw_config_iget_function_type(gen_kw_config, int)"
    )
    _get_function_parameter_names = ResPrototype(
        "stringlist_ref gen_kw_config_iget_function_parameter_names(gen_kw_config, int)"
    )
    _get_function_parameter_values = ResPrototype(
        "double_vector_ref gen_kw_config_iget_function_parameter_values(gen_kw_config, int)"  # noqa
    )

    def __init__(self, key, template_file, parameter_file, tag_fmt="<%s>"):
        """
        @type key: str
        @type tag_fmt: str
        """
        if not os.path.isfile(template_file):
            raise IOError(f"No such file:{template_file}")

        if not os.path.isfile(parameter_file):
            raise IOError(f"No such file:{parameter_file}")

        c_ptr = self._alloc_empty(key, tag_fmt)
        if c_ptr:
            super().__init__(c_ptr)
        else:
            raise ValueError(
                "Could not instantiate GenKwConfig with "
                f'key="{key}" and tag_fmt="{tag_fmt}"'
            )
        self._set_parameter_file(parameter_file)
        self._set_template_file(template_file)
        self.__str__ = self.__repr__

    def getTemplateFile(self):
        path = self._get_template_file()
        return None if path is None else os.path.abspath(path)

    def getParameterFile(self):
        path = self._get_parameter_file()
        return None if path is None else os.path.abspath(path)

    def getKeyWords(self) -> StringList:
        """@rtype: StringList"""
        return self._alloc_name_list()

    def shouldUseLogScale(self, index):
        """@rtype: bool"""
        return self._should_use_log_scale(index)

    def free(self):
        self._free()

    def __repr__(self):
        return (
            f'GenKwConfig(key = "{self.getKey()}", '
            f'tag_fmt = "{self.tag_fmt}") at 0x{self._address():x}'
        )

    def getKey(self):
        """@rtype: str"""
        return self._get_key()

    @property
    def tag_fmt(self):
        return self._get_tag_fmt()

    def __len__(self):
        return self._size()

    def __getitem__(self, index):
        """@rtype: str"""
        return self._iget_name(index)

    def __iter__(self):
        index = 0
        while index < len(self):
            yield self[index]
            index += 1

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        """@rtype: bool"""
        if self.getTemplateFile() != other.getTemplateFile():
            return False

        if self.getParameterFile() != other.getParameterFile():
            return False

        if self.getKey() != other.getKey():
            return False

        return True

    def get_priors(self) -> List["PriorDict"]:
        """
        @rtype: list
        [
            {
                "key" : "<key>",
                "function" : "<function_type>"
                "parameters" : {
                    "<name>" : "<value>"
                }
            }
        ]
        """
        priors: List["PriorDict"] = []
        keys = self.getKeyWords()
        for i, key in enumerate(keys):
            function_type = self._get_function_type(i)
            parameter_names = self._get_function_parameter_names(i)
            parameter_values = self._get_function_parameter_values(i)
            priors.append(
                {
                    "key": key,
                    "function": function_type,
                    "parameters": dict(zip(parameter_names, parameter_values)),
                }
            )
        return priors
