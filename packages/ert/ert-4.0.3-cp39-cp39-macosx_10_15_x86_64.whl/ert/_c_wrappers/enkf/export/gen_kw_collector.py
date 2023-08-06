from typing import List, Optional

from pandas import DataFrame

from ert import _clib
from ert._c_wrappers.enkf import EnKFMain
from ert._c_wrappers.enkf.enkf_fs import EnkfFs
from ert._c_wrappers.enkf.enums import RealizationStateEnum


class GenKwCollector:
    @staticmethod
    def createActiveList(fs: EnkfFs) -> List[int]:
        ens_mask = fs.getStateMap().selectMatching(
            RealizationStateEnum.STATE_INITIALIZED
            | RealizationStateEnum.STATE_HAS_DATA,
        )
        return [index for index, active in enumerate(ens_mask) if active]

    @staticmethod
    def getAllGenKwKeys(ert: EnKFMain) -> List[str]:
        return ert.getKeyManager().genKwKeys()

    @staticmethod
    def loadAllGenKwData(
        ert: EnKFMain,
        case_name: str,
        keys: Optional[List[str]] = None,
        realization_index: Optional[int] = None,
    ) -> DataFrame:
        fs = ert.getEnkfFsManager().getFileSystem(case_name, read_only=True)

        realizations = GenKwCollector.createActiveList(fs)

        if realization_index is not None:
            if realization_index not in realizations:
                raise IndexError(f"No such realization ({realization_index})")
            realizations = [realization_index]

        gen_kw_keys = ert.getKeyManager().genKwKeys()

        if keys is not None:
            gen_kw_keys = [
                key for key in keys if key in gen_kw_keys
            ]  # ignore keys that doesn't exist

        gen_kw_array = _clib.enkf_fs_keyword_data.keyword_data_get_realizations(
            ert.ensembleConfig(), fs, gen_kw_keys, realizations
        )
        gen_kw_data = DataFrame(
            data=gen_kw_array, index=realizations, columns=gen_kw_keys
        )

        gen_kw_data.index.name = "Realization"
        return gen_kw_data
