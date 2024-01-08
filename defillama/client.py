import enum
import uuid
from functools import cached_property
from typing import Any, Dict, List, Optional, Union

import requests
from slugify import slugify

from defillama.dtypes import Coin, UUIDstr
from defillama.exc import InvalidResponseDataException
from defillama.log import get_logger
from defillama.utils import (
    get_bridge_id,
    get_coingecko_coin_ids,
    get_previous_timestamp,
    get_retry_session,
    get_stablecoin_id,
    prepare_coins_for_request,
    read_coingecko_ids_from_file,
    validate_searched_entity,
)

log = get_logger(__name__)


class ApiSectionsEnum(str, enum.Enum):
    """The available API sections."""

    TVL = "tvl"
    COINS = "coins"
    STABLECOINS = "stablecoins"
    YIELDS = "yields"
    BRIDGES = "bridges"
    VOLUMES = "volumes"
    FEES = "fees"


class DexDataTypeEnum(str, enum.Enum):
    """The available data types."""

    dailyVolume = "dailyVolume"
    totalVolume = "totalVolume"


class OptionsDataTypeEnum(str, enum.Enum):
    """The available options data types."""

    dailyPremiumVolume = "dailyPremiumVolume"
    totalPremiumVolume = "totalPremiumVolume"
    dailyNotionalVolume = "dailyNotionalVolume"
    totalNotionalVolume = "totalNotionalVolume"


class FeesDataTypeEnum(str, enum.Enum):
    """The available fees data types."""

    dailyFees = "dailyFees"
    totalFees = "totalFees"
    dailyRevenue = "dailyRevenue"
    totalRevenue = "totalRevenue"


class DefiLlamaClient:
    """This class represents a client for interacting with the DeFi Llama API.

    To use this class, simply create an instance of it and call its methods to interact with the API.
    To see details on how to use the API, refer to the documentation at https://defillama.com/docs/api.

    """

    def __init__(self, **kwargs) -> None:
        """Initializes the Defi Llama Client object.

        Parameters:
            **kwargs (dict): Additional keyword arguments.
        """

        self._urls: Dict[ApiSectionsEnum, str] = {
            ApiSectionsEnum.TVL: "https://api.llama.fi",
            ApiSectionsEnum.COINS: "https://coins.llama.fi",
            ApiSectionsEnum.STABLECOINS: "https://stablecoins.llama.fi",
            ApiSectionsEnum.YIELDS: "https://yields.llama.fi",
            ApiSectionsEnum.BRIDGES: "https://bridges.llama.fi",
            ApiSectionsEnum.VOLUMES: "https://api.llama.fi",
            ApiSectionsEnum.FEES: "https://api.llama.fi",
        }
        self._session: requests.Session = get_retry_session()

        if "headers" in kwargs:
            self._session.headers.update(kwargs["headers"])

    def _resolve_api_url(self, section: ApiSectionsEnum) -> str:
        """
        Resolves the API URL for the specified section.

        Parameters:
            section (ApiSectionsEnum): The section for which to resolve the API URL.

        Returns:
            str: The resolved API URL.

        Raises:
            ValueError: If the specified section is not valid.
        """

        if section not in self._urls:
            raise ValueError(f"Invalid section: {section}")
        return self._urls[section]

    def _build_endpoint_url(
        self, section: ApiSectionsEnum, endpoint: str, *args
    ) -> str:
        """
        Builds and returns the endpoint URL for the given API section,
        endpoint, and optional arguments.

        Parameters:
            section (ApiSectionsEnum): The API section.
            endpoint (str): The endpoint.
            *args: Optional arguments.

        Returns:
            str: The built endpoint URL.
        """

        url = f"{self._resolve_api_url(section)}/{endpoint}"
        if args:
            url += "/" + "/".join([str(arg) for arg in args if arg])
        return url

    @property
    def session(self) -> requests.Session:
        """
        Getter method for the session property.

        Returns:
            requests.Session: The session property.
        """
        return self._session

    def _get(
        self, section: ApiSectionsEnum, endpoint: str, *args, **query_params
    ) -> requests.Response:
        """
        Sends a GET request to the specified API endpoint.

        Parameters:
            section (ApiSectionsEnum): The section of the API to send the request to.
            endpoint (str): The endpoint of the API to send the request to.
            args: Variable length argument list.
            query_params: Keyword arguments containing the query parameters for the request.

        Returns:
            requests.Response: The response object returned by the API.
        """
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

    @cached_property
    def _chains(self) -> List[str]:
        """
        Retrieves a list of chain slugs

        Returns:
            List[str]: The list of chains slugs.
        """
        return list(
            {x["name"].lower() for x in self._get(ApiSectionsEnum.TVL, "v2", "chains")}
        )

    @cached_property
    def _protocols(self) -> List[str]:
        """Retrieves a list of protocols slugs.


        Returns:
            A list of strings representing the slugs of the protocols.

        """
        return list({x["slug"] for x in self._get(ApiSectionsEnum.TVL, "protocols")})

    @cached_property
    def _bridges(self) -> Dict[str, str]:
        """
        Retrieves a list of bridge slugs.

        Returns:
            List[str]: A list of bridge slugs.
        """
        return {
            int(x["id"]): x["name"]
            for x in self._get(ApiSectionsEnum.BRIDGES, "bridges")["bridges"]
        }

    @cached_property
    def _stablecoins(self) -> Dict[Any, Any]:
        """
        Returns a list of dictionaries representing stablecoins.

        Returns:
            Dict[Any, Any]: A list of dictionaries representing the
            stablecoins. Each dictionary contains the 'id' and 'symbol' of a stablecoin.
        """
        return {
            int(x["id"]): x["symbol"]
            for x in self._get(ApiSectionsEnum.STABLECOINS, "stablecoins")[
                "peggedAssets"
            ]
        }

    @cached_property
    def _pools(self) -> Dict[Any, Any]:
        """
        Returns a dictionary of pools where the keys are the pool IDs and the values are the corresponding symbols.

        Returns:
            Dict[Any, Any]: A dictionary of pools where the keys are the pool IDs and the values are the corresponding symbols.
        """
        return {
            x["pool"]: x["symbol"]
            for x in self._get(ApiSectionsEnum.YIELDS, "pools")["data"]
        }

    @cached_property
    def _dex_protocols(self) -> List[str]:
        """A cached property that returns a list of slugified dex protocol names.

        Returns:
            list: A list of slugified dex protocol names.
        """
        return [
            slugify(x["name"]) for x in self.get_dexes_volume_overview()["protocols"]
        ]

    @cached_property
    def _dex_chains(self) -> List[str]:
        """Retrieves the 'allChains' property from the result of the `get_dexes_volume_overview` method.

        Returns:
            The 'allChains' property from the result of the `get_dexes_volume_overview` method.
        """
        return [x.lower() for x in self.get_dexes_volume_overview()["allChains"]]

    @cached_property
    def _dex_options_protocols(self) -> List[str]:
        """Retrieves the 'options' property from the result of the `get_dexes_volume_overview` method.

        Returns:
            The 'options' property from the result of the `get_dexes_volume_overview` method.
        """
        return [
            slugify(x["name"]) for x in self.get_overview_dexes_options()["protocols"]
        ]

    @cached_property
    def _dex_options_chains(self) -> List[str]:
        """Retrieves the 'allChains' property from the result of the `get_overview_dexes_options` method.

        Returns:
            The 'allChains' property from the result of the `get_overview_dexes_options` method.
        """
        return [x.lower() for x in self.get_overview_dexes_options()["allChains"]]

    @cached_property
    def _fees_protocols(self) -> List[str]:
        """Retrieves the 'fees' property from the result of the `get_dexes_volume_overview` method.

        Returns:
            The 'fees' property from the result of the `get_dexes_volume_overview` method.
        """
        return [
            slugify(x["name"])
            for x in self.get_fees_and_revenues_for_all_protocols()["protocols"]
        ]

    @cached_property
    def _fees_chains(self) -> List[str]:
        """Retrieves the 'allChains' property from the result of the `get_fees_and_revenues_for_all_protocols` method.

        Returns:
            The 'allChains' property from the result of the `get_fees_and_revenues_for_all_protocols` method.
        """
        return [
            x.lower()
            for x in self.get_fees_and_revenues_for_all_protocols()["allChains"]
        ]

    def list_protocols(self) -> List[str]:
        """
        Returns a list of protocol slugs.

        Returns:
            List[str] A list of protocol slugs.
        """
        return self._protocols

    def list_chains(self) -> List[str]:
        """
        Returns a list of chains.

        Returns:
            List[str]: A list of chains.
        """
        return self._chains

    def list_bridges(self) -> Dict[int, str]:
        """
        Return a dictionary of bridges.

        Returns:
            Dict[in, str]: A dictionary of bridges.
        """
        return self._bridges

    def list_stablecoins(self) -> Dict[Any, Any]:
        """
        Return the dictionary of stablecoins.

        Returns:
            Dict[Any, Any]: The dictionary containing stablecoins.
        """
        return self._stablecoins

    def list_pools(self) -> Dict[UUIDstr, Any]:
        """Retrieves a list of pools and their symbols.

        Returns a dictionary of pools where the keys are the pool IDs and the values are the corresponding symbols.
        E.g. {'8997587d-a4aa-4441-95ce-4884f7f3c946': 'MATIC-WETH', ...}

        Returns:
            Dict[UUIDstr, Any]: The dictionary containing pools and their symbols.
        """

        return self._pools

    def list_dex_chains(self) -> List[str]:
        """
        Return the list of dex chains.

        Returns:
            List[str]: The list of dex chains.
        """
        return self._dex_chains

    def list_dex_protocols(self) -> List[str]:
        """
        Return the list of dex protocols.

        Returns:
            List[str]: The list of dex protocols.
        """
        return self._dex_protocols

    def list_options_protocols(self) -> List[str]:
        """
        Return the list of options protocols.

        Returns:
            List[str]: The list of options protocols.
        """
        return self._dex_options_protocols

    def list_options_chains(self) -> List[str]:
        """
        Return the list of options chains.

        Returns:
            List[str]: The list of options chains.
        """
        return self._dex_options_chains

    def list_fees_protocols(self) -> List[str]:
        """
        Return the list of fees protocols.

        Returns:
            List[str]: The list of fees protocols.
        """
        return self._fees_protocols

    def list_fees_chains(self) -> List[str]:
        """
        Return the list of fees chains.

        Returns:
            List[str]: The list of fees chains.
        """
        return self._fees_chains

    def get_coingecko_coin_ids(
        self, skip: int = 0, limit: int = None, from_gecko_api: bool = False
    ) -> List[str]:
        """Retrieves a list of CoinGecko coin IDs.

        Parameters:
            skip (int, optional): The number of CoinGecko coin IDs to skip. Defaults to 0.
            limit (int, optional): The maximum number of CoinGecko coin IDs to retrieve.
                Defaults to None. If None, retrieves all CoinGecko coin IDs.
            from_gecko_api (bool, optional): Whether to retrieve CoinGecko coin IDs from CoinGecko API
                or from local file. Defaults to False.

        Returns:
            A list of CoinGecko coin IDs.
        """
        if from_gecko_api:
            log.info("Retrieving CoinGecko coin IDs from CoinGecko API")
            coingecko_ids: List[str] = get_coingecko_coin_ids()
        else:
            log.info(
                "Retrieving CoinGecko coin IDs from file."
                "If you want to retrieve CoinGecko IDs from CoinGecko API, set `from_gecko_api=True`"
            )
            coingecko_ids: List[str] = read_coingecko_ids_from_file()
        return coingecko_ids[skip : skip + limit] if limit else coingecko_ids[skip:]

    def get_protocols(self) -> List[Dict[Any, Any]]:
        """Retrieves all protocols on Defi Llama along with their TVL.

        Returns:
            A list of dictionaries representing the protocols.
            Each dictionary contains key-value pairs representing the protocol information.

        Examples:
            >>> from defillama import DefiLlamaClient
            >>> client = DefiLlamaClient()
            >>> protocols = client.get_protocols()
            >>> print(protocols[0])
            {'id': '2269', 'name': 'Binance CEX', 'address': None, 'symbol': '-',
            'chain': 'Multi-Chain','gecko_id': None, ..., 'slug': 'binance-cex', ...}
        """
        return self._get(ApiSectionsEnum.TVL, "protocols")

    def get_protocol(self, protocol: str) -> Dict[Any, Any]:
        """Get historical TVL of a protocol and breakdowns by token and chain.

        Parameters:
            protocol (str): The protocol slug to retrieve.
            See available protocols by using client.list_protocols()

        Returns:
            The historical TVL of the protocol and breakdowns by token and chain.
        """
        validate_searched_entity(protocol.lower(), self._protocols, "protocol")
        return self._get(ApiSectionsEnum.TVL, "protocol", protocol)

    def get_historical_tvl_of_defi_on_all_chains(self) -> List[Dict[Any, Any]]:
        """Retrieves the historical total value locked (TVL) of decentralized finance (DeFi) on all chains.
        It excludes liquid staking and double counted tvl.

        Returns:
            A list of dictionaries representing the historical TVL data for each chain. Each dictionary contains
            the date and the corresponding TVL value.
        """
        return self._get(ApiSectionsEnum.TVL, "v2", "historicalChainTvl")

    def get_historical_tvl_for_chain(self, chain: str) -> List[Dict[Any, Any]]:
        """Returns the historical total value locked (TVL) for a specific chain.

        Parameters:
            chain (str): chain slug, you can get these from DefiLlamaClient.chains

        Returns:
            The historical TVL for the specified chain. The returned data is a list of dictionaries, where each
            dictionary contains the date and the corresponding TVL value.
        """

        validate_searched_entity(chain.lower(), self._chains, "chain")
        return self._get(ApiSectionsEnum.TVL, "v2", "historicalChainTvl", chain)

    def get_current_tvl_for_protocol(self, protocol: str) -> int:
        """
        Get the current total value locked (TVL) for a given protocol.

        Parameters:
            protocol (str): The protocol slug to retrieve.

        Returns:
            int: The current TVL for the specified protocol.
        """
        validate_searched_entity(protocol.lower(), self._protocols, "protocol")
        return self._get(ApiSectionsEnum.TVL, "tvl", protocol)

    def get_current_tvl_of_all_chains(self) -> List[Dict[Any, Any]]:
        """Get the current total value locked (TVL) of all chains.

        Returns:
            The current TVL for all chains. The returned data is a list of dictionaries,
            where each dictionary contains
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
        )["peggedAssets"]

    def get_current_stablecoins_market_cap(
        self,
    ) -> List[Dict[Any, Any]]:
        """
        Retrieves the current market capitalization of stablecoins on each chain.

        Returns:
            List[Dict[Any, Any]]: The current market capitalization of stablecoins on each chain.
        """
        return self._get(ApiSectionsEnum.STABLECOINS, "stablecoinchains")

    def get_stablecoin_historical_market_cap(
        self, stablecoin: Optional[Union[str, int]] = None
    ) -> List[Dict[Any, Any]]:
        """
        Retrieves the historical market capitalization data for a specific stablecoin.

        Parameters:
            stablecoin_id (int, str): The ID or name of the stablecoin.

        Returns:
            The historical market capitalization data for the specified stablecoin.
        """

        stablecoin = (
            get_stablecoin_id(stablecoin, self._stablecoins)
            if stablecoin
            else stablecoin
        )

        return self._get(
            ApiSectionsEnum.STABLECOINS,
            "stablecoincharts",
            "all",
            stablecoin=stablecoin,
        )

    def get_stablecoins_historical_martket_cap_in_chain(
        self,
        chain: str,
        stablecoin: Optional[Union[str, int]] = None,
    ) -> List[Dict[Any, Any]]:
        """
        Get the historical market cap and distribution of stablecoins in the specified blockchain.

        Params:
            chain (str): The name of the chain.
            stablecoin (Union[str, int]): The name or ID of the stablecoin.

        Raises:
            ValueError: If the chain is invalid or the stablecoin is not found.

        Returns:
            The historical market capitalization of the stablecoin.
        """

        validate_searched_entity(chain.lower(), self._chains, "chain")
        stablecoin_id = (
            get_stablecoin_id(stablecoin, self._stablecoins)
            if stablecoin
            else stablecoin
        )
        return self._get(
            ApiSectionsEnum.STABLECOINS,
            "stablecoincharts",
            chain,
            stablecoin=stablecoin_id,
        )

    def get_stablecoins_historical_market_cap_and_chain_distribution(
        self, stablecoin: Union[str, int]
    ) -> Dict[Any, Any]:
        """
        Get the historical market cap and chain distribution of a stablecoin.

        Parameters:
            stablecoin (Union[str, int]): The name or ID of the stablecoin.

        Returns:
            The historical market cap and chain distribution of the stablecoin.
        """
        stablecoin_id = get_stablecoin_id(stablecoin, self._stablecoins)
        return self._get(ApiSectionsEnum.STABLECOINS, "stablecoin", stablecoin_id)

    def get_stablecoins_historical_prices(self) -> List[Dict[Any, Any]]:
        """
        Retrieves the historical prices of stablecoins.

        Returns:
            A list of historical prices of stablecoins.
        """
        return self._get(ApiSectionsEnum.STABLECOINS, "stablecoinprices")

    def get_pools(self) -> List[Dict[Any, Any]]:
        """
        Retrieves the latest data for all pools, including enriched information
        such as predictions

        Returns:
            A list of dictionaries representing the pools.
        """
        return self._get(ApiSectionsEnum.YIELDS, "pools")["data"]

    def get_pool_historical_apy_and_tvl(
        self, pool: Union[str, UUIDstr]
    ) -> List[Dict[Any, Any]]:
        """
        Get the historical APY and TVL for a specific pool.

        Parameters:
            pool (str): The ID of the pool or Symbol.

        Returns:
            List[Dict[Any, Any]]: A list of dictionaries containing the historical APY and TVL data.

        Raises:
            ValueError: If the pool ID is invalid.

        Examples:
            >>> client.get_pool_historical_apy_and_tvl("WETH") # by pool symbol
            >>> client.get_pool_historical_apy_and_tvl("51d2f8d4-1fb5-4f6b-938b-e9cd17ca1ceb") # by pool id
        """
        try:
            uuid.UUID(pool)
        except ValueError as e:
            pool_id = next(
                (
                    k
                    for k, v in self._pools.items()
                    if v == pool or v.lower() == pool.lower()
                ),
                None,
            )
            if pool_id is None:
                raise ValueError(
                    f"Invalid pool: {pool}. To see available pools, use DefiLlamaClient().list_pools()"
                ) from e
        else:
            pool_id = pool

        return self._get(ApiSectionsEnum.YIELDS, "chart", pool_id)["data"]

    def get_bridges(self, include_chains: bool = True) -> List[Dict[Any, Any]]:
        """
        Retrieves a list of bridges from the API.

        Parameters:
            include_chains (bool, optional): Whether to include current previous day volume breakdown by chain. Defaults to True.

        Returns:
            List[Dict[Any, Any]]: A list of dictionaries representing the bridges.
        """
        return self._get(
            ApiSectionsEnum.BRIDGES, "bridges", includeChains=include_chains
        )["bridges"]

    def get_bridge(self, bridge: Union[str, int]) -> Dict[Any, Any]:
        """
        Get the summary od bridge volume and volume breakdown by chain.

        Parameters:
            bridge (Union[str, int]): The ID or name of the bridge.

        Returns:
            The summary od bridge volume and volume breakdown by chain.

        Raises:
            ValueError: If the provided bridge is invalid or not found in the available bridges.
        """
        bridge_id = get_bridge_id(bridge, self._bridges)
        return self._get(ApiSectionsEnum.BRIDGES, "bridge", bridge_id)

    def get_bridge_volume(
        self, chain: str, bridge: Union[str, int] = None
    ) -> List[Dict[Any, Any]]:
        """
        Retrieves the volume of a bridge in a specific chain.

        Parameters:
            chain (str): The name of the chain.
            bridge (Union[str, int]): The name or ID of the bridge.

        Raises:
            ValueError: If the specified chain is not valid or the bridge is not found.

        Returns:
            The volume of the bridge in the specified chain.
        """
        validate_searched_entity(chain, self._dex_chains, "chain")
        bridge_id = get_bridge_id(bridge, self._bridges) if bridge else None
        return self._get(ApiSectionsEnum.BRIDGES, "bridgevolume", chain, id=bridge_id)

    def get_bridge_day_stats(
        self, timestamp: int, chain: str, bridge: Optional[Union[str, int]] = None
    ) -> List[Dict[Any, Any]]:
        """
        Get the bridge day statistics for a specific timestamp, chain, and bridge.

        Parameters:
            timestamp (int): Unix timestamp. Data returned will be for the 24hr period starting at 00:00 UTC that the timestamp lands in.
            chain (str): The chain for which to retrieve the bridge day statistics.
            bridge (Union[str, int]): The bridge for which to retrieve the bridge day statistics.

        Returns:
            List[Dict[Any, Any]]: A list of dictionaries containing the bridge day statistics.

        Raises:
            ValueError: If an invalid chain is provided or the bridge is not found.
        """

        validate_searched_entity(chain, self._dex_chains, "chain")
        bridge_id = get_bridge_id(bridge, self._bridges) if bridge else None
        return self._get(
            ApiSectionsEnum.BRIDGES, "bridgedaystats", timestamp, chain, id=bridge_id
        )

    def get_bridge_transactions(
        self,
        bridge: Union[str, int],
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None,
        source_chain: Optional[str] = None,
        address: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[Any, Any]]:
        """
        Retrieves a list of bridge transactions based on the specified criteria.

        Parameters:
            bridge (Union[str, int]): The identifier or name of the bridge.
            start_timestamp (int, optional): The start timestamp for filtering transactions. Defaults to None.
            end_timestamp (int, optional): The end timestamp for filtering transactions. Defaults to None.
            source_chain (str, optional): The source chain for filtering transactions. Defaults to None.
            address (str, optional): Returns only transactions with specified address as "from" or "to".
                Addresses are queried in the form {chain}:{address}, where chain is an identifier
                such as ethereum, bsc, polygon, avax... .
            limit (int, optional): The maximum number of transactions to retrieve. Defaults to 10.

        Returns:
            List[Dict[Any, Any]]: A list of bridge transactions matching the specified criteria.
        """

        bridge_id = get_bridge_id(bridge, self._bridges)
        if source_chain:
            validate_searched_entity(source_chain, self._dex_chains, "chain")

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
        dataType: DexDataTypeEnum = "dailyVolume",
    ) -> Dict[Any, Any]:
        """
        List all DEXes with all summaries of their volumes and dataType history.

        Parameters:
            exclude_total_data_chart (bool, optional): Whether to exclude aggregated chart from response. Defaults to True.
            exclude_total_data_chart_breakdown (bool, optional): Whether to exclude broken down chart from response. Defaults to True.
            dataType (DexDataTypeEnum, optional): The type of data to retrieve. Defaults to DexDataTypeEnum.dailyVolume.
                Options: [DexDataTypeEnum.dailyVolume, DexDataTypeEnum.totalVolume]

        Returns:
            The overview of the volume data for DEXs.
        """
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
        dataType: DexDataTypeEnum = "dailyVolume",
    ) -> Dict[Any, Any]:
        """
        List all DEXes for a specific chain with all summaries of their volumes and dataType history.

        Parameters:
            chain (str): The chain for which to retrieve the volume overview.
            exclude_total_data_chart (bool, optional): Whether to exclude aggregated chart from response. Defaults to True.
            exclude_total_data_chart_breakdown (bool, optional): Whether to exclude broken down chart from response. Defaults to True.
            dataType (DexDataTypeEnum, optional): The type of data to retrieve. Defaults to DexDataTypeEnum.dailyVolume.
                Options: [DexDataTypeEnum.dailyVolume, DexDataTypeEnum.totalVolume]

        Raises:
            ValueError: If an invalid chain is provided.

        Returns:
            The volume overview for the specified chain from the DEXes API.
        """
        validate_searched_entity(chain, self._dex_chains, "chain")
        return self._get(
            ApiSectionsEnum.VOLUMES,
            "overview",
            "dexs",
            chain,
            excludeTotalDataChart=exclude_total_data_chart,
            excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
            dataType=dataType,
        )

    def get_summary_of_dex_volume_with_historical_data(
        self,
        protocol: str,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        dataType: DexDataTypeEnum = "dailyVolume",
    ) -> Dict[Any, Any]:
        """
        Get the summary of the DEX volume with historical data.

        Parameters:
            protocol (str): The protocol slug.
            exclude_total_data_chart (bool, optional): Whether to exclude aggregated chart from response. Defaults to True.
            exclude_total_data_chart_breakdown (bool, optional): Whether to exclude broken down chart from response. Defaults to True.
            dataType (DexDataTypeEnum, optional): The type of data to retrieve. Defaults to DexDataTypeEnum.dailyVolume.
                Options: [DexDataTypeEnum.dailyVolume, DexDataTypeEnum.totalVolume]

        Returns:
            The summary of the DEX volume with historical data.

        Raises:
            ValueError: If the protocol is invalid.
        """
        validate_searched_entity(protocol.lower(), self._dex_protocols, "dex protocol")

        return self._get(
            ApiSectionsEnum.VOLUMES,
            "summary",
            "dexs",
            protocol,
            excludeTotalDataChart=exclude_total_data_chart,
            excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
            dataType=dataType,
        )

    def get_overview_dexes_options(
        self,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        dataType: OptionsDataTypeEnum = "dailyPremiumVolume",
    ) -> Dict[Any, Any]:
        """
        List all options dexs along with summaries of their options and dataType history.

        Parameters:
            exclude_total_data_chart (bool, optional): Whether to exclude aggregated chart from response. Defaults to True.
            exclude_total_data_chart_breakdown (bool, optional): Whether to exclude broken down chart from response. Defaults to True.
            dataType (OptionsDataTypeEnum, optional): The type of data to retrieve. One of these:
                dailyPremiumVolume, dailyNotionalVolume, totalPremiumVolume, totalNotionalVolume.
                Defaults to OptionsDataTypeEnum.dailyPremiumVolume.

        Returns:
            Dict[Any, Any]: The options for the overview dexes.
        """
        return self._get(
            ApiSectionsEnum.VOLUMES,
            "overview",
            "options",
            excludeTotalDataChart=exclude_total_data_chart,
            excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
            dataType=dataType,
        )

    def get_overview_dexes_options_for_chain(
        self,
        chain: str,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        dataType: OptionsDataTypeEnum = "dailyPremiumVolume",
    ):
        """
        List all options dexs along with summaries of their options and dataType history for specific chain.

        Parameters:
            chain (str, optional): The chain for which to retrieve the volume overview.
            exclude_total_data_chart (bool, optional): Whether to exclude aggregated chart from response. Defaults to True.
            exclude_total_data_chart_breakdown (bool, optional): Whether to exclude broken down chart from response. Defaults to True.
            dataType (OptionsDataTypeEnum, optional): The type of data to retrieve. One of these:
                dailyPremiumVolume, dailyNotionalVolume, totalPremiumVolume, totalNotionalVolume.
                Defaults to OptionsDataTypeEnum.dailyPremiumVolume.

        Returns:
            Dict[Any, Any]: The options for the overview dexes.
        """
        validate_searched_entity(chain, self._dex_options_chains, "chain")
        return self._get(
            ApiSectionsEnum.VOLUMES,
            "overview",
            "options",
            chain,
            excludeTotalDataChart=exclude_total_data_chart,
            excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
            dataType=dataType,
        )

    def get_summary_of_options_volume_with_historical_data_for_protocol(
        self,
        protocol: str,
        dataType: OptionsDataTypeEnum = "dailyPremiumVolume",
    ):
        """
        Retrieves the summary of options volume with historical data for a given protocol.
        To list available options protocols use: DefiLlamaClient().list_options_protocols()

        Parameters:
            protocol (str): The protocol for which to retrieve the volume data.
            dataType (OptionsDataTypeEnum, optional): The type of data to retrieve. One of these:
                dailyPremiumVolume, dailyNotionalVolume, totalPremiumVolume, totalNotionalVolume.
                Defaults to OptionsDataTypeEnum.dailyPremiumVolume.

        Returns:
            The summary of options volume data for the specified protocol and data type.
        """
        validate_searched_entity(
            protocol.lower(), self._dex_options_protocols, "protocol"
        )

        return self._get(
            ApiSectionsEnum.VOLUMES, "summary", "options", protocol, dataType=dataType
        )

    def get_fees_and_revenues_for_all_protocols(
        self,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        dataType: FeesDataTypeEnum = "dailyFees",
    ) -> Dict[Any, Any]:
        """
        Retrieves the fees and revenues for all protocols.

        Parameters:
            exclude_total_data_chart (bool, optional): Whether to exclude the total data chart. Defaults to True.
            exclude_total_data_chart_breakdown (bool, optional): Whether to exclude the breakdown of the total data chart. Defaults to True.
            dataType (FeesDataTypeEnum, optional): The type of fees data to retrieve. One of these:
                FeesDataTypeEnum.dailyFees, FeesDataTypeEnum.totalFees, FeesDataTypeEnum.dailyRevenue, FeesDataTypeEnum.totalRevenue
        Returns:
            The fees and revenues data for all protocols.
        """
        return self._get(
            ApiSectionsEnum.FEES,
            "overview",
            "fees",
            excludeTotalDataChart=exclude_total_data_chart,
            excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
            dataType=dataType,
        )

    def get_fees_and_revenues_for_all_protocols_for_chain(
        self,
        chain: str,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        dataType: FeesDataTypeEnum = "dailyFees",
    ) -> Dict[Any, Any]:
        """
        Retrieves fees and revenues for all protocols for a given chain.

        Parameters:
            chain (str): The chain for which to retrieve the fees and revenues.
            exclude_total_data_chart (bool, optional): Whether to exclude the total data chart. Defaults to True.
            exclude_total_data_chart_breakdown (bool, optional): Whether to exclude the breakdown of the total data chart. Defaults to True.
            dataType (FeesDataTypeEnum, optional): The type of fees data to retrieve. One of these:
                FeesDataTypeEnum.dailyFees, FeesDataTypeEnum.totalFees, FeesDataTypeEnum.dailyRevenue, FeesDataTypeEnum.totalRevenue

        Raises:
            ValueError: If an invalid chain is provided.

        Returns:
            The fees and revenues data for all protocols on the given chain.
        """
        validate_searched_entity(chain.lower(), self._fees_chains, "chain")

        return self._get(
            ApiSectionsEnum.FEES,
            "overview",
            "fees",
            chain,
            excludeTotalDataChart=exclude_total_data_chart,
            excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
            dataType=dataType,
        )

    def get_summary_of_protocols_fees_and_revenue(
        self,
        protocol: str,
        dataType: FeesDataTypeEnum = "dailyFees",
    ) -> Dict[Any, Any]:
        """
        Retrieves the summary of fees and revenue for a specific protocol.

        Parameters:
            protocol (str): The name of the protocol.
            dataType (FeesDataTypeEnum, optional): The type of fees data to retrieve. One of these:
                FeesDataTypeEnum.dailyFees, FeesDataTypeEnum.totalFees, FeesDataTypeEnum.dailyRevenue, FeesDataTypeEnum.totalRevenue

        Raises:
            ValueError: If the protocol is invalid.

        Returns:
            dict: The summary of fees and revenue for the specified protocol.
        """
        validate_searched_entity(protocol.lower(), self._fees_protocols, "protocol")
        return self._get(
            ApiSectionsEnum.FEES, "summary", "fees", protocol, dataType=dataType
        )

    def get_current_prices_of_tokens_by_contract_address(
        self,
        coins: Union[str, Coin, Dict[str, str], List[Coin], List[Dict[str, str]]],
        search_width: Optional[str] = None,
    ):
        """
        Retrieves the current prices of tokens by contract address.

        To see all available chains use `client.list_chains()`
        To see all available coingecko ids use `client.get_coingecko_coin_ids()`

        You can use coingecko as a chain, and then use coin gecko ids instead of contract addresses:
            >>> coins = "coingecko:uniswap,coingecko:ethereum"
            >>> coins = Coin("coingecko:uniswap")
            >>> coins = {"chain": "coingecko", "address": "uniswap"}

        Parameters:
            coins (Union[str, Coin, Dict[str, str], List[Coin], List[Dict[str, str]]]): The tokens to retrieve prices for.
                Can be a Coin, a Dict, a list of Coin objects or dictionaries containing token details,
                or a string with coma separated tokens in format chain:address
            search_width (str, optional): Time range on either side to find price data, defaults to 6 hours.
                Can use regular chart candle notion like 4h etc where:
                W = week, D = day, H = hour, M = minute (not case sensitive)
        Returns:
            The current prices of the tokens specified.

        Examples:
            >>> client.get_current_prices_of_tokens_by_contract_address(
                "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,coingecko:ethereum"
                )
            >>> client.get_current_prices_of_tokens_by_contract_address([
                    {"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"},
                    {"chain": "coingecko","address": "uniswap"},
                ])
            >>> client.get_current_prices_of_tokens_by_contract_address([
                Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"),
                Coin("bsc", "0x762539b45a1dcce3d36d080f74d1aed37844b878")
                ])
        """

        coins_to_search = prepare_coins_for_request(coins)
        return self._get(
            ApiSectionsEnum.COINS,
            "prices",
            "current",
            coins_to_search,
            searchWidth=search_width,
        )

    def get_historical_prices_of_tokens_by_contract_address(
        self,
        coins: Union[str, Coin, Dict[str, str], List[Coin], List[Dict[str, str]]],
        timestamp: int,
        search_width: Optional[str] = None,
    ):
        """
        Retrieves the historical prices of tokens by contract address.

        To see all available chains use `client.list_chains()`
        To see all available coingecko ids use `client.get_coingecko_coin_ids()`

        You can use coingecko as a chain, and then use coin gecko ids instead of contract addresses:
            >>> coins = "coingecko:uniswap,coingecko:ethereum"
            >>> coins = Coin("coingecko:uniswap")
            >>> coins = {"chain": "coingecko", "address": "uniswap"}

        Parameters:
            coins (Union[str, Coin, Dict[str, str], List[Coin], List[Dict[str, str]]]): The tokens to retrieve prices for.
                Can be a Coin, a Dict, a list of Coin objects or dictionaries containing token details,
                or a string with coma separated tokens in format chain:address
            timestamp (int, optional): The timestamp to retrieve prices for.
            search_width (str, optional): Time range on either side to find price data, defaults to 6 hours.
                Can use regular chart candle notion like 4h etc where:
                W = week, D = day, H = hour, M = minute (not case sensitive)
        Returns:
            The historical prices of the tokens specified.

        Examples:
            >>> client.get_historical_prices_of_tokens_by_contract_address(
                "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,coingecko:ethereum"
                , timestamp=1650000000)
            >>> client.get_historical_prices_of_tokens_by_contract_address([
                    {"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"},
                    {"chain": "coingecko","address": "uniswap"},
                ], timestamp=1650000000)
            >>> client.get_historical_prices_of_tokens_by_contract_address([
                Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"),
                Coin("bsc", "0x762539b45a1dcce3d36d080f74d1aed37844b878")
                ], timestamp=1650000000)
        """

        coins_to_search = prepare_coins_for_request(coins)
        return self._get(
            ApiSectionsEnum.COINS,
            "prices",
            "historical",
            timestamp,
            coins_to_search,
            searchWidth=search_width,
        )

    def get_token_prices_candle(
        self,
        coins: Union[str, Coin, Dict[str, str], List[Coin], List[Dict[str, str]]],
        start: Optional[int] = None,
        end: Optional[int] = None,
        span: Optional[int] = None,
        period: Optional[str] = None,
        search_width: Optional[str] = None,
    ):
        """
        Retrieves token prices at regular time intervals.

        To see all available chains use `client.list_chains()`
        To see all available coingecko ids use `client.get_coingecko_coin_ids()`

        You can use coingecko as a chain, and then use coin gecko ids instead of contract addresses:
            >>> coins = "coingecko:uniswap,coingecko:ethereum"
            >>> coins = Coin("coingecko:uniswap")
            >>> coins = {"chain": "coingecko", "address": "uniswap"}

        Parameters:
            coins (Union[str, Coin, Dict[str, str], List[Coin], List[Dict[str, str]]]): The tokens to retrieve prices for.
                Can be a Coin, a Dict, a list of Coin objects or dictionaries containing token details,
                or a string with coma separated tokens in format chain:address
            start (int, optional): The start timestamp to retrieve prices for. Defaults to None.
            end (int, optional): The end timestamp to retrieve prices for. Defaults to None.
            span (int, optional): Number of data points returned, defaults to 0
            period (str, optional): Duration between data points, defaults to 24 hours
            search_width (str, optional): Time range on either side to find price data, defaults to 6 hours.
                Can use regular chart candle notion like 4h etc where:
                W = week, D = day, H = hour, M = minute (not case sensitive)
        Returns:
            The token prices at regular time intervals.

        Examples:
            >>> client.get_token_prices_candle(
                "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,coingecko:ethereum"
                )
            >>> client.get_token_prices_candle([
                    {"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"},
                    {"chain": "coingecko","address": "uniswap"},
                ])
            >>> client.get_token_prices_candle([
                Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"),
                Coin("bsc", "0x762539b45a1dcce3d36d080f74d1aed37844b878")
                ])
        """

        start = get_previous_timestamp(start) if start else None
        coins_to_search = prepare_coins_for_request(coins)
        return self._get(
            ApiSectionsEnum.COINS,
            "chart",
            coins_to_search,
            start=start,
            end=end,
            span=span,
            period=period,
            searchWidth=search_width,
        )

    def get_percentage_change_in_coin_price(
        self,
        coins: Union[str, Coin, Dict[str, str], List[Coin], List[Dict[str, str]]],
        timestamp: Optional[int] = None,
        look_forward: bool = False,
        period: str = "24h",
    ):
        """
        Retrieves token price percentage change over time.

        To see all available chains use `client.list_chains()`
        To see all available coingecko ids use `client.get_coingecko_coin_ids()`

        You can use coingecko as a chain, and then use coin gecko ids instead of contract addresses:
            >>> coins = "coingecko:uniswap,coingecko:ethereum"
            >>> coins = Coin("coingecko:uniswap")
            >>> coins = {"chain": "coingecko", "address": "uniswap"}

        Parameters:
            coins (Union[str, Coin, Dict[str, str], List[Coin], List[Dict[str, str]]]): The tokens to retrieve prices for.
                Can be a Coin, a Dict, a list of Coin objects or dictionaries containing token details,
                or a string with coma separated tokens in format chain:address
            timestamp (int, optional): The start timestamp to retrieve prices for. Defaults to time now
            look_forward (bool, optional): Whether you want the duration after your given timestamp or not,
                defaults to false (looking back)
            period (str, optional): Duration between data points, defaults to 24 hours

        Returns:
            The token price percentage change over time.

        Examples:
            >>> client.get_percentage_change_in_coin_price(
                "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,coingecko:ethereum"
                )
            >>> client.get_percentage_change_in_coin_price([
                    {"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"},
                    {"chain": "coingecko","address": "uniswap"},
                ])
            >>> client.get_percentage_change_in_coin_price([
                Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"),
                Coin("bsc", "0x762539b45a1dcce3d36d080f74d1aed37844b878")
                ])
        """

        coins_to_search = prepare_coins_for_request(coins)
        return self._get(
            ApiSectionsEnum.COINS,
            "percentage",
            coins_to_search,
            timestamp=timestamp,
            lookForward=look_forward,
            period=period,
        )

    def get_earliest_timestamp_price_record_for_coins(
        self,
        coins: Union[str, Coin, Dict[str, str], List[Coin], List[Dict[str, str]]],
    ):
        """
        Get the earliest timestamped price record for the given coins.

        To see all available chains use `client.list_chains()`
        To see all available coingecko ids use `client.get_coingecko_coin_ids()`

        You can use coingecko as a chain, and then use coin gecko ids instead of contract addresses:
            >>> coins = "coingecko:uniswap,coingecko:ethereum"
            >>> coins = Coin("coingecko:uniswap")
            >>> coins = {"chain": "coingecko", "address": "uniswap"}

        Parameters:
            coins (Union[str, Coin, Dict[str, str], List[Coin], List[Dict[str, str]]]): The tokens to retrieve prices for.
                Can be a Coin, a Dict, a list of Coin objects or dictionaries containing token details,
                or a string with coma separated tokens in format chain:address

        Returns:
            The earliest timestamped price record for the given coins.

        Examples:
            >>> client.get_earliest_timestamp_price_record_for_coins(
                    "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,coingecko:ethereum"
                )
            >>> client.get_earliest_timestamp_price_record_for_coins([
                    {"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"},
                    {"chain": "coingecko","address": "uniswap"}
                ])
            >>> client.get_earliest_timestamp_price_record_for_coins([
                Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"),
                Coin("bsc", "0x762539b45a1dcce3d36d080f74d1aed37844b878")
                ])
        """
        return self._get(ApiSectionsEnum.COINS, "prices", "first", coins)

    def get_the_closest_block_to_timestamp(
        self, chain: str, timestamp: int
    ) -> Dict[str, Any]:
        """
        Get the closest block to the given timestamp for a specific chain.

        Parameters:
            chain (str): Chain which you want to get the block from
            timestamp (int): UNIX timestamp of the block you are searching for

        Raises:
            ValueError: If the chain is not valid.

        Returns:
            The closest block to the given timestamp for the specified chain.
        """
        validate_searched_entity(chain, self._chains, "chain")
        return self._get(ApiSectionsEnum.COINS, "block", chain, timestamp)
