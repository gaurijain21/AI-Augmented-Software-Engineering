import httpx
import pytest

import server


GERMANY = {
    "name": {"common": "Germany", "official": "Federal Republic of Germany"},
    "capital": ["Berlin"],
    "region": "Europe",
    "subregion": "Western Europe",
    "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
    "languages": {"deu": "German"},
    "borders": ["AUT", "BEL", "CZE", "DNK", "FRA", "LUX", "NLD", "POL", "CHE"],
    "cca3": "DEU",
}


@pytest.fixture(autouse=True)
def fake_dataset(monkeypatch):
    monkeypatch.setattr(server, "_countries", [GERMANY])


def test_search_returns_model_friendly_result():
    assert server.search_countries("eRM", limit=1) == [
        {
            "name": "Germany",
            "capital": "Berlin",
            "region": "Europe",
            "subregion": "Western Europe",
        }
    ]


def test_search_validates_empty_query_and_limit():
    assert server.search_countries(" ") == [{"error": "query must be a non-empty string"}]
    assert server.search_countries("Germany", limit=0) == [
        {"error": "limit must be an integer from 1 to 20"}
    ]


def test_details_returns_currencies_languages_borders_and_flag():
    result = server.get_country_details("germany")
    assert result["name"] == "Germany"
    assert result["currencies"]["EUR"]["symbol"] == "€"
    assert result["languages"] == {"deu": "German"}
    assert "FRA" in result["borders"]
    assert result["flag_url"].endswith("/DEU.svg")


def test_details_handles_empty_and_unknown_names():
    assert server.get_country_details("") == {"error": "name must be a non-empty string"}
    assert server.get_country_details("Atlantis") == {"error": "country not found: Atlantis"}


@pytest.mark.parametrize("failure", [httpx.ReadTimeout("slow"), httpx.HTTPStatusError("503", request=httpx.Request("GET", server.DATA_URL), response=httpx.Response(503))])
def test_both_tools_return_structured_upstream_errors(monkeypatch, failure):
    monkeypatch.setattr(server, "_countries", None)
    monkeypatch.setattr(server.httpx, "get", lambda *args, **kwargs: (_ for _ in ()).throw(failure))

    search_result = server.search_countries("Germany")
    details_result = server.get_country_details("Germany")

    assert search_result[0]["error"].startswith("upstream request")
    assert details_result["error"].startswith("upstream request")
