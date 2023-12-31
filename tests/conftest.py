import json
from unittest.mock import mock_open, patch

import pytest

from dfllama.client import DefiLlamaClient


@pytest.fixture
def mock_get_retry_session():
    with patch("dfllama.utils.get_retry_session") as _mock_get_retry_session:
        yield _mock_get_retry_session


@pytest.fixture
def mock_coins_file(monkeypatch):
    coins_data = {"coins": ["bitcoin", "ethereum"]}
    mock_file = mock_open(read_data=json.dumps(coins_data))
    monkeypatch.setattr("builtins.open", mock_file)


@pytest.fixture
def dlclient():
    return DefiLlamaClient()


@pytest.fixture
def mock_get():
    with patch("dfllama.client.DefiLlamaClient._get") as mock:
        yield mock


@pytest.fixture
def mock_protocols():
    with patch("dfllama.client.DefiLlamaClient._protocols", ["protocol1", "protocol2"]):
        yield


@pytest.fixture
def mock_chains():
    with patch("dfllama.client.DefiLlamaClient._chains", ["chain1", "chain2"]):
        yield


@pytest.fixture
def mock_bridges():
    with patch("dfllama.client.DefiLlamaClient._bridges", {1: "bridge1", 2: "bridge2"}):
        yield


@pytest.fixture
def mock_stablecoins():
    with patch(
        "dfllama.client.DefiLlamaClient._stablecoins",
        {1: "stablecoin1", 2: "stablecoin2"},
    ):
        yield


@pytest.fixture
def mock_pools():
    with patch(
        "dfllama.client.DefiLlamaClient._pools",
        {"pool1": "symbol1", "pool2": "symbol2"},
    ):
        yield


@pytest.fixture
def mock_dex_chains():
    with patch(
        "dfllama.client.DefiLlamaClient._dex_chains", ["dex_chain1", "dex_chain2"]
    ):
        yield


@pytest.fixture
def mock_dex_protocols():
    with patch(
        "dfllama.client.DefiLlamaClient._dex_protocols",
        ["dex_protocol1", "dex_protocol2"],
    ):
        yield


@pytest.fixture
def mock_options_protocols():
    with patch(
        "dfllama.client.DefiLlamaClient._dex_options_protocols",
        ["options_protocol1", "options_protocol2"],
    ):
        yield


@pytest.fixture
def mock_options_chains():
    with patch(
        "dfllama.client.DefiLlamaClient._dex_options_chains",
        ["options_chain1", "options_chain2"],
    ):
        yield


@pytest.fixture
def mock_fees_protocols():
    with patch(
        "dfllama.client.DefiLlamaClient._fees_protocols",
        ["fees_protocol1", "fees_protocol2"],
    ):
        yield


@pytest.fixture
def mock_fees_chains():
    with patch(
        "dfllama.client.DefiLlamaClient._fees_chains", ["fees_chain1", "fees_chain2"]
    ):
        yield


@pytest.fixture
def mock_get_bridge_id(mocker):
    return mocker.patch("dfllama.client.get_bridge_id")


@pytest.fixture
def mock_validate_searched_entity():
    with patch("dfllama.client.validate_searched_entity") as mock:
        yield mock
