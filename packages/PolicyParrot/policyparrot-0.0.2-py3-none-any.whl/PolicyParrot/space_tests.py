"""Useful tests for sanity checking buffer data.

Author: WillDudley
"""
from __future__ import annotations

from gymnasium.spaces import Box, Discrete
import torch


def space_tests(space: Box | Discrete, recorded_data: torch.Tensor, next_recorded_data: torch.Tensor = None):
    if recorded_data.shape != space.shape:
        raise ValueError(
            f"Observation dimensionality mismatch!"
            f"Given |S|: {space.shape}. Observation shape: {recorded_data.shape}."
        )

    if type(space) == Box:
        lower_bound = min(space.low)
        upper_bound = max(space.high)
    elif type(space) == Discrete:
        lower_bound = space.start
        upper_bound = lower_bound + space.n
    else:
        raise NotImplementedError(f"Observation space '{type(space)}' not supported!")
    if recorded_data.min() < lower_bound:
        raise ValueError(
            f"Observation minimum value ({recorded_data.min()}) is smaller than the given lower bound ({lower_bound})."
        )
    if recorded_data.max() > upper_bound:
        raise ValueError(
            f"Observation maximum value ({recorded_data.max()}) is larger than the given upper bound ({upper_bound})."
        )

    if next_recorded_data is not None:
        if next_recorded_data.shape != next_recorded_data.shape:
            raise ValueError(
                f"Next observation dimensionality mismatch!"
                f"Given |S|: {space.shape}. Next observation shape: {recorded_data.shape}."
            )

        if next_recorded_data.min() < lower_bound:
            raise ValueError(
                f"Next observation minimum value ({next_recorded_data.min()}) is smaller than the given lower bound ({lower_bound})."
            )
        if next_recorded_data.max() > upper_bound:
            raise ValueError(
                f"Next observation maximum value ({next_recorded_data.max()}) is larger than the given upper bound ({upper_bound})."
            )
