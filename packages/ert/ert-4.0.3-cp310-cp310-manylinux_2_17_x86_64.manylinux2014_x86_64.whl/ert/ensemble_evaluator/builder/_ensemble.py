import logging
from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Sequence, Union

from cloudevents.conversion import to_json
from cloudevents.http import CloudEvent

from ert.ensemble_evaluator import state
from ert.ensemble_evaluator.snapshot import (
    Job,
    PartialSnapshot,
    Realization,
    Snapshot,
    SnapshotDict,
    Step,
)
from ert.ensemble_evaluator.tracker.ensemble_state_tracker import EnsembleStateTracker
from ert.serialization import evaluator_marshaller
from ert.shared.ensemble_evaluator.client import Client

from ._realization import _Realization

if TYPE_CHECKING:
    import asyncio

    from ert.shared.ensemble_evaluator.config import EvaluatorServerConfig

logger = logging.getLogger(__name__)


class _Ensemble:
    def __init__(
        self, reals: Sequence[_Realization], metadata: Mapping[str, Any], id_: str
    ) -> None:
        self.reals = reals
        self.metadata = metadata
        self._snapshot = self._create_snapshot()
        self.status = self._snapshot.status
        self._status_tracker = EnsembleStateTracker(self._snapshot.status)
        self._id: str = id_

    def __repr__(self) -> str:
        return f"Ensemble with {len(self.reals)} members"

    def evaluate(self, config: "EvaluatorServerConfig") -> None:
        pass

    async def evaluate_async(
        self, config: "EvaluatorServerConfig", experiment_id: str
    ) -> None:
        pass

    def cancel(self) -> None:
        pass

    @property
    def id_(self) -> str:
        return self._id

    @property
    def cancellable(self) -> bool:
        return False

    @property
    def active_reals(self) -> Sequence[_Realization]:
        return list(filter(lambda real: real.active, self.reals))

    @property
    def snapshot(self) -> Snapshot:
        return self._snapshot

    def update_snapshot(self, events: List[CloudEvent]) -> PartialSnapshot:
        snapshot_mutate_event = PartialSnapshot(self._snapshot)
        for event in events:
            snapshot_mutate_event.from_cloudevent(event)
        self._snapshot.merge_event(snapshot_mutate_event)
        if self.status != self._snapshot.status:
            self.status = self._status_tracker.update_state(self._snapshot.status)
        return snapshot_mutate_event

    async def send_cloudevent(  # pylint: disable=too-many-arguments
        self,
        url: str,
        event: CloudEvent,
        token: Optional[str] = None,
        cert: Optional[Union[str, bytes]] = None,
        retries: int = 10,
    ) -> None:
        async with Client(url, token, cert, max_retries=retries) as client:
            await client._send(to_json(event, data_marshaller=evaluator_marshaller))

    # TODO: make legacy-only?
    # See https://github.com/equinor/ert/issues/3456
    @property
    @abstractmethod
    def output_bus(
        self,
    ) -> "asyncio.Queue[CloudEvent]":
        raise NotImplementedError

    # TODO: make legacy-only?
    # See https://github.com/equinor/ert/issues/3456
    async def queue_cloudevent(
        self,
        event: CloudEvent,
    ) -> None:
        self.output_bus.put_nowait(event)

    def get_successful_realizations(self) -> int:
        return self._snapshot.get_successful_realizations()

    def _create_snapshot(self) -> Snapshot:
        reals: Dict[str, Realization] = {}
        for real in self.active_reals:
            reals[str(real.iens)] = Realization(
                active=True,
                status=state.REALIZATION_STATE_WAITING,
            )
            for step in real.steps:
                reals[str(real.iens)].steps[str(step.id_)] = Step(
                    status=state.STEP_STATE_UNKNOWN
                )
                for job in step.jobs:
                    reals[str(real.iens)].steps[str(step.id_)].jobs[str(job.id_)] = Job(
                        status=state.JOB_STATE_START,
                        index=job.index,
                        data={},
                        name=job.name,
                    )
        top = SnapshotDict(
            reals=reals,
            status=state.ENSEMBLE_STATE_UNKNOWN,
            metadata=self.metadata,
        )

        return Snapshot(top.dict())
