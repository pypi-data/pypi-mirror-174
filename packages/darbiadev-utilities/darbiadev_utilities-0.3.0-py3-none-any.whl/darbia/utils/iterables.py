"""Assorted utility functions"""

from __future__ import annotations

from typing import Any, Generator, Iterable


# https://stackoverflow.com/a/24290026/8160821
def enumerate2(
    iterable: Iterable[Any],
    start: int = 0,
    step: int = 1,
) -> Generator[tuple[int, Any], Any, None]:
    """
    Yield items from a list with a custom index.

    Yields
    ------
    item, index : tuple[Any, int]
        The next item and the next number per step
    """
    for item in iterable:
        yield start, item
        start += step


# https://stackoverflow.com/a/312464/8160821
def chunks(
    lst: list[Any],
    size: int,
) -> Generator[list, Any, None]:
    """
    Yield successive n-sized chunks from lst.

    Yields
    ------
    chunk : list
        An n-sized chunk of the list
    """
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


# https://stackoverflow.com/a/952952
def flatten(
    lst: list[list[Any]],
) -> list[Any]:
    """
    Flattens a list of lists into a single list.

    Parameters
    ----------
    lst : list[list[Any]]
        The nested lists to flatten.

    Returns
    -------
    flattend_list : list[Any]
        The flattened list.

    Examples
    --------
    >>> flatten(lst=[['a'],['b']])
    ['a', 'b']
    """
    return [item for sublist in lst for item in sublist]
