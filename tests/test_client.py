import pytest
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
