from enum import Enum

__all__ = ["Mix"]


class Mix(Enum):
    """Mixture types."""

    Mass = "Mass-based mixture"
    Volume = "Volume-based mixture"

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name
