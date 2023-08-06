from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List

from matplotlib.colors import LinearSegmentedColormap


class ColumnType(Enum):
    """The Column Type.

    Column Types are:
        STRING = "string"
        SUBPLOT = "subplot"
    """

    STRING = "string"
    SUBPLOT = "subplot"


def _filter_none_values(d: Dict[str, Any]) -> Dict[str, Any]:
    """Filters out keys with None values from a dictionary.

    Args:
        d (Dict[str, Any]): Dictionary

    Returns:
        Dict[str, Any]: Dictionary without None valued values.
    """
    return {k: v for k, v in d.items() if v is not None}


@dataclass
class ColumnDefinition:
    """A Class defining attributes for a table column.

    Args:
        name: str:
            the column name
        title: str = None:
            the plotted title to override the column name
        width: float = 1:
            the width of the column as a factor of the default width
        textprops: Dict[str, Any] = field(default_factory=dict)
            textprops provided to each textcell
        formatter: Callable = None:
            A Callable to format the appearance of the texts
        cmap: Callable | LinearSegmentedColormap = None:
            A Callable that returns a color based on the cells value.
        text_cmap: Callable | LinearSegmentedColormap = None:
            A Callable that returns a color based on the cells value.
        group: str = None:
            Each group will get a spanner column label above the column labels.
        plot_fn: Callable = None
            A Callable that will take the cells value as input and create a subplot
            on top of each cell and plot onto them.
            To pass additional arguments to it, use plot_kw (see below).
        plot_kw: Dict[str, Any] = field(default_factory=dict)
            Additional keywords provided to plot_fn.
        border: str | List = None:
            Plots a vertical borderline.
            can be either "left" / "l", "right" / "r" or "both"
    """

    name: str
    title: str = None
    width: float = 1
    textprops: Dict[str, Any] = field(default_factory=dict)
    formatter: Callable = None
    cmap: Callable | LinearSegmentedColormap = None
    text_cmap: Callable | LinearSegmentedColormap = None
    group: str = None
    plot_fn: Callable = None
    plot_kw: Dict[str, Any] = field(default_factory=dict)
    border: str | List = None

    def _asdict(self) -> Dict[str, Any]:
        """Returns the attributes as a dictionary.

        Returns:
            Dict[str, Any]: Dictionary of Column Attributes.
        """
        return asdict(self)

    def _as_non_none_dict(self) -> Dict[str, Any]:
        """Returns the attributes as a dictionary, filtering out
        keys with None values.

        Returns:
            Dict[str, Any]: Dictionary of Column Attributes.
        """
        return _filter_none_values(asdict(self))


# abbreviated name to reduce writing
ColDef = ColumnDefinition
