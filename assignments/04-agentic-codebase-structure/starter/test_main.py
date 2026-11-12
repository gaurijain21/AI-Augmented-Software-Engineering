import main
import pytest
from fastapi import HTTPException
from fastapi.responses import RedirectResponse


@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "links.db")
    main.init_db()


def test_shorten_and_redirect():
    result = main.shorten(main.ShortenRequest(url="https://example.com"))
    code = result["code"]
    assert code
    redirect = main.redirect(code)
    assert isinstance(redirect, RedirectResponse)
    assert redirect.status_code == 307
    assert redirect.headers["location"] == "https://example.com"


def test_rejects_bad_url():
    with pytest.raises(HTTPException) as error:
        main.shorten(main.ShortenRequest(url="ftp://nope"))
    assert error.value.status_code == 400


def test_unknown_code_404():
    with pytest.raises(HTTPException) as error:
        main.redirect("does-not-exist")
    assert error.value.status_code == 404
