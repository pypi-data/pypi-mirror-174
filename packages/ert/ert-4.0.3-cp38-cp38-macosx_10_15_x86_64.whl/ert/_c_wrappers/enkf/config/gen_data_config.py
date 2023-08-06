#  Copyright (C) 2012  Equinor ASA, Norway.
#
#  The file 'gen_data_config.py' is part of ERT - Ensemble based Reservoir Tool.
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
from typing import List

from cwrap import BaseCClass

from ert._c_wrappers import ResPrototype
from ert._c_wrappers.enkf.enums import GenDataFileType


class GenDataConfig(BaseCClass):
    TYPE_NAME = "gen_data_config"

    _alloc = ResPrototype(
        "void* gen_data_config_alloc_GEN_DATA_result( char* , gen_data_file_format_type)",  # noqa
        bind=False,
    )
    _free = ResPrototype("void  gen_data_config_free( gen_data_config )")
    _get_output_format = ResPrototype(
        "gen_data_file_format_type gen_data_config_get_output_format(gen_data_config)"
    )
    _get_input_format = ResPrototype(
        "gen_data_file_format_type gen_data_config_get_input_format(gen_data_config)"
    )
    _get_template_file = ResPrototype(
        "char* gen_data_config_get_template_file(gen_data_config)"
    )
    _get_template_key = ResPrototype(
        "char* gen_data_config_get_template_key(gen_data_config)"
    )
    _get_initial_size = ResPrototype(
        "int   gen_data_config_get_initial_size(gen_data_config)"
    )
    _has_report_step = ResPrototype(
        "bool  gen_data_config_has_report_step(gen_data_config, int)"
    )
    _get_data_size = ResPrototype(
        "int   gen_data_config_get_data_size__(gen_data_config , int)"
    )
    _get_key = ResPrototype("char* gen_data_config_get_key(gen_data_config)")
    _get_active_mask = ResPrototype(
        "bool_vector_ref gen_data_config_get_active_mask(gen_data_config)"
    )
    _get_num_report_step = ResPrototype(
        "int   gen_data_config_num_report_step(gen_data_config)"
    )
    _iget_report_step = ResPrototype(
        "int   gen_data_config_iget_report_step(gen_data_config, int)"
    )

    def __init__(self, key, input_format=GenDataFileType.ASCII):
        # Can currently only create GEN_DATA instances which should be used
        # as result variables.
        c_pointer = self._alloc(key, input_format)
        super().__init__(c_pointer)

    def get_template_file(self):
        return self._get_template_file()

    def get_template_key(self):
        return self._get_template_key()

    def getDataSize(self, report_step):
        data_size = self._get_data_size(report_step)
        if data_size < 0:
            raise ValueError(
                f"No data has been loaded for {self.getName()} "
                f"at report step:{report_step} "
            )
        return data_size

    def getActiveMask(self):
        return self._get_active_mask()

    def getName(self):
        return self.name()

    def name(self):
        return self._get_key()

    def get_initial_size(self) -> int:
        return self._get_initial_size()

    def getOutputFormat(self):
        return self._get_output_format()

    def getInputFormat(self):
        return self._get_input_format()

    def free(self):
        self._free()

    def __repr__(self):
        return (
            f"GenDataConfig(name = {self.name()}, "
            f"template_key = {self.get_template_key()}, "
            f"initial_size = {self.get_initial_size()}) {self._ad_str()}"
        )

    def hasReportStep(self, report_step) -> bool:
        return self._has_report_step(report_step)

    def getNumReportStep(self) -> int:
        return self._get_num_report_step()

    def getReportStep(self, index) -> int:
        return self._iget_report_step(index)

    def getReportSteps(self) -> List[int]:
        return [self.getReportStep(index) for index in range(self.getNumReportStep())]

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other) -> bool:
        if self.getName() != other.getName():
            return False

        if self.get_template_key() != other.get_template_key():
            return False

        if self.getInputFormat() != other.getInputFormat():
            return False

        if self.getOutputFormat() != other.getOutputFormat():
            return False

        if self.getReportSteps() != other.getReportSteps():
            return False

        return True
