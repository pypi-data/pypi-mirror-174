#  Copyright (C) 2012  Equinor ASA, Norway.
#
#  The file 'analysis_config.py' is part of ERT - Ensemble based Reservoir Tool.
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

from os.path import realpath
from typing import List, Optional

from cwrap import BaseCClass

from ert import _clib
from ert._c_wrappers import ResPrototype
from ert._c_wrappers.analysis import AnalysisModule
from ert._c_wrappers.config import ConfigContent
from ert._c_wrappers.enkf.analysis_iter_config import AnalysisIterConfig
from ert._c_wrappers.enkf.config_keys import ConfigKeys


class AnalysisConfig(BaseCClass):
    TYPE_NAME = "analysis_config"

    _alloc = ResPrototype("void* analysis_config_alloc(config_content)", bind=False)
    _alloc_full = ResPrototype(
        "void* analysis_config_alloc_full(double, bool, "
        "int, char*, double, bool, bool, "
        "double, int, int, char*, int, int)",
        bind=False,
    )

    _add_module_copy = ResPrototype(
        "void analysis_config_add_module_copy( analysis_config, char* , char* )"
    )

    _free = ResPrototype("void analysis_config_free( analysis_config )")
    _get_rerun = ResPrototype("int analysis_config_get_rerun( analysis_config )")
    _set_rerun = ResPrototype("void analysis_config_set_rerun( analysis_config, bool)")
    _get_rerun_start = ResPrototype(
        "int analysis_config_get_rerun_start( analysis_config )"
    )
    _set_rerun_start = ResPrototype(
        "void analysis_config_set_rerun_start( analysis_config, int)"
    )
    _get_log_path = ResPrototype("char* analysis_config_get_log_path( analysis_config)")
    _set_log_path = ResPrototype(
        "void analysis_config_set_log_path( analysis_config, char*)"
    )
    _get_iter_config = ResPrototype(
        "analysis_iter_config_ref analysis_config_get_iter_config(analysis_config)"
    )
    _get_max_runtime = ResPrototype(
        "int analysis_config_get_max_runtime(analysis_config)"
    )
    _set_max_runtime = ResPrototype(
        "void analysis_config_set_max_runtime(analysis_config, int)"
    )
    _get_stop_long_running = ResPrototype(
        "bool analysis_config_get_stop_long_running(analysis_config)"
    )
    _set_stop_long_running = ResPrototype(
        "void analysis_config_set_stop_long_running(analysis_config, bool)"
    )
    _get_active_module_name = ResPrototype(
        "char* analysis_config_get_active_module_name(analysis_config)"
    )
    _get_module = ResPrototype(
        "analysis_module_ref analysis_config_get_module(analysis_config, char*)"
    )
    _select_module = ResPrototype(
        "bool analysis_config_select_module(analysis_config, char*)"
    )
    _has_module = ResPrototype(
        "bool analysis_config_has_module(analysis_config, char*)"
    )
    _get_alpha = ResPrototype("double analysis_config_get_alpha(analysis_config)")
    _set_alpha = ResPrototype("void analysis_config_set_alpha(analysis_config, double)")
    _get_std_cutoff = ResPrototype(
        "double analysis_config_get_std_cutoff(analysis_config)"
    )
    _set_std_cutoff = ResPrototype(
        "void analysis_config_set_std_cutoff(analysis_config, double)"
    )
    _set_global_std_scaling = ResPrototype(
        "void analysis_config_set_global_std_scaling(analysis_config, double)"
    )
    _get_global_std_scaling = ResPrototype(
        "double analysis_config_get_global_std_scaling(analysis_config)"
    )
    _get_min_realizations = ResPrototype(
        "int analysis_config_get_min_realisations(analysis_config)"
    )

    def __init__(
        self,
        config_content: Optional[ConfigContent] = None,
        config_dict=None,
    ):
        configs = sum(1 for x in [config_content, config_dict] if x is not None)

        if configs > 1:
            raise ValueError(
                "Attempting to create AnalysisConfig object "
                "with multiple config objects"
            )

        if configs == 0:
            raise ValueError(
                "Error trying to create AnalysisConfig without any configuration"
            )

        c_ptr = None
        if config_content is not None:
            c_ptr = self._alloc(config_content)
            if c_ptr:
                super().__init__(c_ptr)
            else:
                raise ValueError("Failed to construct AnalysisConfig instance.")

        if config_dict is not None:
            c_ptr = self._alloc_full(
                config_dict.get(ConfigKeys.ALPHA_KEY, 3.0),
                config_dict.get(ConfigKeys.RERUN_KEY, False),
                config_dict.get(ConfigKeys.RERUN_START_KEY, 0),
                realpath(config_dict.get(ConfigKeys.UPDATE_LOG_PATH, "update_log")),
                config_dict.get(ConfigKeys.STD_CUTOFF_KEY, 1e-6),
                config_dict.get(ConfigKeys.STOP_LONG_RUNNING, False),
                config_dict.get(ConfigKeys.SINGLE_NODE_UPDATE, False),
                config_dict.get(ConfigKeys.GLOBAL_STD_SCALING, 1.0),
                config_dict.get(ConfigKeys.MAX_RUNTIME, 0),
                config_dict.get(ConfigKeys.MIN_REALIZATIONS, 0),
                config_dict.get(ConfigKeys.ITER_CASE, "ITERATED_ENSEMBLE_SMOOTHER%d"),
                config_dict.get(ConfigKeys.ITER_COUNT, 4),
                config_dict.get(ConfigKeys.ITER_RETRY_COUNT, 4),
            )
            if c_ptr:
                super().__init__(c_ptr)

                # copy modules
                analysis_copy_list = config_dict.get(ConfigKeys.ANALYSIS_COPY, [])
                for analysis_copy in analysis_copy_list:
                    self._add_module_copy(
                        analysis_copy[ConfigKeys.SRC_NAME],
                        analysis_copy[ConfigKeys.DST_NAME],
                    )

                # set var list
                set_var_list = config_dict.get(ConfigKeys.ANALYSIS_SET_VAR, [])
                for set_var in set_var_list:
                    module = self._get_module(set_var[ConfigKeys.MODULE_NAME])
                    module._set_var(
                        set_var[ConfigKeys.VAR_NAME], str(set_var[ConfigKeys.VALUE])
                    )

                if ConfigKeys.ANALYSIS_SELECT in config_dict:
                    self._select_module(config_dict[ConfigKeys.ANALYSIS_SELECT])

            else:
                raise ValueError("Failed to construct AnalysisConfig from dict.")

    def get_rerun(self):
        return self._get_rerun()

    def set_rerun(self, rerun):
        self._set_rerun(rerun)

    def get_rerun_start(self):
        return self._get_rerun_start()

    def set_rerun_start(self, index):
        self._set_rerun_start(index)

    def get_log_path(self) -> str:
        return self._get_log_path()

    def set_log_path(self, path: str):
        self._set_log_path(path)

    def getEnkfAlpha(self) -> float:
        return self._get_alpha()

    def setEnkfAlpha(self, alpha):
        self._set_alpha(alpha)

    def getStdCutoff(self) -> float:
        return self._get_std_cutoff()

    def setStdCutoff(self, std_cutoff: float):
        self._set_std_cutoff(std_cutoff)

    def getAnalysisIterConfig(self) -> AnalysisIterConfig:
        return self._get_iter_config().setParent(self)

    def get_stop_long_running(self) -> bool:
        return self._get_stop_long_running()

    def set_stop_long_running(self, stop_long_running):
        self._set_stop_long_running(stop_long_running)

    def get_max_runtime(self) -> int:
        return self._get_max_runtime()

    def set_max_runtime(self, max_runtime: int):
        self._set_max_runtime(max_runtime)

    def free(self):
        self._free()

    def activeModuleName(self) -> str:
        return self._get_active_module_name()

    def getModuleList(self) -> List[str]:
        return _clib.analysis_config_module_names(self)

    def getModule(self, module_name: str) -> AnalysisModule:
        return self._get_module(module_name)

    def hasModule(self, module_name: str) -> bool:
        return self._has_module(module_name)

    def selectModule(self, module_name: str) -> bool:
        return self._select_module(module_name)

    def getActiveModule(self) -> AnalysisModule:
        return self.getModule(self.activeModuleName())

    def setGlobalStdScaling(self, std_scaling: float):
        self._set_global_std_scaling(std_scaling)

    def getGlobalStdScaling(self) -> float:
        return self._get_global_std_scaling()

    @property
    def minimum_required_realizations(self) -> int:
        return self._get_min_realizations()

    def haveEnoughRealisations(self, realizations) -> bool:
        return realizations >= self.minimum_required_realizations

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return (
            "AnalysisConfig(config_dict={"
            f"'UPDATE_LOG_PATH': {realpath(self.get_log_path())}, "
            f"'MAX_RUNTIME': {self.get_max_runtime()}, "
            f"'GLOBAL_STD_SCALING': {self.getGlobalStdScaling()}, "
            f"'STOP_LONG_RUNNING': {self.get_stop_long_running()}, "
            f"'STD_CUTOFF': {self.getStdCutoff()}, "
            f"'ENKF_ALPHA': {self.getEnkfAlpha()}, "
            f"'RERUN': {self.get_rerun()}, "
            f"'RERUN_START': {self.get_rerun_start()}, "
            f"'ANALYSIS_SELECT': {self.activeModuleName()}, "
            f"'MODULE_LIST': {self.getModuleList()}, "
            f"'ITER_CONFIG': {self.getAnalysisIterConfig()}, "
            "})"
        )

    def __eq__(self, other):
        if realpath(self.get_log_path()) != realpath(other.get_log_path()):
            return False

        if self.get_max_runtime() != other.get_max_runtime():
            return False

        if self.getGlobalStdScaling() != other.getGlobalStdScaling():
            return False

        if self.get_stop_long_running() != other.get_stop_long_running():
            return False

        if self.getStdCutoff() != other.getStdCutoff():
            return False

        if self.getEnkfAlpha() != other.getEnkfAlpha():
            return False

        if self.get_rerun() != other.get_rerun():
            return False

        if self.get_rerun_start() != other.get_rerun_start():
            return False

        if set(self.getModuleList()) != set(other.getModuleList()):
            return False

        if self.activeModuleName() != other.activeModuleName():
            return False

        if self.getAnalysisIterConfig() != other.getAnalysisIterConfig():
            return False

        # compare each module
        for a in self.getModuleList():
            if self.getModule(a) != other.getModule(a):
                return False

        return True
