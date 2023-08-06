#  Copyright (C) 2012 Equinor ASA, Norway.
#
#  The file 'summary_observation.py' is part of ERT - Ensemble based Reservoir Tool.
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

from cwrap import BaseCClass

from ert import _clib
from ert._c_wrappers import ResPrototype
from ert._c_wrappers.enkf.active_list import ActiveList


class SummaryObservation(BaseCClass):
    TYPE_NAME = "summary_obs"

    _alloc = ResPrototype(
        "void*  summary_obs_alloc(char*, char*, double, double)",
        bind=False,
    )
    _free = ResPrototype("void   summary_obs_free(summary_obs)")
    _get_value = ResPrototype("double summary_obs_get_value(summary_obs)")
    _get_std = ResPrototype("double summary_obs_get_std(summary_obs)")
    _get_std_scaling = ResPrototype("double summary_obs_get_std_scaling(summary_obs)")
    _get_summary_key = ResPrototype("char*  summary_obs_get_summary_key(summary_obs)")
    _set_std_scale = ResPrototype(
        "void   summary_obs_set_std_scale(summary_obs , double)"
    )

    def __init__(self, summary_key, observation_key, value, std):
        assert isinstance(summary_key, str)
        assert isinstance(observation_key, str)
        assert isinstance(value, float)
        assert isinstance(std, float)

        c_ptr = self._alloc(summary_key, observation_key, value, std)
        if c_ptr:
            super().__init__(c_ptr)
        else:
            raise ValueError(
                "Unable to construct SummaryObservation with given configuration!"
            )

    def getValue(self) -> float:
        return self._get_value()

    def getStandardDeviation(self) -> float:
        return self._get_std()

    def getStdScaling(self, index=0) -> float:
        return self._get_std_scaling()

    def set_std_scaling(self, scaling_factor: float) -> None:
        self._set_std_scale(scaling_factor)

    def __len__(self):
        return 1

    def getSummaryKey(self) -> str:
        return self._get_summary_key()

    def updateStdScaling(self, factor: float, active_list: ActiveList) -> None:
        _clib.local.summary_obs.update_std_scaling(self, factor, active_list)

    def free(self):
        self._free()

    def __repr__(self):
        sk = self.getSummaryKey()
        va = self.getValue()
        sd = self.getStandardDeviation()
        sc = self.getStdScaling()
        ad = self._address()
        fmt = (
            "SummaryObservation(key = %s, "
            "value = %f, std = %f, std_scaling = %f) at 0x%x"
        )
        return fmt % (sk, va, sd, sc, ad)
