"""SOAP response extraction utilities.

Purpose
-------
Provide reusable utilities for extracting data from SOAP response objects.

System Role
-----------
Domain layer - pure utility functions with no I/O dependencies.
"""

from __future__ import annotations

from typing import Any, cast


def extract_string_attr(response: Any, attr_name: str, default: str = "") -> str:
    """Extract a string attribute from a SOAP response object.

    Safely extracts an attribute from a SOAP response, handling:
    - Missing attributes (returns default)
    - None values (returns default)
    - Non-string values (casts to string)

    Args:
        response: SOAP response object with named attributes.
        attr_name: Attribute name to extract (e.g., 'adrz1', 'name').
        default: Default value if attribute is missing or None.

    Returns:
        Extracted string value, or default if not present.

    Examples:
        >>> class FakeResponse:
        ...     adrz1 = "Line 1"
        ...     adrz2 = None
        >>> r = FakeResponse()
        >>> extract_string_attr(r, "adrz1")
        'Line 1'
        >>> extract_string_attr(r, "adrz2")
        ''
        >>> extract_string_attr(r, "adrz3")
        ''
        >>> extract_string_attr(r, "adrz3", "N/A")
        'N/A'
    """
    value = getattr(response, attr_name, None)
    if value is None:
        return default
    return str(cast(str, value) or default)
