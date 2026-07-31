"""
Result mappers.
"""

from .duplicate_update_mapper import DuplicateUpdateMapper
from .orphan_update_mapper import OrphanUpdateMapper

__all__ = [
    "DuplicateUpdateMapper",
    "OrphanUpdateMapper",
]