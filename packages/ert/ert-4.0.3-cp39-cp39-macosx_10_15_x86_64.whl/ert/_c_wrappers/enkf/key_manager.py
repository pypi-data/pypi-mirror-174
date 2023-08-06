import weakref
from typing import TYPE_CHECKING, Dict, List

from ert._c_wrappers.enkf.config import GenKwConfig
from ert._c_wrappers.enkf.enums import EnkfObservationImplementationType, ErtImplType

if TYPE_CHECKING:
    from ert._c_wrappers.enkf import EnKFMain, EnsembleConfig
    from ert._c_wrappers.enkf.config.gen_kw_config import PriorDict


class KeyManager:
    def __init__(self, ert: "EnKFMain"):
        super().__init__()
        self.__ert_ref = weakref.ref(ert)

        self.__all_keys = None
        self.__all_keys_with_observations = None
        self.__summary_keys = None
        self.__summary_keys_with_observations = None
        self.__gen_data_keys = None
        self.__gen_data_keys_with_observations = None
        self.__gen_kw_keys = None
        self.__misfit_keys = None

    def _ert(self) -> "EnKFMain":
        ert = self.__ert_ref()
        if ert is None:
            raise RuntimeError("The reference EnKFMain instance has been deleted")
        return ert

    def ensembleConfig(self) -> "EnsembleConfig":
        return self._ert().ensembleConfig()

    def summaryKeys(self) -> List[str]:
        if self.__summary_keys is None:
            self.__summary_keys = sorted(
                list(self.ensembleConfig().getKeylistFromImplType(ErtImplType.SUMMARY)),
                key=lambda k: k.lower(),
            )

        return self.__summary_keys

    def summaryKeysWithObservations(self) -> List[str]:
        if self.__summary_keys_with_observations is None:
            self.__summary_keys_with_observations = sorted(
                [
                    key
                    for key in self.summaryKeys()
                    if len(self.ensembleConfig().getNode(key).getObservationKeys()) > 0
                ],
                key=lambda k: k.lower(),
            )

        return self.__summary_keys_with_observations

    def genKwKeys(self) -> List[str]:
        if self.__gen_kw_keys is None:
            gen_kw_keys = list(
                self.ensembleConfig().getKeylistFromImplType(ErtImplType.GEN_KW)
            )

            gen_kw_list = []
            for key in gen_kw_keys:
                enkf_config_node = self.ensembleConfig().getNode(key)
                gen_kw_config = enkf_config_node.getModelConfig()
                assert isinstance(gen_kw_config, GenKwConfig)

                for keyword_index, keyword in enumerate(gen_kw_config):
                    gen_kw_list.append(f"{key}:{keyword}")

                    if gen_kw_config.shouldUseLogScale(keyword_index):
                        gen_kw_list.append(f"LOG10_{key}:{keyword}")

            self.__gen_kw_keys = sorted(gen_kw_list, key=lambda k: k.lower())

        return self.__gen_kw_keys

    def genDataKeys(self) -> List[str]:
        if self.__gen_data_keys is None:
            gen_data_keys = self.ensembleConfig().getKeylistFromImplType(
                ErtImplType.GEN_DATA
            )
            gen_data_list = []
            for key in gen_data_keys:
                enkf_config_node = self._ert().ensembleConfig().getNode(key)
                gen_data_config = enkf_config_node.getDataModelConfig()

                for report_step in gen_data_config.getReportSteps():
                    gen_data_list.append(f"{key}@{report_step}")

            self.__gen_data_keys = sorted(gen_data_list, key=lambda k: k.lower())

        return self.__gen_data_keys

    def genDataKeysWithObservations(self) -> List[str]:
        if self.__gen_data_keys_with_observations is None:
            enkf_obs = self._ert().getObservations()
            gen_data_obs_keys = []
            for obs_vector in enkf_obs:
                if (
                    obs_vector.getImplementationType()
                    is EnkfObservationImplementationType.GEN_OBS
                ):
                    report_step = obs_vector.activeStep()
                    key = obs_vector.getDataKey()

                    gen_data_key = f"{key}@{report_step}"
                    if gen_data_key in self.genDataKeys():
                        gen_data_obs_keys.append(gen_data_key)

            self.__gen_data_keys_with_observations = gen_data_obs_keys

        return self.__gen_data_keys_with_observations

    def misfitKeys(self, sort_keys=True) -> List[str]:
        if self.__misfit_keys is None:
            keys = []
            for obs_vector in self._ert().getObservations():
                keys.append(f"MISFIT:{obs_vector.getObservationKey()}")

            keys.append("MISFIT:TOTAL")

            self.__misfit_keys = (
                sorted(keys, key=lambda k: k.lower()) if sort_keys else keys
            )

        return self.__misfit_keys

    def allDataTypeKeys(self) -> List[str]:
        if self.__all_keys is None:
            self.__all_keys = self.summaryKeys() + self.genKwKeys() + self.genDataKeys()

        return self.__all_keys

    def allDataTypeKeysWithObservations(self) -> List[str]:
        if self.__all_keys_with_observations is None:
            self.__all_keys_with_observations = (
                self.summaryKeysWithObservations() + self.genDataKeysWithObservations()
            )

        return self.__all_keys_with_observations

    def isKeyWithObservations(self, key: str) -> bool:
        return key in self.allDataTypeKeysWithObservations()

    def isSummaryKey(self, key: str) -> bool:
        return key in self.summaryKeys()

    def isGenKwKey(self, key: str) -> bool:
        return key in self.genKwKeys()

    def isGenDataKey(self, key: str) -> bool:
        return key in self.genDataKeys()

    def isMisfitKey(self, key: str) -> bool:
        return key in self.misfitKeys()

    def gen_kw_priors(
        self,
    ) -> Dict[str, List["PriorDict"]]:
        gen_kw_keys = self.ensembleConfig().getKeylistFromImplType(ErtImplType.GEN_KW)
        all_gen_kw_priors = {}
        for key in gen_kw_keys:
            enkf_config_node = self.ensembleConfig().getNode(key)
            gen_kw_config = enkf_config_node.getModelConfig()
            all_gen_kw_priors[key] = gen_kw_config.get_priors()

        return all_gen_kw_priors
