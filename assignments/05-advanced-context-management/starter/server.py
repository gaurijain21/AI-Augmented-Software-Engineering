"""Data Explorer MCP server for Week 5.

The server exposes a small, model-friendly view of the open countries dataset
over MCP's STDIO transport.  Network and input failures are returned as
structured tool results so a client can recover without the server crashing.
"""

from __future__ import annotations

from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

DATA_URL = "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"
FLAG_URL = "https://raw.githubusercontent.com/mledoze/countries/master/data/{cca3}.svg"
MAX_SEARCH_LIMIT = 20

mcp = FastMCP("data-explorer")

_countries: list[dict[str, Any]] | None = None


def load_countries() -> list[dict[str, Any]]:
    """Download and cache the dataset, preserving real HTTP failure modes."""
    global _countries
    if _countries is None:
        response = httpx.get(DATA_URL, timeout=30, follow_redirects=True)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list):
            raise ValueError("country dataset must be a JSON list")
        _countries = payload
    return _countries


def _load_error(exc: Exception) -> dict[str, str]:
    if isinstance(exc, httpx.TimeoutException):
        return {"error": "upstream request timed out"}
    if isinstance(exc, httpx.HTTPStatusError):
        return {"error": f"upstream request failed with HTTP {exc.response.status_code}"}
    if isinstance(exc, httpx.HTTPError):
        return {"error": f"upstream request failed: {exc}"}
    return {"error": f"upstream response was invalid: {exc}"}


def _find_country(name: str, countries: list[dict[str, Any]]) -> dict[str, Any] | None:
    query = name.strip().casefold()
    for country in countries:
        country_name = country.get("name") or {}
        common = str(country_name.get("common", "")).casefold()
        official = str(country_name.get("official", "")).casefold()
        if query == common or query == official:
            return country
    return None


@mcp.tool()
def search_countries(query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Search by common or official name.

    Results contain only name, capital, region, and subregion.  No matches are
    represented by an empty list; input and upstream failures use an error item.
    """
    if not isinstance(query, str) or not query.strip():
        return [{"error": "query must be a non-empty string"}]
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= MAX_SEARCH_LIMIT:
        return [{"error": f"limit must be an integer from 1 to {MAX_SEARCH_LIMIT}"}]

    try:
        countries = load_countries()
    except (httpx.HTTPError, ValueError, TypeError) as exc:
        return [_load_error(exc)]

    q = query.strip().casefold()
    matches = []
    for country in countries:
        country_name = country.get("name") or {}
        common = str(country_name.get("common", ""))
        official = str(country_name.get("official", ""))
        if q in common.casefold() or q in official.casefold():
            matches.append(
                {
                    "name": common,
                    "capital": (country.get("capital") or [None])[0],
                    "region": country.get("region"),
                    "subregion": country.get("subregion"),
                }
            )
    return matches[:limit]


@mcp.tool()
def get_country_details(name: str) -> dict[str, Any]:
    """Return currencies, languages, borders, and flag URL for one country."""
    if not isinstance(name, str) or not name.strip():
        return {"error": "name must be a non-empty string"}

    try:
        countries = load_countries()
    except (httpx.HTTPError, ValueError, TypeError) as exc:
        return _load_error(exc)

    country = _find_country(name, countries)
    if country is None:
        return {"error": f"country not found: {name.strip()}"}

    country_name = country.get("name") or {}
    cca3 = country.get("cca3")
    if not cca3:
        return {"error": f"country record is missing a cca3 code: {name.strip()}"}

    return {
        "name": country_name.get("common"),
        "currencies": country.get("currencies") or {},
        "languages": country.get("languages") or {},
        "borders": country.get("borders") or [],
        "flag_url": FLAG_URL.format(cca3=cca3),
    }


if __name__ == "__main__":
    mcp.run()
