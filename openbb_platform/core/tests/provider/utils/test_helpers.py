"""Test the provider helpers."""

import os
from datetime import date, datetime, timedelta
from types import SimpleNamespace

import pytest
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.utils import helpers
from openbb_core.provider.utils.client import ClientSession
from openbb_core.provider.utils.helpers import (
    amake_request,
    amake_requests,
    combine_certificates,
    filter_by_dates,
    get_querystring,
    get_requests_session,
    make_request,
    maybe_coroutine,
    run_async,
    safe_fromtimestamp,
    to_snake_case,
)

# pylint: disable=unused-argument


class MockResponse:
    """Mock the response."""

    def __init__(self):
        """Initialize the mock response."""
        self.status_code = 200
        self.status = 200

    async def json(self):
        """Return the json response."""
        return {"test": "test"}


class MockSession:
    """Mock the ClientSession."""

    def __init__(self):
        """Initialize the mock session."""
        self.response = MockResponse()

    async def request(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Mock the ClientSession.request method."""
        if kwargs.get("raise_for_status", False):
            raise Exception("Test")

        return self.response

    @staticmethod
    async def mock_callback(response, session):
        """Mock the response_callback."""
        assert response.status == 200
        return await response.json()


def test_get_querystring_exclude():
    """Test the get_querystring helper."""
    items = {
        "key1": "value1",
        "key2": "value2",
        "key3": None,
        "key4": ["value3", "value4"],
    }
    exclude = ["key2"]

    querystring = get_querystring(items, exclude)
    assert querystring == "key1=value1&key4=value3&key4=value4"


def test_get_querystring_no_exclude():
    """Test the get_querystring helper with no exclude list."""
    items = {
        "key1": "value1",
        "key2": "value2",
        "key3": None,
        "key4": ["value3", "value4"],
    }

    querystring = get_querystring(items, [])
    assert querystring == "key1=value1&key2=value2&key4=value3&key4=value4"


def test_make_request(monkeypatch):
    """Test the make_request helper."""

    def mock_get(*args, **kwargs):
        """Mock the requests.get method."""
        return MockResponse()

    client_session = get_requests_session()
    monkeypatch.setattr(client_session, "get", mock_get)

    response = make_request("http://mock.url", session=client_session)
    assert response.status_code == 200

    with pytest.raises(ValueError):
        make_request("http://mock.url", method="PUT")


def test_to_snake_case():
    """Test the to_snake_case helper."""
    assert to_snake_case("SomeRandomString") == "some_random_string"
    assert to_snake_case("someRandomString") == "some_random_string"
    assert to_snake_case("already_snake_case") == "already_snake_case"


@pytest.mark.asyncio
async def test_amake_request(monkeypatch):
    """Test the amake_request helper."""

    mock_callback = MockSession.mock_callback

    client_session = MockSession()
    monkeypatch.setattr(ClientSession, "request", client_session.request)

    response = await amake_request("http://mock.url", response_callback=mock_callback)
    assert response == {"test": "test"}

    with pytest.raises(Exception):
        await amake_request(
            "http://mock.url",
            response_callback=mock_callback,
            raise_for_status=True,
        )

    with pytest.raises(ValueError):
        await amake_request("http://mock.url", method="PUT")  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_amake_requests(monkeypatch):
    """Test the amake_requests helper."""

    mock_callback = MockSession.mock_callback

    client_session = MockSession()
    monkeypatch.setattr(ClientSession, "request", client_session.request)

    multi_response = await amake_requests(
        ["http://mock.url", "http://mock.url"],
        response_callback=mock_callback,
    )
    assert multi_response == [{"test": "test"}, {"test": "test"}]

    with pytest.raises(ValueError):
        await amake_requests(
            ["http://mock.url", "http://mock.url"], method="PUT", raise_for_status=True
        )


def test_combine_certificates(tmp_path):
    """Test combine_certificates creates a file."""
    cert_file = tmp_path / "cert.pem"
    bundle_file = tmp_path / "bundle.pem"
    cert_content = "-----BEGIN CERTIFICATE-----\nMIID...\n-----END CERTIFICATE-----\n"
    bundle_content = "-----BEGIN CERTIFICATE-----\nMIIC...\n-----END CERTIFICATE-----\n"
    cert_file.write_text(cert_content)
    bundle_file.write_text(bundle_content)

    combined = combine_certificates(str(cert_file), str(bundle_file))
    assert os.path.isfile(combined)


def test_safe_fromtimestamp(monkeypatch):
    """Test safe_fromtimestamp handles negatives on Windows."""
    monkeypatch.setattr(helpers, "os", SimpleNamespace(name="nt"))
    result = safe_fromtimestamp(-1)
    assert result == datetime(1970, 1, 1) + timedelta(seconds=-1)


def test_filter_by_dates():
    """Test filter_by_dates filters correctly."""
    class MockData(Data):
        date: datetime

    data = [
        MockData(date=datetime(2024, 1, 1)),
        MockData(date=datetime(2024, 1, 3)),
        MockData(date=datetime(2024, 1, 5)),
    ]

    filtered = filter_by_dates(
        data, start_date=date(2024, 1, 2), end_date=date(2024, 1, 4)
    )
    assert len(filtered) == 1
    assert filtered[0].date.date() == date(2024, 1, 3)


def test_maybe_coroutine_and_run_async():
    """Test maybe_coroutine and run_async wrappers."""

    async def coro(a):
        return a + 1

    def reg(a):
        return a + 2

    assert run_async(coro, 1) == 2
    assert run_async(reg, 1) == 3
    assert run_async(lambda x: x, 5) == 5
    assert run_async(coro, 3) == 4

    assert run_async(lambda x: x * 2, 2) == 4

    async def get_three():
        return 3

    assert run_async(get_three) == 3

    assert run_async(lambda: 5) == 5


@pytest.mark.asyncio
async def test_maybe_coroutine():
    """Test maybe_coroutine helper."""

    async def coro(v):
        return v * 2

    def reg(v):
        return v + 1

    assert await maybe_coroutine(coro, 2) == 4
    assert await maybe_coroutine(reg, 2) == 3

