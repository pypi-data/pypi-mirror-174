"""
These superclasses are NOT meant to provide inheritance of attributes. They are solely meant to assist in the standardisation of RL algorithms by encouraging the user to decompose algorithms into Actor, Critics, and Policies.
"""
from abc import ABC, abstractmethod

import torch
import torch.nn as nn


class Policy(ABC):
    """Abstract base class for all policies."""

    @abstractmethod
    def select_action(self, observation: torch.Tensor) -> torch.Tensor:
        """Select an action given the current state.
        :param observation: Tensor of the same shape as the observations
        :return: Tensor of the same shape as the actions
        """
        pass

    @abstractmethod
    def update(self, batch: dict) -> None:
        """Update the policy.
        :param batch:
        """
        pass


class Critic(ABC):
    def __init_subclass__(cls):
        assert issubclass(cls, nn.Module), "The Critic must inherit from `nn.Module`."

    @abstractmethod
    def forward(self, observation: torch.Tensor, action: torch.Tensor) -> torch.Tensor:
        pass

    @abstractmethod
    def loss(self, predicted_values: torch.Tensor, target_values: torch.Tensor) -> torch.Tensor:
        pass


class Actor(ABC):
    def __init_subclass__(cls):
        assert issubclass(cls, nn.Module), "The Actor must inherit from `nn.Module`."

    @abstractmethod
    def forward(self, observation: torch.Tensor) -> (torch.Tensor, torch.Tensor):
        pass

    @abstractmethod
    def get_action(self, observation: torch.Tensor) -> (torch.Tensor, torch.Tensor, torch.Tensor):
        pass

    @abstractmethod
    def loss(self, predicted_logprobs: torch.Tensor, target_logprobs: torch.Tensor) -> torch.Tensor:
        pass
