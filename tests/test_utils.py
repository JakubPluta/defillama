import datetime
from typing import Dict, Union
from unittest import mock

import requests
import defillama
import pytest

from requests.exceptions import HTTPError
from defillama.utils import (
    convert_from_timestamp,
    convert_to_timestamp,
    get_previous_timestamp,
    get_retry_session,
    get_stablecoin_id,
    prepare_coins_for_request,
)
from defillama.utils import get_coingecko_coin_ids
from defillama.utils import read_coingecko_ids_from_file
from defillama.utils import _prepare_token
from defillama.dtypes import Coin
from defillama.utils import get_bridge_id


@pytest.mark.parametrize(
    "input, expected",
    [
        (datetime.date(2022, 1, 1), int(datetime.datetime(2022, 1, 1).timestamp())),
        (
            datetime.datetime(2022, 1, 1, 12, 0, 0),
            int(datetime.datetime(2022, 1, 1, 12, 0, 0).timestamp()),
        ),
        ("2022-01-01", int(datetime.datetime(2022, 1, 1).timestamp())),
        ("01-01-2022", 1640991600),
        (1641024000, 1641024000),
        (True, TypeError),
    ],
)
def test_convert_to_timestamp(input, expected):
    if expected in (TypeError, ValueError, Exception):
        with pytest.raises(expected):
            convert_to_timestamp(input)
    else:
        assert convert_to_timestamp(input) == expected


def test_should_create_retry_session():
    max_retries = 6
    session = get_retry_session(retries=max_retries)
    for adapter in session.adapters.values():
        assert adapter.max_retries.total == max_retries
        assert isinstance(adapter, requests.adapters.HTTPAdapter)


def test_successful_request(mock_get_retry_session):
    mock_session = mock_get_retry_session.return_value
    mock_session.get.return_value.json.return_value = [
        {"id": "bitcoin"},
        {"id": "ethereum"},
        {"id": "litecoin"},
    ]

    result = get_coingecko_coin_ids()

    assert result == ["bitcoin", "ethereum", "litecoin"]
    mock_get_retry_session.assert_called_once()
    mock_session.get.assert_called_once_with(
        "https://api.coingecko.com/api/v3/coins/list"
    )
    mock_session.get.return_value.raise_for_status.assert_called_once()


def test_failed_request(mock_get_retry_session):
    mock_session = mock_get_retry_session.return_value
    mock_session.get.return_value.raise_for_status.side_effect = HTTPError("Error")

    with pytest.raises(HTTPError):
        get_coingecko_coin_ids()

    mock_get_retry_session.assert_called_once()
    mock_session.get.assert_called_once_with(
        "https://api.coingecko.com/api/v3/coins/list"
    )
    mock_session.get.return_value.raise_for_status.assert_called_once()


def test_read_coingecko_ids_from_file(mock_coins_file):
    expected_coingecko_ids = ["bitcoin", "ethereum"]
    actual_coingecko_ids = read_coingecko_ids_from_file()
    assert actual_coingecko_ids == expected_coingecko_ids


@pytest.mark.parametrize(
    "token, expected_result",
    [
        (Coin(chain="ETH", address="0x123456789"), "ETH:0x123456789"),
        ({"chain": "ETH", "address": "0x123456789"}, "ETH:0x123456789"),
        ("ETH:0x123456789", "ETH:0x123456789"),
    ],
)
def test_prepare_token(token, expected_result):
    result = _prepare_token(token)
    assert result == expected_result


@pytest.mark.parametrize(
    "coins, expected_result",
    [
        (
            "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
            "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
        ),
        (
            [
                {
                    "chain": "ethereum",
                    "address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
                },
                {
                    "chain": "ethereum",
                    "address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
                },
            ],
            "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
        ),
        (
            [
                Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"),
                Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"),
            ],
            "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
        ),
        (
            Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"),
            "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
        ),
        (
            {
                "chain": "ethereum",
                "address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
            },
            "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
        ),
    ],
)
def test_prepare_coins_for_request(coins, expected_result):
    assert prepare_coins_for_request(coins) == expected_result


@mock.patch(f"{defillama.utils.__name__}.datetime", wraps=datetime)
def test_get_previous_timestamp(mock_datetime):
    mock_datetime.datetime.now.return_value = datetime.datetime(2022, 12, 31)
    assert get_previous_timestamp(90) == 1664665200
    assert get_previous_timestamp(30) == 1669849200
    assert get_previous_timestamp(0) == 1672441200


@pytest.fixture
def stablecoins():
    return {1: "USDT", 2: "USDC", 3: "DAI"}


@pytest.mark.parametrize(
    "stablecoin, expected_id",
    [
        ("USDT", 1),
        (2, 2),
        ("invalid", None),
        (4, None),
    ],
)
def test_get_stablecoin_id(stablecoin, expected_id, stablecoins):
    if expected_id is None:
        with pytest.raises(ValueError):
            get_stablecoin_id(stablecoin, stablecoins)
    else:
        stablecoin_id = get_stablecoin_id(stablecoin, stablecoins)
        assert stablecoin_id == expected_id


def test_get_stablecoin_id_empty_dict():
    with pytest.raises(ValueError):
        get_stablecoin_id("USDT", {})


@pytest.mark.parametrize(
    "bridge, bridges, expected",
    [
        ("Bridge 1", {1: "Bridge 1", "2": "Bridge 2"}, 1),
        (2, {1: "Bridge 1", 2: "Bridge 2"}, 2),
    ],
)
def test_get_bridge_id_with_valid_input(
    bridge: Union[str, int], bridges: Dict[str, str], expected: int
):
    bridge_id = get_bridge_id(bridge, bridges)
    assert bridge_id == expected


@pytest.mark.parametrize(
    "bridge, bridges",
    [
        ("Invalid Bridge", {1: "Bridge 1", 2: "Bridge 2"}),
    ],
)
def test_get_bridge_id_with_invalid_input(
    bridge: Union[str, int], bridges: Dict[str, str]
):
    with pytest.raises(ValueError) as exc_info:
        get_bridge_id(bridge, bridges)
    assert (
        str(exc_info.value) == f"Invalid bridge: {bridge}. Available bridges: {bridges}"
    )


@pytest.mark.parametrize(
    "timestamp, as_str, fmt, expected",
    [
        (
            1609459200,
            False,
            "%Y-%m-%d %H:%M:%S",
            datetime.datetime(2021, 1, 1, 1, 0, 0),
        ),
        (1609459200, True, "%Y-%m-%d %H:%M:%S", "2021-01-01 01:00:00"),
        (1609459200, False, "%Y-%m-%d", datetime.datetime(2021, 1, 1, 1)),
        (1609459200, True, "%Y-%m-%d", "2021-01-01"),
    ],
)
def test_convert_from_timestamp(timestamp, as_str, fmt, expected):
    result = convert_from_timestamp(timestamp, as_str=as_str, fmt=fmt)
    assert result == expected
