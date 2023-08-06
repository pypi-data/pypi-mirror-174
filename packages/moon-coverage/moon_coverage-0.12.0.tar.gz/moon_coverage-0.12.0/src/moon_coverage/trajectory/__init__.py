"""Trajectory module."""

from .config import TourConfig, TrajectoryConfig
from .fovs import debug_fovs
from .trajectory import (
    Flyby, InstrumentFlyby, InstrumentTrajectory, SpacecraftFlyby,
    SpacecraftTrajectory, Trajectory, debug_trajectory
)


__all__ = [
    'Flyby',
    'SpacecraftFlyby',
    'InstrumentFlyby',
    'Trajectory',
    'SpacecraftTrajectory',
    'InstrumentTrajectory',
    'TourConfig',
    'debug_trajectory',
    'debug_fovs',
    'TrajectoryConfig',  # Depreciated
]
