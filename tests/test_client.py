from unittest.mock import MagicMock, patch
from defillama.exc import InvalidResponseDataException
import pytest
from requests import Response
import requests
from defillama.client import DefiLlamaClient, ApiSectionsEnum


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
    result = client.list_protocols_slugs()
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
    with patch(
        "defillama.client.get_coingecko_coin_ids"
    ) as mock_get_coingecko_coin_ids:
        with patch(
            "defillama.client.read_coingecko_ids_from_file"
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

    with patch("defillama.DefiLlamaClient._get") as mock_get:
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
        "defillama.client.validate_searched_entity"
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

    with patch("defillama.DefiLlamaClient._get") as mock_get:
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
        "defillama.client.validate_searched_entity"
    ) as mock_validate_searched_entity:
        mock_validate_searched_entity.return_value = None

        with patch("defillama.client.DefiLlamaClient._get") as mock_get:
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
        "defillama.client.validate_searched_entity"
    ) as mock_validate_searched_entity:
        mock_validate_searched_entity.return_value = None

        with patch("defillama.client.DefiLlamaClient._get") as mock_get:
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

    with patch("defillama.DefiLlamaClient._get") as mock_get:
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
