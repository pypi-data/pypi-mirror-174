"""Implementation of replay buffers for learning algorithms.

These store a history of transitions, which allows learning algorithms to learn from past experience (rather than just the previous timestep). These are necessary for off-policy learning. The buffers are built upon Python's deque data structure, which is of fixed-length in our case. More information can be found here: https://docs.python.org/3/library/collections.html#collections.deque

Author: WillDudley
"""
from __future__ import annotations
import collections
import pickle
import random

import torch
from gymnasium.spaces import Box, Discrete
from .space_tests import space_tests


class ReplayBuffer:
    def __init__(self, buffer_size: int, action_space: Box | Discrete, observation_space: Box | Discrete):
        self.buffer = collections.deque(maxlen=buffer_size)
        self.action_space = action_space
        self.observation_space = observation_space
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


    def append(self, observation: torch.Tensor, action: torch.Tensor, reward: torch.Tensor,
               next_observation: torch.Tensor, termination: torch.Tensor, truncation: torch.Tensor):
        """
        Add a new transition to the buffer.
        """
        # space_tests(self.action_space, action)
        # space_tests(self.observation_space, observation, next_observation)

        self.buffer.append((observation, action, reward, next_observation, termination, truncation))


    def transpose(self, feature: str | tuple[str] = ("observation", "action", "reward", "next_observation", "termination", "truncation")):
        feature_map = {
            "observation": 0,
            "action": 1,
            "reward": 2,
            "next_observation": 3,
            "termination": 4,
            "truncation": 5
        }

        if type(feature) == str:
            feature = feature_map[feature]
            return torch.cat([torch.stack([transition[feature_map[feature]] for transition in self.buffer], dim=0)])
        elif type(feature) == tuple:
            features = [feature_map[f] for f in feature]
            return (torch.cat([torch.stack([transition[f] for transition in self.buffer], dim=0)]) for f in features)
        else:
            raise TypeError(f"feature must be a string or tuple of strings, not {type(feature)}")


    def sample_batch(self, batch_size: int):
        if batch_size > len(self.buffer):
            raise ValueError(f"Batch size of {batch_size} is greater than buffer size of {len(self.buffer)}.")

        batch = random.sample(self.buffer, batch_size)
        return (torch.cat([d[i] for d in batch], dim=0) for i in range(6))

    def save(self, path):
        if path[-7:] != ".pickle":
            raise SyntaxError(
                f'Please save the file with a ".pickle" extension. \n'
                f"Given path: {path}"
            )
        pickle.dump(self.buffer, open(path, "wb"))

    def load(self, path):
        if path[-7:] != ".pickle":
            raise SyntaxError(
                f'The file you are loading does not have a ".pickle" extension - are you sure this is the correct path? \n'
                f"Given path: {path}"
            )
        self.buffer = pickle.load(open(path, "rb"))

    def __str__(self):
        return f"ReplayBuffer object with {len(self.buffer)} previous OAROTT steps."

    def __len__(self):
        return len(self.buffer)

    def __getitem__(self, item):
        return self.buffer[item]

    def __setitem__(self):
        raise NotImplementedError("Overwriting elements is not supported for ReplayBuffer objects.")

    def __delitem__(self):
        raise NotImplementedError("Deleting elements is not supported for ReplayBuffer objects.")

    def __iter__(self):
        return self.buffer.__iter__()

    def __reversed__(self):
        return self.buffer.__reversed__()

    def __contains__(self, item):
        return self.buffer.__contains__(item)
