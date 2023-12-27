import enum
from typing import Any, Dict, List
import requests
import pprint
from exc import InvalidResponseDataException, InvalidResponseStatusCodeException
from utils import get_retry_session
from log import get_logger


log = get_logger(__name__)


class ApiSectionsEnum(str, enum.Enum):
    TVL = "tvl"
    COINS = "coins"
    STABLECOINS = "stablecoins"
    YIELDS = "yields"
    BRIDGES = "bridges"
    VOLUMES = "volumes"
    FEES = "fees"


class DefiLlamaClient:
    def __init__(self, **kwargs) -> None:
        self._urls = {
            "tvl": "https://api.llama.fi",
            "coins": "https://coins.llama.fi",
            "stablecoins": "https://stablecoins.llama.fi",
            "yields": "https://yields.llama.fi",
            "bridges": "https://bridges.llama.fi",
            "volumes": "https://api.llama.fi",
            "fees": "https://api.llama.fi",
        }
        self._session: requests.Session = get_retry_session()

        if "headers" in kwargs:
            self._session.headers.update(kwargs["headers"])

    def _resolve_api_url(self, section: str) -> str:
        if section not in self._urls.keys():
            raise ValueError(f"Invalid section: {section}")
        return self._urls[section]

    def _build_endpoint_url(self, section: str, endpoint: str, *args) -> str:
        url = f"{self._resolve_api_url(section)}/{endpoint}"
        if args:
            url += "/" + "/".join(args)
        return url

    @property
    def session(self) -> requests.Session:
        return self._session

    def _get(
        self, section: ApiSectionsEnum, endpoint: str, *args, **query_params
    ) -> requests.Response:
        r = self.session.get(
            self._build_endpoint_url(section, endpoint, *args),
            params=query_params,
        )
        return self._handle_response(r)

    def _handle_response(self, response: requests.Response) -> dict:
        """
        Handle the response from an HTTP request and return the response data as a dictionary.

        Parameters:
            response (requests.Response): The HTTP response object.

        Returns:
            dict: The response data as a dictionary.

        Raises:
            InvalidResponseDataException: If the response data is invalid.
        """
        response.raise_for_status()
        try:
            data = response.json()
        except (AttributeError, requests.exceptions.JSONDecodeError) as ve:
            raise InvalidResponseDataException(f"Invalid data: {response.text}") from ve
        return data

    def get_protocols(self) -> List[Dict[Any, Any]]:
        """List all protocols on defillama along with their tvl."""
        return self._get(ApiSectionsEnum.TVL, "protocols")

    def get_protocol(self, protocol: str) -> Dict[Any, Any]:
        """Get historical TVL of a protocol and breakdowns by token and chain.

        Parameters:
            protocol (str): The protocol slug to retrieve.

        Returns:
            The historical TVL of the protocol and breakdowns by token and chain.
        """
        return self._get(ApiSectionsEnum.TVL, "protocol", protocol)

    def get_historical_tvl_of_defi_on_all_chains(self) -> List[Dict[Any, Any]]:
        """
        Retrieves the historical total value locked (TVL) of decentralized finance (DeFi) on all chains.

        Returns:
            A list of dictionaries representing the historical TVL data for each chain. Each dictionary contains
            the date and the corresponding TVL value.
        """
        return self._get(ApiSectionsEnum.TVL, "v2", "historicalChainTvl")

    def get_historical_tvl_for_chain(self, chain: str) -> List[Dict[Any, Any]]:
        """
        Returns the historical total value locked (TVL) for a specific chain.

        Parameters:
            chain (str): chain slug, you can get these from /chains or the chains property on /protocols

        Returns:
            The historical TVL for the specified chain. The returned data is a list of dictionaries, where each
            dictionary contains the date and the corresponding TVL value.
        """

        return self._get(ApiSectionsEnum.TVL, "v2", "historicalChainTvl", chain)

    def get_current_tvl_for_protocol(self, protocol: str) -> int:
        """
        Get the current total value locked (TVL) for a given protocol.

        Parameters:
            protocol (str): The protocol slug to retrieve.

        Returns:
            int: The current TVL for the specified protocol.
        """

        return self._get(ApiSectionsEnum.TVL, "tvl", protocol)

    def get_current_tvl_of_all_chains(self) -> List[Dict[Any, Any]]:
        """Get the current total value locked (TVL) of all chains.

        Returns:
            The current TVL for all chains. The returned data is a list of dictionaries, where each dictionary contains
            the chain name, id, token symbol and the corresponding TVL value.

        """
        return self._get(ApiSectionsEnum.TVL, "v2", "chains")

    def get_stablecoins(self, include_prices: bool = True) -> List[Dict[Any, Any]]:
        """
        List all stablecoins along with their circulating ammounts.

        Parameters:
            include_prices (bool, optional): Whether to include current stablecoin prices. Defaults to True.

        Returns:
            List[Dict[Any, Any]]: A list of dictionaries representing the stablecoins.
        """
        return self._get(
            ApiSectionsEnum.STABLECOINS, "stablecoins", includePrices=include_prices
        )

    def get_current_stablecoins_market_cap(
        self,
    ):
        """
        Retrieves the current market capitalization of stablecoins on each chain.

        Returns:
            float: The total market capitalization of stablecoins.
        """
        return self._get(ApiSectionsEnum.STABLECOINS, "stablecoinchains")

    def get_stablecoins_historical_market_cap(self, stablecoin_id: int):
        """
        Retrieves the historical market capitalization data for a specific stablecoin.

        Parameters:
            stablecoin_id (int): The ID of the stablecoin.  Can be obtained from /stablecoins

        Returns:
            The historical market capitalization data for the specified stablecoin.
        """
        return self._get(
            ApiSectionsEnum.STABLECOINS,
            "stablecoincharts",
            "all",
            stablecoin=stablecoin_id,
        )

    def get_stablecoins_historical_martket_cap_in_chain(
        self, chain: str = "Ethereum", stablecoin_id: int = 1
    ):
        """Get the historical market cap and distribution of stablecoins in the specified blockchain.

        Parameters:
            chain (str, optional): The name of the blockchain. Defaults to "Ethereum".
            stablecoin_id (int, optional): The ID of the stablecoin. Defaults to 1.

        Returns:
            The historical market cap of the stablecoin in the specified blockchain.
        """
        return self._get(
            ApiSectionsEnum.STABLECOINS,
            "stablecoincharts",
            chain,
            stablecoin=stablecoin_id,
        )

    def get_stablecoins_historical_market_cap_and_chain_distribution(
        self, stablecoin_id: int = 1
    ):
        return self._get(ApiSectionsEnum.STABLECOINS, "stablecoin", stablecoin_id)

    def get_stablecoins_historical_prices(self):
        return self._get(ApiSectionsEnum.STABLECOINS, "stablecoinprices")

    def get_pools(self):
        return self._get(ApiSectionsEnum.YIELDS, "pools")

    def get_pool_historical_apy_and_tvl(self, pool_id: int):
        return self._get(ApiSectionsEnum.YIELDS, "chart", pool_id)

    def get_bridges(self, include_chains: bool = True):
        return self._get(
            ApiSectionsEnum.BRIDGES, "bridges", includeChains=include_chains
        )

    def get_bridge(self, bridge_id: int):
        return self._get(ApiSectionsEnum.BRIDGES, "bridge", bridge_id)

    def get_bridge_volume(self, chain: str, bridge_id: int):
        return self._get(ApiSectionsEnum.BRIDGES, "bridgevolume", chain, id=bridge_id)

    def get_bridge_day_stats(self, timestamp: int, chain: str, bridge_id: int):
        return self._get(
            ApiSectionsEnum.BRIDGES, "bridgedaystats", timestamp, chain, id=bridge_id
        )

    def get_bridge_transactions(
        self,
        bridge_id: int,
        start_timestamp: int,
        end_timestamp: int,
        source_chain: str,
        address: str,
        limit: int = 200,
    ):
        return self._get(
            ApiSectionsEnum.BRIDGES,
            "transactions",
            bridge_id,
            starttimestamp=start_timestamp,
            endtimestamp=end_timestamp,
            sourcechain=source_chain,
            address=address,
            limit=limit,
        )

    def get_dexes_volume_overview(
        self,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        dataType: str = "dailyVolume",
    ):
        return self._get(
            ApiSectionsEnum.VOLUMES,
            "overview",
            "dexs",
            excludeTotalDataChart=exclude_total_data_chart,
            excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
            dataType=dataType,
        )

    def get_dexes_volume_overview_for_chain(
        self,
        chain: str,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        dataType: str = "dailyVolume",
    ):
        return self._get(
            ApiSectionsEnum.VOLUMES,
            "overview",
            "dexs",
            chain,
            excludeTotalDataChart=exclude_total_data_chart,
            excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
            dataType=dataType,
        )
