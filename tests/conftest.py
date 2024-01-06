import json
from unittest.mock import mock_open, patch
import pytest


@pytest.fixture
def mock_get_retry_session():
    with patch("defillama.utils.get_retry_session") as _mock_get_retry_session:
        yield _mock_get_retry_session


@pytest.fixture
def mock_coins_file(monkeypatch):
    coins_data = {"coins": ["bitcoin", "ethereum"]}
    mock_file = mock_open(read_data=json.dumps(coins_data))
    monkeypatch.setattr("builtins.open", mock_file)
