from cwrap import BaseCClass
from ecl.util.util import CTime

from ert._c_wrappers import ResPrototype


class EnsemblePlotDataVector(BaseCClass):
    TYPE_NAME = "ensemble_plot_data_vector"

    _size = ResPrototype("int    enkf_plot_tvector_size(ensemble_plot_data_vector)")
    _get_value = ResPrototype(
        "double enkf_plot_tvector_iget_value(ensemble_plot_data_vector, int)"
    )
    _get_time = ResPrototype(
        "time_t enkf_plot_tvector_iget_time(ensemble_plot_data_vector, int)"
    )
    _is_active = ResPrototype(
        "bool   enkf_plot_tvector_iget_active(ensemble_plot_data_vector, int)"
    )

    def __init__(self):
        raise NotImplementedError("Class can not be instantiated directly!")

    def __len__(self):
        """@rtype: int"""
        return self._size()

    def getValue(self, index):
        """@rtype: float"""
        return self._get_value(index)

    def getTime(self, index) -> CTime:
        """@rtype: CTime"""
        return self._get_time(index)

    def isActive(self, index):
        """@rtype: bool"""
        return self._is_active(index)

    def __repr__(self):
        return f"EnsemblePlotDataVector(size = {len(self)}) {self._ad_str()}"
