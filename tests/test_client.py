from unittest.mock import MagicMock, patch

import pytest
import requests
from requests import Response

from dfllama.client import ApiSectionsEnum, DefiLlamaClient
from dfllama.exc import InvalidResponseDataException


@pytest.mark.parametrize(
    "api_section, expected_url",
    [
        (ApiSectionsEnum.TVL, "https://api.llama.fi"),
        (ApiSectionsEnum.COINS, "https://coins.llama.fi"),
        (ApiSectionsEnum.STABLECOINS, "https://stablecoins.llama.fi"),
        (ApiSectionsEnum.YIELDS, "https://yields.llama.fi"),
        (ApiSectionsEnum.BRIDGES, "https://bridges.llama.fi"),
        (ApiSectionsEnum.VOLUMES, "https://api.llama.fi"),
        (ApiSectionsEnum.FEES, "https://api.llama.fi"),
    ],
)
def test_init_set_urls(api_section, expected_url):
    client = DefiLlamaClient()
    assert client._urls[api_section] == expected_url


@pytest.mark.parametrize(
    "section, expected_url",
    [
        (ApiSectionsEnum.TVL, "https://api.llama.fi"),
        (ApiSectionsEnum.COINS, "https://coins.llama.fi"),
        (ApiSectionsEnum.STABLECOINS, "https://stablecoins.llama.fi"),
        (ApiSectionsEnum.YIELDS, "https://yields.llama.fi"),
        (ApiSectionsEnum.BRIDGES, "https://bridges.llama.fi"),
        (ApiSectionsEnum.VOLUMES, "https://api.llama.fi"),
        (ApiSectionsEnum.FEES, "https://api.llama.fi"),
    ],
)
def test_resolve_api_url(dlclient, section, expected_url):
    url = dlclient._resolve_api_url(section)
    assert url == expected_url
    # Add more assertions as needed


def test_cannnot_resolve_invalid_api_url(dlclient):
    with pytest.raises(ValueError):
        dlclient._resolve_api_url("invalid-section")


@pytest.mark.parametrize(
    "section, endpoint, args, expected_url",
    [
        (ApiSectionsEnum.TVL, "endpoint1", (), "https://api.llama.fi/endpoint1"),
        (
            ApiSectionsEnum.COINS,
            "endpoint2",
            (1, 2, 3),
            "https://coins.llama.fi/endpoint2/1/2/3",
        ),
        (
            ApiSectionsEnum.COINS,
            "endpoint3",
            ("ethereum", 1654000),
            "https://coins.llama.fi/endpoint3/ethereum/1654000",
        ),
    ],
)
def test_build_endpoint_url(dlclient, section, endpoint, args, expected_url):
    url = dlclient._build_endpoint_url(section, endpoint, *args)
    assert url == expected_url


def test_session_property(dlclient):
    # Test if the session property returns an instance of requests.Session
    session = dlclient.session
    assert isinstance(session, requests.Session)


def test_session_property_is_same(dlclient):
    session1 = dlclient.session
    session2 = dlclient.session
    assert session1 is session2


def test_handle_response_valid_response(dlclient):
    mock_response = MagicMock(spec=requests.Response)
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"key": "value"}

    result = dlclient._handle_response(mock_response)

    assert result == {"key": "value"}


def test_handle_response_invalid_response_data(dlclient):
    mock_response = MagicMock(spec=requests.Response)
    mock_response.raise_for_status.return_value = 500
    mock_response.raise_for_status.side_effect = requests.HTTPError

    with pytest.raises(requests.HTTPError):
        dlclient._handle_response(mock_response)


def test_handle_response_invalid_json_data(dlclient):
    mock_response = MagicMock(spec=requests.Response)
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = AttributeError

    with pytest.raises(InvalidResponseDataException):
        dlclient._handle_response(mock_response)


def test_get_request(dlclient, monkeypatch):
    section = ApiSectionsEnum.TVL
    endpoint = "some/endpoint"
    query_params = {"param1": "value1", "param2": "value2"}

    # Mock the session object and its get method
    mock_session = MagicMock()
    mock_response = MagicMock(spec=Response)
    mock_session.get.return_value = mock_response

    # Mock the _build_endpoint_url method to return a valid URL
    mock_build_endpoint_url = MagicMock(
        return_value="https://api.example.com/some/endpoint"
    )

    # Patch the session and _build_endpoint_url methods
    monkeypatch.setattr(dlclient, "_session", mock_session)
    monkeypatch.setattr(dlclient, "_build_endpoint_url", mock_build_endpoint_url)

    # Call the _get method with the given parameters
    _ = dlclient._get(section, endpoint, **query_params)

    # Assert that the session's get method was called with the correct arguments
    mock_session.get.assert_called_once_with(
        "https://api.example.com/some/endpoint", params=query_params
    )


@pytest.mark.parametrize(
    "chains, expected_result",
    [
        (
            [{"name": "Chain1"}, {"name": "Chain2"}, {"name": "Chain3"}],
            ["chain1", "chain2", "chain3"],
        ),
        ([], []),
    ],
)
def test_chains(mock_get, chains, expected_result):
    mock_get.return_value = chains
    obj = DefiLlamaClient()
    result = obj._chains
    assert set(result) == set(expected_result) and len(result) == len(expected_result)


@pytest.mark.parametrize(
    "protocols, expected_result",
    [
        (
            [{"slug": "protocol1"}, {"slug": "protocol2"}, {"slug": "protocol3"}],
            ["protocol1", "protocol2", "protocol3"],
        ),
        ([], []),
    ],
)
def test_protocols(mock_get, protocols, expected_result):
    mock_get.return_value = protocols
    obj = DefiLlamaClient()
    result = obj._protocols
    assert set(result) == set(expected_result) and len(result) == len(expected_result)


def test_bridges(mock_get):
    mock_get.return_value = {
        "bridges": [
            {"id": 1, "name": "Bridge 1"},
            {"id": 2, "name": "Bridge 2"},
            {"id": 3, "name": "Bridge 3"},
        ]
    }
    client = DefiLlamaClient()
    bridges = client._bridges
    assert bridges == {1: "Bridge 1", 2: "Bridge 2", 3: "Bridge 3"}


def test_bridges_with_empty_list(mock_get):
    mock_get.return_value = {"bridges": []}
    client = DefiLlamaClient()
    bridges = client._bridges
    assert bridges == {}


def test_bridges_with_invalid_data(mock_get):
    mock_get.return_value = {"bridges": [{"id": "1", "name": "Bridge 1"}]}
    client = DefiLlamaClient()
    with pytest.raises(TypeError):
        client._bridges()


@pytest.mark.parametrize(
    "stables, expected_result",
    [
        (
            {
                "peggedAssets": [
                    {"id": "1", "symbol": "USDT"},
                    {"id": "2", "symbol": "USDC"},
                ]
            },
            {1: "USDT", 2: "USDC"},
        ),
        ({"peggedAssets": []}, {}),
    ],
)
def test_stablecoins(mock_get, stables, expected_result):
    mock_get.return_value = stables
    obj = DefiLlamaClient()
    result = obj._stablecoins
    assert result == expected_result


@pytest.mark.parametrize(
    "pools_data, expected_result",
    [
        (
            {
                "data": [
                    {"pool": "pool_id_1", "symbol": "symbol_1"},
                    {"pool": "pool_id_2", "symbol": "symbol_2"},
                ]
            },
            {"pool_id_1": "symbol_1", "pool_id_2": "symbol_2"},
        ),
        ({"data": []}, {}),
    ],
)
def test_pools(mock_get, pools_data, expected_result):
    mock_get.return_value = pools_data
    client = DefiLlamaClient()
    result = client._pools
    assert result == expected_result


@pytest.mark.parametrize(
    "protocols_data, expected_result",
    [
        (
            {"protocols": [{"name": "protocol_1"}, {"name": "protocol_2"}]},
            ["protocol-1", "protocol-2"],
        ),
        ({"protocols": []}, []),
    ],
)
def test_dex_protocols(mock_get, protocols_data, expected_result):
    mock_get.return_value = protocols_data
    client = DefiLlamaClient()
    result = client._dex_protocols
    assert result == expected_result


@pytest.mark.parametrize(
    "chains_data, expected_result",
    [
        ({"allChains": ["Chain1", "Chain2"]}, ["chain1", "chain2"]),
        ({"allChains": []}, []),
    ],
)
def test_dex_chains(mock_get, chains_data, expected_result):
    mock_get.return_value = chains_data
    client = DefiLlamaClient()
    result = client._dex_chains
    assert result == expected_result


@pytest.mark.parametrize(
    "protocols_data, expected_result",
    [
        (
            {"protocols": [{"name": "protocol_1"}, {"name": "protocol_2"}]},
            ["protocol-1", "protocol-2"],
        ),
        ({"protocols": []}, []),
    ],
)
def test_dex_options_protocols(mock_get, protocols_data, expected_result):
    mock_get.return_value = protocols_data
    client = DefiLlamaClient()
    result = client._dex_options_protocols
    assert result == expected_result


@pytest.mark.parametrize(
    "chains_data, expected_result",
    [
        ({"allChains": ["Chain1", "Chain2"]}, ["chain1", "chain2"]),
        ({"allChains": []}, []),
    ],
)
def test_dex_options_chains(mock_get, chains_data, expected_result):
    mock_get.return_value = chains_data
    client = DefiLlamaClient()
    result = client._dex_options_chains
    assert result == expected_result


@pytest.mark.parametrize(
    "protocols_data, expected_result",
    [
        (
            {"protocols": [{"name": "protocol_1"}, {"name": "protocol_2"}]},
            ["protocol-1", "protocol-2"],
        ),
        ({"protocols": []}, []),
    ],
)
def test_fees_protocols(mock_get, protocols_data, expected_result):
    mock_get.return_value = protocols_data
    client = DefiLlamaClient()
    result = client._fees_protocols
    assert result == expected_result


@pytest.mark.parametrize(
    "chains_data, expected_result",
    [
        ({"allChains": ["Chain1", "Chain2"]}, ["chain1", "chain2"]),
        ({"allChains": []}, []),
    ],
)
def test_fees_chains(mock_get, chains_data, expected_result):
    mock_get.return_value = chains_data
    client = DefiLlamaClient()
    result = client._fees_chains
    assert result == expected_result


def test_list_protocols_slugs(mock_protocols):
    client = DefiLlamaClient()
    result = client.list_protocols()
    assert result == ["protocol1", "protocol2"]


def test_list_chains(mock_chains):
    client = DefiLlamaClient()
    result = client.list_chains()
    assert result == ["chain1", "chain2"]


def test_list_bridges(mock_bridges):
    client = DefiLlamaClient()
    result = client.list_bridges()
    assert result == {1: "bridge1", 2: "bridge2"}


def test_list_stablecoins(mock_stablecoins):
    client = DefiLlamaClient()
    result = client.list_stablecoins()
    assert result == {1: "stablecoin1", 2: "stablecoin2"}


def test_list_pools(mock_pools):
    client = DefiLlamaClient()
    result = client.list_pools()
    assert result == {"pool1": "symbol1", "pool2": "symbol2"}


def test_list_dex_chains(mock_dex_chains):
    client = DefiLlamaClient()
    result = client.list_dex_chains()
    assert result == ["dex_chain1", "dex_chain2"]


def test_list_dex_protocols(mock_dex_protocols):
    client = DefiLlamaClient()
    result = client.list_dex_protocols()
    assert result == ["dex_protocol1", "dex_protocol2"]


def test_list_options_protocols(mock_options_protocols):
    client = DefiLlamaClient()
    result = client.list_options_protocols()
    assert result == ["options_protocol1", "options_protocol2"]


def test_list_options_chains(mock_options_chains):
    client = DefiLlamaClient()
    result = client.list_options_chains()
    assert result == ["options_chain1", "options_chain2"]


def test_list_fees_protocols(mock_fees_protocols):
    client = DefiLlamaClient()
    result = client.list_fees_protocols()
    assert result == ["fees_protocol1", "fees_protocol2"]


def test_list_fees_chains(mock_fees_chains):
    client = DefiLlamaClient()
    result = client.list_fees_chains()
    assert result == ["fees_chain1", "fees_chain2"]


@pytest.mark.parametrize(
    "skip, limit, from_gecko_api, expected_result",
    [
        (
            0,
            10,
            True,
            [
                "coin1",
                "coin2",
                "coin3",
                "coin4",
                "coin5",
                "coin6",
                "coin7",
                "coin8",
                "coin9",
                "coin10",
            ],
        ),
        (5, 3, False, ["coin6", "coin7", "coin8"]),
        (
            0,
            None,
            False,
            [
                "coin1",
                "coin2",
                "coin3",
                "coin4",
                "coin5",
                "coin6",
                "coin7",
                "coin8",
                "coin9",
                "coin10",
            ],
        ),
    ],
)
def test_get_coingecko_coin_ids(skip, limit, from_gecko_api, expected_result):
    with patch("dfllama.client.get_coingecko_coin_ids") as mock_get_coingecko_coin_ids:
        with patch(
            "dfllama.client.read_coingecko_ids_from_file"
        ) as mock_read_coingecko_ids_from_file:
            mock_get_coingecko_coin_ids.return_value = expected_result
            mock_read_coingecko_ids_from_file.return_value = [
                "coin1",
                "coin2",
                "coin3",
                "coin4",
                "coin5",
                "coin6",
                "coin7",
                "coin8",
                "coin9",
                "coin10",
            ]
            client = DefiLlamaClient()
            result = client.get_coingecko_coin_ids(skip, limit, from_gecko_api)

            assert result == expected_result
            if from_gecko_api:
                mock_get_coingecko_coin_ids.assert_called_once()
                mock_read_coingecko_ids_from_file.assert_not_called()
            else:
                mock_get_coingecko_coin_ids.assert_not_called()
                mock_read_coingecko_ids_from_file.assert_called_once()


def test_get_protocols(dlclient):
    expected_result = [
        {
            "id": "2269",
            "name": "Binance CEX",
            "address": None,
            "symbol": "-",
            "chain": "Multi-Chain",
            "gecko_id": None,
            "slug": "binance-cex",
        },
    ]

    with patch("dfllama.DefiLlamaClient._get") as mock_get:
        mock_get.return_value = expected_result

        protocols = dlclient.get_protocols()

        assert protocols == expected_result
        mock_get.assert_called_once_with(ApiSectionsEnum.TVL, "protocols")


def test_get_protocol(dlclient, mock_protocols, mock_get):
    protocol_slug = "protocol1"
    expected_result = {
        "protocol_slug": protocol_slug,
    }

    with patch(
        "dfllama.client.validate_searched_entity"
    ) as mock_validate_searched_entity:
        mock_validate_searched_entity.return_value = None
        mock_get.return_value = expected_result

        protocol_data = dlclient.get_protocol(protocol_slug)
        assert protocol_data == expected_result
        mock_validate_searched_entity.assert_called_once_with(
            protocol_slug.lower(), ["protocol1", "protocol2"], "protocol"
        )
        mock_get.assert_called_once_with(ApiSectionsEnum.TVL, "protocol", protocol_slug)


def test_get_protocol_invalid_protocol(dlclient, mock_protocols):
    protocol_slug = "invalid_protocol"

    with pytest.raises(ValueError):
        dlclient.get_protocol(protocol_slug)


def test_get_historical_tvl_of_defi_on_all_chains(dlclient):
    expected_result = [
        {
            "date": "2022-01-01",
            "tvl": 1000000000,
        },
        {
            "date": "2022-01-02",
            "tvl": 1100000000,
        },
    ]

    with patch("dfllama.DefiLlamaClient._get") as mock_get:
        mock_get.return_value = expected_result

        historical_tvl = dlclient.get_historical_tvl_of_defi_on_all_chains()

        assert historical_tvl == expected_result
        mock_get.assert_called_once_with(
            ApiSectionsEnum.TVL, "v2", "historicalChainTvl"
        )


def test_get_historical_tvl_for_chain(dlclient, mock_chains):
    chain_slug = "chain1"
    expected_result = [
        {
            "date": "2022-01-01",
            "tvl": 1000000000,
        },
        {
            "date": "2022-01-02",
            "tvl": 1100000000,
        },
        # ... other dictionaries ...
    ]

    with patch(
        "dfllama.client.validate_searched_entity"
    ) as mock_validate_searched_entity:
        mock_validate_searched_entity.return_value = None

        with patch("dfllama.client.DefiLlamaClient._get") as mock_get:
            mock_get.return_value = expected_result

            historical_tvl = dlclient.get_historical_tvl_for_chain(chain_slug)

            assert historical_tvl == expected_result
            mock_validate_searched_entity.assert_called_once_with(
                chain_slug.lower(), ["chain1", "chain2"], "chain"
            )
            mock_get.assert_called_once_with(
                ApiSectionsEnum.TVL, "v2", "historicalChainTvl", chain_slug
            )


def test_get_historical_tvl_for_chain_invalid_chain(dlclient, mock_chains):
    chain_slug = "invalid_chain"

    with pytest.raises(ValueError):
        dlclient.get_historical_tvl_for_chain(chain_slug)


def test_get_current_tvl_for_protocol(dlclient, mock_protocols):
    protocol_slug = "protocol1"
    expected_result = 1000000000

    with patch(
        "dfllama.client.validate_searched_entity"
    ) as mock_validate_searched_entity:
        mock_validate_searched_entity.return_value = None

        with patch("dfllama.client.DefiLlamaClient._get") as mock_get:
            mock_get.return_value = expected_result

            current_tvl = dlclient.get_current_tvl_for_protocol(protocol_slug)

            assert current_tvl == expected_result
            mock_validate_searched_entity.assert_called_once_with(
                protocol_slug.lower(), ["protocol1", "protocol2"], "protocol"
            )
            mock_get.assert_called_once_with(ApiSectionsEnum.TVL, "tvl", protocol_slug)


def test_get_current_tvl_for_protocol_invalid_protocol(dlclient, mock_protocols):
    protocol_slug = "invalid_protocol"

    with pytest.raises(ValueError):
        dlclient.get_current_tvl_for_protocol(protocol_slug)


def test_get_current_tvl_of_all_chains(dlclient):
    expected_result = [
        {
            "chain_name": "Chain 1",
            "chain_id": 1,
            "token_symbol": "TOKEN1",
            "tvl": 1000000000,
        },
        {
            "chain_name": "Chain 2",
            "chain_id": 2,
            "token_symbol": "TOKEN2",
            "tvl": 2000000000,
        },
        # ... other dictionaries ...
    ]

    with patch("dfllama.DefiLlamaClient._get") as mock_get:
        mock_get.return_value = expected_result

        current_tvl = dlclient.get_current_tvl_of_all_chains()

        assert current_tvl == expected_result
        mock_get.assert_called_once_with(ApiSectionsEnum.TVL, "v2", "chains")


def test_get_stablecoins(dlclient, mock_get):
    expected_result = [
        {
            "name": "Stablecoin 1",
            "circulating_amount": 1000000,
            "price": 1.0,
        },
        {
            "name": "Stablecoin 2",
            "circulating_amount": 2000000,
            "price": 1.1,
        },
    ]
    mock_get.return_value = {"peggedAssets": expected_result}
    stablecoins = dlclient.get_stablecoins()
    assert stablecoins == expected_result
    mock_get.assert_called_once_with(
        ApiSectionsEnum.STABLECOINS, "stablecoins", includePrices=True
    )


def test_get_stablecoins_exclude_prices(dlclient, mock_get):
    expected_result = [
        {
            "name": "Stablecoin 1",
            "circulating_amount": 1000000,
        },
        {
            "name": "Stablecoin 2",
            "circulating_amount": 2000000,
        },
    ]

    mock_get.return_value = {"peggedAssets": expected_result}
    stablecoins = dlclient.get_stablecoins(include_prices=False)
    assert stablecoins == expected_result
    mock_get.assert_called_once_with(
        ApiSectionsEnum.STABLECOINS, "stablecoins", includePrices=False
    )


def test_get_current_stablecoins_market_cap(dlclient, mock_get):
    expected_result = [
        {
            "chain_name": "Chain 1",
            "market_cap": 1000000000,
        },
        {
            "chain_name": "Chain 2",
            "market_cap": 2000000000,
        },
    ]

    mock_get.return_value = expected_result

    market_cap = dlclient.get_current_stablecoins_market_cap()

    assert market_cap == expected_result
    mock_get.assert_called_once_with(ApiSectionsEnum.STABLECOINS, "stablecoinchains")


@pytest.mark.parametrize(
    "stablecoin, stablecoin_id, expected_result",
    [
        (
            123,
            123,
            [
                {"date": "2021-01-01", "market_cap": 100000},
                {"date": "2021-01-02", "market_cap": 200000},
                {"date": "2021-01-03", "market_cap": 150000},
            ],
        ),
        (
            "USDT",
            123,
            [
                {"date": "2021-01-01", "market_cap": 100000},
                {"date": "2021-01-02", "market_cap": 200000},
                {"date": "2021-01-03", "market_cap": 150000},
            ],
        ),
        (
            None,
            None,
            [
                {"date": "2021-01-01", "market_cap": 100000},
                {"date": "2021-01-02", "market_cap": 200000},
                {"date": "2021-01-03", "market_cap": 150000},
            ],
        ),
    ],
)
def test_get_stablecoin_historical_market_cap(
    stablecoin, stablecoin_id, expected_result, mock_get, dlclient
):
    mock_get.return_value = expected_result
    dlclient._stablecoins = {123: "USDT"}

    result = dlclient.get_stablecoin_historical_market_cap(stablecoin)

    dlclient._get.assert_called_once_with(
        ApiSectionsEnum.STABLECOINS, "stablecoincharts", "all", stablecoin=stablecoin_id
    )
    assert result == expected_result


@pytest.mark.parametrize(
    "chain, stablecoin, stablecoin_id, expected_result",
    [
        (
            "chain1",
            "stablecoin1",
            1,
            [{"market_cap": 1000000}, {"market_cap": 2000000}],
        ),
        ("chain1", None, None, [{"market_cap": 1000000}, {"market_cap": 2000000}]),
    ],
)
def test_get_stablecoins_historical_martket_cap_in_chain_valid_chain_and_stablecoin(
    dlclient,
    mock_get,
    mock_chains,
    mock_stablecoins,
    chain,
    stablecoin,
    stablecoin_id,
    expected_result,
):
    mock_get.return_value = expected_result

    result = dlclient.get_stablecoins_historical_martket_cap_in_chain(chain, stablecoin)

    assert result == expected_result
    dlclient._get.assert_called_once_with(
        ApiSectionsEnum.STABLECOINS, "stablecoincharts", chain, stablecoin=stablecoin_id
    )


def test_get_stablecoins_historical_martket_cap_in_chain_invalid_chain(
    dlclient, mock_get, mock_chains, mock_stablecoins
):
    chain = "invalid_chain"
    stablecoin = "stablecoin1"

    with pytest.raises(ValueError):
        dlclient.get_stablecoins_historical_martket_cap_in_chain(chain, stablecoin)


@pytest.mark.parametrize(
    "stablecoin, expected_stablecoin_id, expected_result",
    [
        (
            "stablecoin1",
            1,
            {
                "market_cap": 1000000,
                "chain_distribution": {
                    "Ethereum": 500000,
                    "Binance Smart Chain": 500000,
                },
            },
        )
    ],
)
def test_get_stablecoins_historical_market_cap_and_chain_distribution(
    dlclient,
    mock_get,
    stablecoin,
    expected_stablecoin_id,
    expected_result,
    mock_stablecoins,
):
    dlclient.get_stablecoin_id = mock_get
    dlclient._get = mock_get

    dlclient.get_stablecoin_id.return_value = expected_stablecoin_id
    dlclient._get.return_value = expected_result

    result = dlclient.get_stablecoins_historical_market_cap_and_chain_distribution(
        stablecoin
    )

    dlclient._get.assert_called_once_with(
        ApiSectionsEnum.STABLECOINS, "stablecoin", expected_stablecoin_id
    )

    # Assert that the result is the expected result
    assert result == expected_result


def test_get_stablecoins_historical_prices(dlclient, mock_get):
    mock_get.return_value = [
        {"stablecoin": "USDT", "price": 1.0},
        {"stablecoin": "DAI", "price": 1.01},
        {"stablecoin": "USDC", "price": 1.02},
    ]

    result = dlclient.get_stablecoins_historical_prices()

    mock_get.assert_called_once_with(ApiSectionsEnum.STABLECOINS, "stablecoinprices")

    expected_result = [
        {"stablecoin": "USDT", "price": 1.0},
        {"stablecoin": "DAI", "price": 1.01},
        {"stablecoin": "USDC", "price": 1.02},
    ]
    assert result == expected_result


def test_get_pools(dlclient, mock_get):
    mock_get.return_value = {
        "data": [
            {"pool_id": 1, "name": "Pool 1"},
            {"pool_id": 2, "name": "Pool 2"},
            {"pool_id": 3, "name": "Pool 3"},
        ]
    }

    result = dlclient.get_pools()

    mock_get.assert_called_once_with(ApiSectionsEnum.YIELDS, "pools")

    expected_result = [
        {"pool_id": 1, "name": "Pool 1"},
        {"pool_id": 2, "name": "Pool 2"},
        {"pool_id": 3, "name": "Pool 3"},
    ]
    assert result == expected_result


def test_get_pool_historical_apy_and_tvl(dlclient, mock_get, mock_pools):
    mock_get.return_value = {
        "data": [
            {"date": "2022-01-01", "apy": 0.05, "tvl": 1000000},
            {"date": "2022-01-02", "apy": 0.06, "tvl": 1100000},
            {"date": "2022-01-03", "apy": 0.07, "tvl": 1200000},
        ]
    }

    result = dlclient.get_pool_historical_apy_and_tvl("symbol1")

    mock_get.assert_called_once_with(ApiSectionsEnum.YIELDS, "chart", "pool1")
    expected_result = [
        {"date": "2022-01-01", "apy": 0.05, "tvl": 1000000},
        {"date": "2022-01-02", "apy": 0.06, "tvl": 1100000},
        {"date": "2022-01-03", "apy": 0.07, "tvl": 1200000},
    ]
    assert result == expected_result


def test_get_bridges(dlclient, mock_get):
    mock_get.return_value = {
        "bridges": [
            {"name": "Bridge 1", "volume": 1000000},
            {"name": "Bridge 2", "volume": 2000000},
            {"name": "Bridge 3", "volume": 3000000},
        ]
    }

    result = dlclient.get_bridges()

    mock_get.assert_called_once_with(
        ApiSectionsEnum.BRIDGES, "bridges", includeChains=True
    )

    expected_result = [
        {"name": "Bridge 1", "volume": 1000000},
        {"name": "Bridge 2", "volume": 2000000},
        {"name": "Bridge 3", "volume": 3000000},
    ]
    assert result == expected_result


def test_get_bridge(dlclient, mock_get, mock_get_bridge_id, mock_bridges):
    mock_get_bridge_id.return_value = "bridge_id"
    mock_get.return_value = {
        "bridge_id": "bridge_id",
        "volume": 1000000,
        "volume_breakdown": {
            "chain1": 500000,
            "chain2": 500000,
        },
    }

    result = dlclient.get_bridge("Bridge 1")

    mock_get_bridge_id.assert_called_once_with("Bridge 1", dlclient._bridges)

    mock_get.assert_called_once_with(ApiSectionsEnum.BRIDGES, "bridge", "bridge_id")

    expected_result = {
        "bridge_id": "bridge_id",
        "volume": 1000000,
        "volume_breakdown": {
            "chain1": 500000,
            "chain2": 500000,
        },
    }
    assert result == expected_result


@pytest.mark.parametrize(
    "chain, bridge, bridge_id, expected_volume",
    [
        ("dex_chain1", "bridge1", 1, [{"volume": 100}, {"volume": 200}]),
        ("dex_chain2", None, None, [{"volume": 300}, {"volume": 400}]),
    ],
)
def test_get_bridge_valid(
    dlclient,
    mock_get,
    chain,
    bridge,
    bridge_id,
    expected_volume,
    mock_bridges,
    mock_dex_chains,
):
    mock_get.return_value = expected_volume

    result = dlclient.get_bridge_volume(chain, bridge)

    mock_get.assert_called_once_with(
        ApiSectionsEnum.BRIDGES, "bridgevolume", chain, id=bridge_id
    )
    assert result == expected_volume


@pytest.mark.parametrize(
    "chain, bridge",
    [
        ("invalid_chain", "bridge1"),
        ("chain1", "bridge3"),
    ],
)
def test_get_bridge_invalid(dlclient, mock_get, chain, bridge, mock_bridges):
    with pytest.raises(ValueError):
        dlclient.get_bridge_volume(chain, bridge)


@pytest.mark.parametrize(
    "chain, bridge, dex_chains, bridges, expected_volume",
    [
        (
            "chain1",
            "bridge1",
            ["chain1", "chain2"],
            [{"id": 1, "name": "bridge1"}, {"id": 2, "name": "bridge2"}],
            [{"volume": 100}, {"volume": 200}],
        ),
        (
            "chain2",
            None,
            ["chain1", "chain2"],
            [{"id": 1, "name": "bridge1"}, {"id": 2, "name": "bridge2"}],
            [{"volume": 300}, {"volume": 400}],
        ),
    ],
)
def test_get_bridge_volume_valid(
    dlclient,
    mock_validate_searched_entity,
    mock_get_bridge_id,
    mock_get,
    chain,
    bridge,
    dex_chains,
    bridges,
    expected_volume,
):
    mock_validate_searched_entity.return_value = None
    mock_get_bridge_id.return_value = 1 if bridge == "bridge1" else None
    mock_get.return_value = expected_volume

    dlclient._dex_chains = dex_chains
    dlclient._bridges = bridges
    result = dlclient.get_bridge_volume(chain, bridge)

    mock_validate_searched_entity.assert_called_once_with(chain, dex_chains, "chain")
    if bridge is not None:
        mock_get_bridge_id.assert_called_once_with(bridge, bridges)
    else:
        mock_get_bridge_id.assert_not_called()
    mock_get.assert_called_once_with(
        ApiSectionsEnum.BRIDGES,
        "bridgevolume",
        chain,
        id=1 if bridge == "bridge1" else None,
    )
    assert result == expected_volume


@pytest.mark.parametrize(
    "chain, bridge, dex_chains, bridges",
    [
        (
            "invalid_chain",
            "bridge1",
            ["chain1", "chain2"],
            [{"id": 1, "name": "bridge1"}, {"id": 2, "name": "bridge2"}],
        ),
        (
            "chain1",
            "bridge3",
            ["chain1", "chain2"],
            [{"id": 1, "name": "bridge1"}, {"id": 2, "name": "bridge2"}],
        ),
    ],
)
def test_get_bridge_volume_invalid(
    dlclient,
    mock_validate_searched_entity,
    mock_get_bridge_id,
    mock_get,
    chain,
    bridge,
    dex_chains,
    bridges,
):
    mock_validate_searched_entity.side_effect = ValueError
    mock_get_bridge_id.return_value = None

    dlclient._dex_chains = dex_chains
    dlclient._bridges = bridges

    with pytest.raises(ValueError):
        dlclient.get_bridge_volume(chain, bridge)


@pytest.mark.parametrize(
    "timestamp, chain, bridge, dex_chains, bridges, expected_stats",
    [
        (
            1234567890,
            "chain1",
            "bridge1",
            ["chain1", "chain2"],
            [{"id": 1, "name": "bridge1"}, {"id": 2, "name": "bridge2"}],
            [{"volume": 100}, {"volume": 200}],
        ),
        (
            1234567890,
            "chain2",
            None,
            ["chain1", "chain2"],
            [{"id": 1, "name": "bridge1"}, {"id": 2, "name": "bridge2"}],
            [{"volume": 300}, {"volume": 400}],
        ),
    ],
)
def test_get_bridge_day_stats_valid(
    dlclient,
    mock_validate_searched_entity,
    mock_get_bridge_id,
    mock_get,
    timestamp,
    chain,
    bridge,
    dex_chains,
    bridges,
    expected_stats,
):
    mock_validate_searched_entity.return_value = None
    mock_get_bridge_id.return_value = 1 if bridge == "bridge1" else None
    mock_get.return_value = expected_stats

    dlclient._dex_chains = dex_chains
    dlclient._bridges = bridges
    result = dlclient.get_bridge_day_stats(timestamp, chain, bridge)

    mock_validate_searched_entity.assert_called_once_with(chain, dex_chains, "chain")
    if bridge is not None:
        mock_get_bridge_id.assert_called_once_with(bridge, bridges)
    else:
        mock_get_bridge_id.assert_not_called()
    mock_get.assert_called_once_with(
        ApiSectionsEnum.BRIDGES,
        "bridgedaystats",
        timestamp,
        chain,
        id=1 if bridge == "bridge1" else None,
    )
    assert result == expected_stats


@pytest.mark.parametrize(
    "timestamp, chain, bridge, dex_chains, bridges",
    [
        (
            1234567890,
            "invalid_chain",
            "bridge1",
            ["chain1", "chain2"],
            [{"id": 1, "name": "bridge1"}, {"id": 2, "name": "bridge2"}],
        ),
        (
            1234567890,
            "chain1",
            "bridge3",
            ["chain1", "chain2"],
            [{"id": 1, "name": "bridge1"}, {"id": 2, "name": "bridge2"}],
        ),
    ],
)
def test_get_bridge_day_stats_invalid(
    dlclient,
    mock_validate_searched_entity,
    mock_get_bridge_id,
    mock_get,
    timestamp,
    chain,
    bridge,
    dex_chains,
    bridges,
):
    mock_validate_searched_entity.side_effect = ValueError
    mock_get_bridge_id.return_value = None

    dlclient._dex_chains = dex_chains
    dlclient._bridges = bridges

    with pytest.raises(ValueError):
        dlclient.get_bridge_day_stats(timestamp, chain, bridge)


@pytest.mark.parametrize(
    "bridge, start_timestamp, end_timestamp, source_chain, address, limit, expected_transactions",
    [
        (
            "bridge1",
            1234567890,
            1234567999,
            "chain1",
            "ethereum:0x1234567890abcdef",
            10,
            [{"transaction_id": "tx1"}, {"transaction_id": "tx2"}],
        ),
        (
            2,
            None,
            None,
            None,
            None,
            20,
            [{"transaction_id": "tx3"}, {"transaction_id": "tx4"}],
        ),
    ],
)
def test_get_bridge_transactions_valid(
    dlclient,
    mock_get_bridge_id,
    mock_validate_searched_entity,
    mock_get,
    bridge,
    start_timestamp,
    end_timestamp,
    source_chain,
    address,
    limit,
    mock_bridges,
    mock_dex_chains,
    expected_transactions,
):
    _bridge_value = 1 if bridge == "bridge1" else 2
    mock_get_bridge_id.return_value = _bridge_value
    mock_validate_searched_entity.return_value = None
    mock_get.return_value = expected_transactions

    result = dlclient.get_bridge_transactions(
        bridge,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        source_chain=source_chain,
        address=address,
        limit=limit,
    )

    mock_get_bridge_id.assert_called_once()
    if source_chain is not None:
        mock_validate_searched_entity.assert_called_once_with(
            source_chain, dlclient._dex_chains, "chain"
        )
    else:
        mock_validate_searched_entity.assert_not_called()
    mock_get.assert_called_once_with(
        ApiSectionsEnum.BRIDGES,
        "transactions",
        _bridge_value,
        starttimestamp=start_timestamp,
        endtimestamp=end_timestamp,
        sourcechain=source_chain,
        address=address,
        limit=limit,
    )
    assert result == expected_transactions


def test_get_bridge_transactions_no_bridge(dlclient, mock_bridges, mock_dex_chains):
    with pytest.raises(ValueError):
        dlclient.get_bridge_transactions("not_existing_bridge")


def test_get_bridge_transactions_invalid_source_chain(
    dlclient, mock_get_bridge_id, mock_validate_searched_entity, mock_bridges
):
    mock_get_bridge_id.return_value = 1
    mock_validate_searched_entity.side_effect = ValueError
    with pytest.raises(ValueError):
        dlclient.get_bridge_transactions("bridge1", source_chain="invalid_chain")


@pytest.mark.parametrize(
    "exclude_total_data_chart, exclude_total_data_chart_breakdown, data_type, expected_result",
    [
        (
            True,
            True,
            "dailyVolume",
            {
                "dexs": [
                    {"name": "dex1", "volume": 100},
                    {"name": "dex2", "volume": 200},
                ]
            },
        ),
        (
            False,
            False,
            "totalVolume",
            {
                "dexs": [
                    {"name": "dex3", "volume": 300},
                    {"name": "dex4", "volume": 400},
                ]
            },
        ),
    ],
)
def test_get_dexes_volume_overview(
    dlclient,
    mock_get,
    exclude_total_data_chart,
    exclude_total_data_chart_breakdown,
    data_type,
    expected_result,
):
    mock_get.return_value = expected_result

    result = dlclient.get_dexes_volume_overview(
        exclude_total_data_chart=exclude_total_data_chart,
        exclude_total_data_chart_breakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )

    mock_get.assert_called_once_with(
        ApiSectionsEnum.VOLUMES,
        "overview",
        "dexs",
        excludeTotalDataChart=exclude_total_data_chart,
        excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )
    assert result == expected_result


@pytest.mark.parametrize(
    "chain, exclude_total_data_chart, exclude_total_data_chart_breakdown, data_type, expected_result",
    [
        (
            "chain1",
            True,
            True,
            "dailyVolume",
            {
                "dexs": [
                    {"name": "dex1", "volume": 100},
                    {"name": "dex2", "volume": 200},
                ]
            },
        ),
        (
            "chain2",
            False,
            False,
            "totalVolume",
            {
                "dexs": [
                    {"name": "dex3", "volume": 300},
                    {"name": "dex4", "volume": 400},
                ]
            },
        ),
    ],
)
def test_get_dexes_volume_overview_for_chain(
    dlclient,
    mock_validate_searched_entity,
    mock_get,
    chain,
    exclude_total_data_chart,
    exclude_total_data_chart_breakdown,
    data_type,
    expected_result,
    mock_dex_chains,
):
    mock_validate_searched_entity.return_value = None
    mock_get.return_value = expected_result

    result = dlclient.get_dexes_volume_overview_for_chain(
        chain,
        exclude_total_data_chart=exclude_total_data_chart,
        exclude_total_data_chart_breakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )

    mock_validate_searched_entity.assert_called_once_with(
        chain, dlclient._dex_chains, "chain"
    )
    mock_get.assert_called_once_with(
        ApiSectionsEnum.VOLUMES,
        "overview",
        "dexs",
        chain,
        excludeTotalDataChart=exclude_total_data_chart,
        excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )
    assert result == expected_result


def test_get_dexes_volume_overview_for_chain_invalid_chain(
    dlclient, mock_validate_searched_entity
):
    mock_validate_searched_entity.side_effect = ValueError

    with pytest.raises(ValueError):
        dlclient.get_dexes_volume_overview_for_chain("invalid_chain")


@pytest.mark.parametrize(
    "protocol, exclude_total_data_chart, exclude_total_data_chart_breakdown, data_type, expected_result",
    [
        (
            "protocol1",
            True,
            True,
            "dailyVolume",
            {"summary": {"volume": 1000, "trades": 200}},
        ),
        (
            "protocol2",
            False,
            False,
            "totalVolume",
            {"summary": {"volume": 3000, "trades": 400}},
        ),
    ],
)
def test_get_summary_of_dex_volume_with_historical_data(
    dlclient,
    mock_validate_searched_entity,
    mock_get,
    protocol,
    exclude_total_data_chart,
    exclude_total_data_chart_breakdown,
    data_type,
    expected_result,
    mock_dex_protocols,
):
    mock_validate_searched_entity.return_value = None
    mock_get.return_value = expected_result

    result = dlclient.get_summary_of_dex_volume_with_historical_data(
        protocol,
        exclude_total_data_chart=exclude_total_data_chart,
        exclude_total_data_chart_breakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )

    mock_validate_searched_entity.assert_called_once_with(
        protocol.lower(), dlclient._dex_protocols, "dex protocol"
    )
    mock_get.assert_called_once_with(
        ApiSectionsEnum.VOLUMES,
        "summary",
        "dexs",
        protocol,
        excludeTotalDataChart=exclude_total_data_chart,
        excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )
    assert result == expected_result


def test_get_summary_of_dex_volume_with_historical_data_invalid_protocol(
    dlclient, mock_validate_searched_entity
):
    mock_validate_searched_entity.side_effect = ValueError

    with pytest.raises(ValueError):
        dlclient.get_summary_of_dex_volume_with_historical_data("invalid_protocol")


@pytest.mark.parametrize(
    "exclude_total_data_chart, exclude_total_data_chart_breakdown, data_type, expected_result",
    [
        (
            True,
            True,
            "dailyPremiumVolume",
            {
                "options": [
                    {"name": "option1", "volume": 100},
                    {"name": "option2", "volume": 200},
                ]
            },
        ),
        (
            False,
            False,
            "totalPremiumVolume",
            {
                "options": [
                    {"name": "option3", "volume": 300},
                    {"name": "option4", "volume": 400},
                ]
            },
        ),
    ],
)
def test_get_overview_dexes_options(
    dlclient,
    mock_get,
    exclude_total_data_chart,
    exclude_total_data_chart_breakdown,
    data_type,
    expected_result,
):
    mock_get.return_value = expected_result

    result = dlclient.get_overview_dexes_options(
        exclude_total_data_chart=exclude_total_data_chart,
        exclude_total_data_chart_breakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )

    mock_get.assert_called_once_with(
        ApiSectionsEnum.VOLUMES,
        "overview",
        "options",
        excludeTotalDataChart=exclude_total_data_chart,
        excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )
    assert result == expected_result


@pytest.mark.parametrize(
    "chain, exclude_total_data_chart, exclude_total_data_chart_breakdown, data_type, expected_result",
    [
        (
            "chain1",
            True,
            True,
            "dailyPremiumVolume",
            {
                "options": [
                    {"name": "option1", "volume": 100},
                    {"name": "option2", "volume": 200},
                ]
            },
        ),
        (
            "chain2",
            False,
            False,
            "totalPremiumVolume",
            {
                "options": [
                    {"name": "option3", "volume": 300},
                    {"name": "option4", "volume": 400},
                ]
            },
        ),
    ],
)
def test_get_overview_dexes_options_for_chain(
    dlclient,
    mock_validate_searched_entity,
    mock_get,
    chain,
    exclude_total_data_chart,
    exclude_total_data_chart_breakdown,
    data_type,
    expected_result,
    mock_options_chains,
    mock_options_protocols,
):
    mock_validate_searched_entity.return_value = None
    mock_get.return_value = expected_result

    result = dlclient.get_overview_dexes_options_for_chain(
        chain,
        exclude_total_data_chart=exclude_total_data_chart,
        exclude_total_data_chart_breakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )

    mock_validate_searched_entity.assert_called_once_with(
        chain, dlclient._dex_options_chains, "chain"
    )
    mock_get.assert_called_once_with(
        ApiSectionsEnum.VOLUMES,
        "overview",
        "options",
        chain,
        excludeTotalDataChart=exclude_total_data_chart,
        excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )
    assert result == expected_result


def test_get_overview_dexes_options_for_chain_invalid_chain(
    dlclient, mock_validate_searched_entity
):
    mock_validate_searched_entity.side_effect = ValueError

    with pytest.raises(ValueError):
        dlclient.get_overview_dexes_options_for_chain("invalid_chain")


@pytest.mark.parametrize(
    "protocol, data_type, expected_result",
    [
        (
            "protocol1",
            "dailyPremiumVolume",
            {"summary": {"volume": 1000, "averageVolume": 200}},
        ),
        (
            "protocol2",
            "totalPremiumVolume",
            {"summary": {"volume": 5000, "averageVolume": 1000}},
        ),
    ],
)
def test_get_summary_of_options_volume_with_historical_data_for_protocol(
    dlclient,
    mock_validate_searched_entity,
    mock_get,
    protocol,
    data_type,
    expected_result,
    mock_options_protocols,
    mock_options_chains,
):
    mock_validate_searched_entity.return_value = None
    mock_get.return_value = expected_result

    result = dlclient.get_summary_of_options_volume_with_historical_data_for_protocol(
        protocol,
        dataType=data_type,
    )

    mock_validate_searched_entity.assert_called_once_with(
        protocol.lower(), dlclient._dex_options_protocols, "protocol"
    )
    mock_get.assert_called_once_with(
        ApiSectionsEnum.VOLUMES,
        "summary",
        "options",
        protocol,
        dataType=data_type,
    )
    assert result == expected_result


def test_get_summary_of_options_volume_with_historical_data_for_protocol_invalid_protocol(
    dlclient, mock_validate_searched_entity
):
    mock_validate_searched_entity.side_effect = ValueError

    with pytest.raises(ValueError):
        dlclient.get_summary_of_options_volume_with_historical_data_for_protocol(
            "invalid_protocol"
        )


@pytest.mark.parametrize(
    "exclude_total_data_chart, exclude_total_data_chart_breakdown, data_type, expected_result",
    [
        (True, True, "dailyFees", {"fees": {"protocol1": 100, "protocol2": 200}}),
        (False, False, "totalFees", {"fees": {"protocol3": 300, "protocol4": 400}}),
    ],
)
def test_get_fees_and_revenues_for_all_protocols(
    dlclient,
    mock_get,
    exclude_total_data_chart,
    exclude_total_data_chart_breakdown,
    data_type,
    expected_result,
):
    mock_get.return_value = expected_result

    result = dlclient.get_fees_and_revenues_for_all_protocols(
        exclude_total_data_chart=exclude_total_data_chart,
        exclude_total_data_chart_breakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )

    mock_get.assert_called_once_with(
        ApiSectionsEnum.FEES,
        "overview",
        "fees",
        excludeTotalDataChart=exclude_total_data_chart,
        excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )
    assert result == expected_result


@pytest.mark.parametrize(
    "chain, exclude_total_data_chart, exclude_total_data_chart_breakdown, data_type, expected_result",
    [
        (
            "chain1",
            True,
            True,
            "dailyFees",
            {"fees": {"protocol1": 100, "protocol2": 200}},
        ),
        (
            "chain2",
            False,
            False,
            "totalFees",
            {"fees": {"protocol3": 300, "protocol4": 400}},
        ),
    ],
)
def test_get_fees_and_revenues_for_all_protocols_for_chain(
    dlclient,
    mock_validate_searched_entity,
    mock_get,
    chain,
    exclude_total_data_chart,
    exclude_total_data_chart_breakdown,
    data_type,
    expected_result,
    mock_fees_chains,
    mock_fees_protocols,
):
    mock_validate_searched_entity.return_value = None
    mock_get.return_value = expected_result

    result = dlclient.get_fees_and_revenues_for_all_protocols_for_chain(
        chain,
        exclude_total_data_chart=exclude_total_data_chart,
        exclude_total_data_chart_breakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )

    mock_validate_searched_entity.assert_called_once_with(
        chain.lower(), dlclient._fees_chains, "chain"
    )
    mock_get.assert_called_once_with(
        ApiSectionsEnum.FEES,
        "overview",
        "fees",
        chain,
        excludeTotalDataChart=exclude_total_data_chart,
        excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
        dataType=data_type,
    )
    assert result == expected_result


def test_get_fees_and_revenues_for_all_protocols_for_chain_invalid_chain(
    dlclient, mock_validate_searched_entity
):
    mock_validate_searched_entity.side_effect = ValueError

    with pytest.raises(ValueError):
        dlclient.get_fees_and_revenues_for_all_protocols_for_chain("invalid_chain")


@pytest.mark.parametrize(
    "protocol, data_type, expected_result",
    [
        ("protocol1", "dailyFees", {"fees": 100, "revenue": 200}),
        ("protocol2", "totalFees", {"fees": 300, "revenue": 400}),
    ],
)
def test_get_summary_of_protocols_fees_and_revenue(
    dlclient,
    mock_validate_searched_entity,
    mock_get,
    protocol,
    data_type,
    expected_result,
    mock_fees_protocols,
    mock_fees_chains,
):
    mock_validate_searched_entity.return_value = None
    mock_get.return_value = expected_result

    result = dlclient.get_summary_of_protocols_fees_and_revenue(
        protocol,
        dataType=data_type,
    )

    mock_validate_searched_entity.assert_called_once_with(
        protocol.lower(), dlclient._fees_protocols, "protocol"
    )
    mock_get.assert_called_once_with(
        ApiSectionsEnum.FEES,
        "summary",
        "fees",
        protocol,
        dataType=data_type,
    )
    assert result == expected_result


def test_get_summary_of_protocols_fees_and_revenue_invalid_protocol(
    dlclient, mock_validate_searched_entity
):
    mock_validate_searched_entity.side_effect = ValueError

    with pytest.raises(ValueError):
        dlclient.get_summary_of_protocols_fees_and_revenue("invalid_protocol")
