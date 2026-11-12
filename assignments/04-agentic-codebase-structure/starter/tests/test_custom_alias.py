import main
import pytest
from fastapi import HTTPException
from fastapi.responses import RedirectResponse


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "links.db")
    main.init_db()
    return main


def test_custom_alias_is_used_and_redirects(client):
    response = client.shorten(
        client.ShortenRequest(url="https://example.com/docs", alias="docs")
    )

    assert response == {"code": "docs", "short_url": "/docs"}

    redirect = client.redirect("docs")
    assert isinstance(redirect, RedirectResponse)
    assert redirect.status_code == 307
    assert redirect.headers["location"] == "https://example.com/docs"


def test_duplicate_custom_alias_returns_conflict(client):
    first = client.shorten(
        client.ShortenRequest(url="https://example.com/first", alias="same-link")
    )
    with pytest.raises(HTTPException) as error:
        client.shorten(
            client.ShortenRequest(url="https://example.com/second", alias="same-link")
        )

    assert first["code"] == "same-link"
    assert error.value.status_code == 409
    assert error.value.detail == "alias already in use"
