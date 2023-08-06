"""Assorted utility functions"""

from __future__ import annotations

import json
import random
import re
import string
from typing import Any


def random_string(
    length: int = 6,
    characters: str = string.ascii_uppercase,
) -> str:
    """
    Generates a random string of the specified length using the specified character set.

    Parameters
    ----------
    length
        The desired length.
    characters
        The character set.

    Returns
    -------
    result : str
        A random string.

    Examples
    --------
    >>> random_string(length=1,  characters='a')
    'a'
    """
    return "".join(random.choices(characters, k=length))


def split_prefix_and_number(
    text: str,
) -> tuple[str, int]:
    """
    Split a string into alpha prefix and numeric suffix.

    Parameters
    ----------
    text : str
        The text to split

    Returns
    -------
    prefix, number : tuple[str, int]
        The prefix and the number

    Examples
    --------
    >>> split_prefix_and_number('U1500000')
    ('U', 1500000)
    """
    search_results = re.search(r"([a-zA-Z])(\d+)", text)

    if search_results is None:
        raise ValueError("Invalid input")

    prefix, number = search_results.groups()

    return prefix, int(number)


class CustomEncoder(json.JSONEncoder):
    """A custom JSON encoder that attempts to convert all user defined classes to string."""

    def default(
        self,
        o: Any,
    ) -> Any:
        """
        Serialize an object.
        If the object is not a builtin, return the __str__ of the object.
        For builtins, use the standard serializer.

        Parameters
        ----------
        o : Any
            Object to serialize

        Returns
        -------
        serialized_object : Any
            Serialized object
        """
        if type(o) not in [dict, list, tuple, str, int, float, bool, None]:
            return str(o)
        return json.JSONEncoder.default(self, o)


def find_nth(
    haystack: str,
    needle: str,
    nth: int,
) -> int:
    """
    Find the nth occurrence of a substring in a string.

    Parameters
    ----------
    haystack
        The string to search in
    needle
        The substring to search for
    nth
        Which nth occurrence to find

    Returns
    -------
    The index of the nth occurrence of the substring, or -1 if not found.

    Examples
    --------
    >>> find_nth("yankee doodle", "o", 2)
    9
    """
    start = haystack.find(needle)
    while start >= 0 and nth > 1:
        start = haystack.find(needle, start + len(needle))
        nth -= 1
    return start


def bulk_substring_remove(
    text: str,
    substrings: list[str],
):
    """
    Remove all substrings from a string.

    Parameters
    ----------
    text
        The string to update
    substrings
        The substrings to remove

    Returns
    -------
    The original string with all substrings removed

    Examples
    --------
    >>> bulk_substring_remove("yankee doodle", ["yan", "dle"])
    'kee doo'
    """
    for substring in substrings:
        text = text.replace(substring, "")
    return text
