"""Small, dependency-free completed-transition memory for an RLT pilot.

This is a timing/provenance prototype, not the Zeva neural CTE or a trained policy.
Every stored effect must come from an already executed, observed transition.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt


Vector = tuple[float, ...]


def _vector(values: Vector, name: str) -> Vector:
    if not values or not all(isfinite(v) for v in values):
        raise ValueError(f"{name} must be a nonempty finite vector")
    return values


def _cosine(a: Vector, b: Vector) -> float:
    if len(a) != len(b):
        raise ValueError("phase dimension mismatch")
    an = sqrt(sum(v * v for v in a))
    bn = sqrt(sum(v * v for v in b))
    return sum(x * y for x, y in zip(a, b)) / (an * bn) if an and bn else 0.0


@dataclass(frozen=True)
class EpisodeKey:
    session_id: str
    task_id: str
    environment_seed: int
    controller_version: str

    def __post_init__(self) -> None:
        if not self.session_id or not self.task_id or not self.controller_version:
            raise ValueError("session, task and controller version are required")
        if self.environment_seed < 0:
            raise ValueError("environment seed must be nonnegative")


@dataclass(frozen=True)
class CompletedTransition:
    key: EpisodeKey
    attempt_id: int
    decision_step: int
    observation_step: int
    phase_at_decision: Vector
    executed_action: Vector
    measured_delta: Vector
    effect_embedding: Vector
    label_source: str

    def __post_init__(self) -> None:
        if self.attempt_id < 0 or self.decision_step < 0:
            raise ValueError("attempt and decision step must be nonnegative")
        if self.observation_step <= self.decision_step:
            raise ValueError("effect must be observed after the decision")
        for name in ("phase_at_decision", "executed_action", "measured_delta", "effect_embedding"):
            _vector(getattr(self, name), name)
        if not self.label_source:
            raise ValueError("label source is required")


@dataclass(frozen=True)
class RetrievedEvidence:
    transition: CompletedTransition
    phase_similarity: float


class AttemptMemory:
    """BIT resets on retry; PIM survives retries only inside the same episode."""

    def __init__(self, bit_capacity: int = 4, pim_capacity: int = 64) -> None:
        if min(bit_capacity, pim_capacity) < 1:
            raise ValueError("capacities must be positive")
        self.bit_capacity = bit_capacity
        self.pim_capacity = pim_capacity
        self._key: EpisodeKey | None = None
        self._attempt_id: int | None = None
        self._bit: list[CompletedTransition] = []
        self._pim: list[CompletedTransition] = []
        self._last_observation_step = -1

    def start_episode(self, key: EpisodeKey) -> None:
        self._key = key
        self._attempt_id = None
        self._bit.clear()
        self._pim.clear()
        self._last_observation_step = -1

    def start_attempt(self, attempt_id: int) -> None:
        if self._key is None or attempt_id < 0:
            raise ValueError("start an episode and supply a valid attempt")
        if self._attempt_id is None and attempt_id != 0:
            raise ValueError("the first attempt must be zero")
        if self._attempt_id is not None and attempt_id != self._attempt_id + 1:
            raise ValueError("attempts must advance exactly once")
        self._attempt_id = attempt_id
        self._bit.clear()
        self._last_observation_step = -1

    def write_completed(self, record: CompletedTransition) -> None:
        if self._key != record.key or self._attempt_id != record.attempt_id:
            raise ValueError("episode or attempt mismatch")
        if record.decision_step < self._last_observation_step:
            raise ValueError("overlapping or out-of-order transitions")
        if self._pim and len(self._pim[0].phase_at_decision) != len(record.phase_at_decision):
            raise ValueError("phase encoder/version changed within the episode")
        self._last_observation_step = record.observation_step
        self._bit.append(record)
        self._pim.append(record)
        del self._bit[:-self.bit_capacity]
        del self._pim[:-self.pim_capacity]

    def read(self, current_phase: Vector, decision_step: int, top_k: int = 4) -> tuple[tuple[CompletedTransition, ...], tuple[RetrievedEvidence, ...]]:
        """Call before policy action; the query uses current phase, never future effects."""
        if self._key is None or self._attempt_id is None:
            raise ValueError("start an episode and attempt before reading")
        _vector(current_phase, "current_phase")
        if decision_step < 0 or top_k < 1:
            raise ValueError("decision step and top_k must be valid")
        eligible = [r for r in self._pim if (r.attempt_id < self._attempt_id or r.observation_step <= decision_step)]
        ranked = sorted(
            (RetrievedEvidence(r, _cosine(current_phase, r.phase_at_decision)) for r in eligible),
            key=lambda item: item.phase_similarity,
            reverse=True,
        )
        recent = tuple(r for r in self._bit if r.observation_step <= decision_step)
        return recent, tuple(ranked[:top_k])
