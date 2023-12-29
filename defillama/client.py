import datetime
import enum
from functools import cached_property, lru_cache
import json
from typing import Any, Dict, List, Union
import uuid
import requests
import pprint
from exc import InvalidResponseDataException, InvalidResponseStatusCodeException
from utils import get_retry_session
from log import get_logger
from slugify import slugify

log = get_logger(__name__)


class ApiSectionsEnum(str, enum.Enum):
    TVL = "tvl"
    COINS = "coins"
    STABLECOINS = "stablecoins"
    YIELDS = "yields"
    BRIDGES = "bridges"
    VOLUMES = "volumes"
    FEES = "fees"


class DataTypeEnum(str, enum.Enum):
    dailyVolume = "dailyVolume"
    totalVolume = "totalVolume"


class OptionsDataTypeEnum(str, enum.Enum):
    dailyPremiumVolume = "dailyPremiumVolume"
    totalPremiumVolume = "totalPremiumVolume"
    dailyNotionalVolume = "dailyNotionalVolume"
    totalNotionalVolume = "totalNotionalVolume"


class FeesDataTypeEnum(str, enum.Enum):
    dailyFees = "dailyFees"
    totalFees = "totalFees"
    dailyRevenue = "dailyRevenue"
    totalRevenue = "totalRevenue"


class DefiLlamaClient:
    def __init__(self, **kwargs) -> None:
        self._urls = {
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

        if section not in self._urls.keys():
            raise ValueError(f"Invalid section: {section}")
        return self._urls[section]

    def _build_endpoint_url(
        self, section: ApiSectionsEnum, endpoint: str, *args
    ) -> str:
        """
        Builds and returns the endpoint URL for the given API section, endpoint, and optional arguments.

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
    def chains(self) -> List[str]:
        """
        Retrieves a list of chain slugs

        Returns:
            List[str]: The list of chains slugs.
        """
        return list({x['name'] for x in self._get(ApiSectionsEnum.TVL, "v2", "chains")})
    
    @cached_property
    def protocols(self) -> List[str]:
        """Retrieves a list of protocols slugs. 


        Returns:
            A list of strings representing the slugs of the protocols.

        """
        return list({x['slug'] for x in self._get(ApiSectionsEnum.TVL, "protocols")})
    
    @cached_property
    def bridges(self) -> Dict[str, str]:
        """
        Retrieves a list of bridge slugs.

        Returns:
            List[str]: A list of bridge slugs.
        """
        return {int(x['id']) : x['name'] for x in self._get(ApiSectionsEnum.BRIDGES, "bridges")['bridges']}
    
    @cached_property
    def stablecoins(self) -> Dict[Any, Any]:
        """
        Returns a list of dictionaries representing stablecoins.

        Returns:
            Dict[Any, Any]: A list of dictionaries representing the 
            stablecoins. Each dictionary contains the 'id' and 'symbol' of a stablecoin.
        """
        return {int(x['id']) : x['symbol'] for x in self._get(ApiSectionsEnum.STABLECOINS, "stablecoins")['peggedAssets']}
    @cached_property
    def pools(self) -> Dict[Any, Any]:
        """
        Returns a dictionary of pools where the keys are the pool IDs and the values are the corresponding symbols.
        
        Returns:
            Dict[Any, Any]: A dictionary of pools where the keys are the pool IDs and the values are the corresponding symbols.
        """
        return {x['pool']: x['symbol'] for x in self._get(ApiSectionsEnum.YIELDS, "pools")['data']}
    
    def get_protocols(self) -> List[Dict[Any, Any]]:
        """Retrieves all protocols on Defi Llama along with their TVL.

        Returns:
            A list of dictionaries representing the protocols. 
            Each dictionary contains key-value pairs representing the protocol information.
        """

        return self._get(ApiSectionsEnum.TVL, "protocols")

    def get_protocol(self, protocol: str) -> Dict[Any, Any]:
        """Get historical TVL of a protocol and breakdowns by token and chain.

        Parameters:
            protocol (str): The protocol slug to retrieve. See available protocols by using DefiLlamaClient.protocols

        Returns:
            The historical TVL of the protocol and breakdowns by token and chain.
        """
        if protocol not in self.protocols:
            raise ValueError(f"Invalid protocol: {protocol}. Available protocols: {self.protocols}")
        return self._get(ApiSectionsEnum.TVL, "protocol", protocol)


    def get_historical_tvl_of_defi_on_all_chains(self) -> List[Dict[Any, Any]]:
        """Retrieves the historical total value locked (TVL) of decentralized finance (DeFi) on all chains.
        It excludes liquid staking and double counted tvl.

        Returns:
            A list of dictionaries representing the historical TVL data for each chain. Each dictionary contains
            the date and the corresponding TVL value.
            
        Response:
            [{'date': 1530230400, 'tvl': 20541.94079040033}, {'date': 1530316800, 'tvl': 20614.458266145004}]
        """
        return self._get(ApiSectionsEnum.TVL, "v2", "historicalChainTvl")

    def get_historical_tvl_for_chain(self, chain: str) -> List[Dict[Any, Any]]:
        """Returns the historical total value locked (TVL) for a specific chain.

        Parameters:
            chain (str): chain slug, you can get these from DefiLlamaClient.chains

        Returns:
            The historical TVL for the specified chain. The returned data is a list of dictionaries, where each
            dictionary contains the date and the corresponding TVL value.
            
        Response:
            [{'date': 1626220800, 'tvl': 68353955.52897093}, {'date': 1626307200, 'tvl': 62829548.17372862}]
        """
        if chain not in self.chains:
            raise ValueError(f"Invalid chain: {chain}. Available chains: {self.chains}")

        return self._get(ApiSectionsEnum.TVL, "v2", "historicalChainTvl", chain)

    def get_current_tvl_for_protocol(self, protocol: str) -> int:
        """
        Get the current total value locked (TVL) for a given protocol.

        Parameters:
            protocol (str): The protocol slug to retrieve.

        Returns:
            int: The current TVL for the specified protocol.
        """
        if protocol not in self.protocols:
            raise ValueError(f"Invalid protocol: {protocol}. Available protocols: {self.protocols}")
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
        )['peggedAssets']

    def get_current_stablecoins_market_cap(
        self,
    ) -> List[Dict[Any, Any]]:
        """
        Retrieves the current market capitalization of stablecoins on each chain.
        
        Returns:
            The current market capitalization of stablecoins on each chain.
            
        """
        return self._get(ApiSectionsEnum.STABLECOINS, "stablecoinchains")
    
    def _get_stablecoin_id(self, stablecoin: Union[str, int]) -> int:
        if isinstance(stablecoin, str) and not stablecoin.isnumeric():
            stablecoin_id = next((k for k, v in self.stablecoins.items() if v == stablecoin), None)
            if stablecoin_id is None:
                raise ValueError(f"Invalid stablecoin: {stablecoin}. Available stablecoins: {self.stablecoins}")
        elif isinstance(stablecoin, int):
            stablecoin_id = stablecoin
        elif isinstance(stablecoin, str):
            stablecoin_id = int(stablecoin)
        else:
            raise ValueError("Invalid stablecoin")

        if stablecoin_id not in self.stablecoins:
            raise ValueError(f"Invalid stablecoin: {stablecoin}. Available stablecoins: {self.stablecoins}")
        
        return stablecoin_id

    def _get_bridge_id(self, bridge: Union[str, int]) -> int:
        if isinstance(bridge, str) and not bridge.isnumeric():
            bridge_id = next((k for k, v in self.bridges.items() if v == bridge), None)
            if bridge_id is None:
                raise ValueError(f"Invalid bridge: {bridge}. Available bridges: {self.bridges}")
        else:
            bridge_id = int(bridge)
        
        if bridge_id not in self.bridges:
            raise ValueError(f"Invalid bridge: {bridge}. Available bridges: {self.bridges}")
        return bridge_id

    def get_stablecoins_historical_market_cap(self, stablecoin: Union[str, int]) -> List[Dict[Any, Any]]:
        """
        Retrieves the historical market capitalization data for a specific stablecoin.

        Parameters:
            stablecoin_id (int, str): The ID or name of the stablecoin.

        Returns:
            The historical market capitalization data for the specified stablecoin.
        """
        
        return self._get(
            ApiSectionsEnum.STABLECOINS,
            "stablecoincharts",
            "all",
            stablecoin=self._get_stablecoin_id(stablecoin),
        )

    def get_stablecoins_historical_martket_cap_in_chain(
        self, chain: str, stablecoin: Union[str, int],
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

        if chain not in self.chains:
            raise ValueError(f"Invalid chain: {chain}. Available chains: {self.chains}")
        
        stablecoin_id = self._get_stablecoin_id(stablecoin)
        
        return self._get(
            ApiSectionsEnum.STABLECOINS,
            "stablecoincharts",
            chain,
            stablecoin=stablecoin_id,
        )

    def get_stablecoins_historical_market_cap_and_chain_distribution(
        self, stablecoin: Union[str, int]
    ) -> List[Dict[Any, Any]]:
        """
        Get the historical market cap and chain distribution of a stablecoin.

        Parameters:
            stablecoin (Union[str, int]): The name or ID of the stablecoin.

        Returns:
            The historical market cap and chain distribution of the stablecoin.
        """
        stablecoin_id = self._get_stablecoin_id(stablecoin)
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
        return self._get(ApiSectionsEnum.YIELDS, "pools")['data']

    def get_pool_historical_apy_and_tvl(self, pool: str) -> List[Dict[Any, Any]]:
        """
        Get the historical APY and TVL for a specific pool.

        Args:
            pool (str): The ID of the pool or Symbol.

        Returns:
            List[Dict[Any, Any]]: A list of dictionaries containing the historical APY and TVL data.

        Raises:
            ValueError: If the pool ID is invalid.
        """
        try:
            uuid.UUID(pool)
        except ValueError:
            log.debug(f"Invalid pool id: {pool}")
            pool_id = next((k for k, v in self.pools.items() if v == pool), None)
            if pool_id is None:
                raise ValueError(f"Invalid pool: {pool}. To see available pools, use DefiLlamaClient().pools")
        else:
            pool_id = pool
            
        return self._get(ApiSectionsEnum.YIELDS, "chart", pool_id)

    def get_bridges(self, include_chains: bool = True) -> List[Dict[Any, Any]]:
        """
        Retrieves a list of bridges from the API.

        Params:
            include_chains (bool, optional): Whether to include current previous day volume breakdown by chain. Defaults to True.
            

        Returns:
            List[Dict[Any, Any]]: A list of dictionaries representing the bridges.
        """
        return self._get(
            ApiSectionsEnum.BRIDGES, "bridges", includeChains=include_chains
        )['bridges']
        

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
        return self._get(ApiSectionsEnum.BRIDGES, "bridge", self._get_bridge_id(bridge))
    

    def get_bridge_volume(self, chain: str, bridge: Union[str, int] = None) -> List[Dict[Any, Any]]:
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
        if chain not in self.chains:
            raise ValueError(f"Invalid chain: {chain}. Available chains: {self.chains}")
        
        if bridge is not None:
            try:
                bridge_id = self._get_bridge_id(bridge)
            except ValueError:
                log.warning(f"Bridge not found: {bridge}. Setting bridge_id to None.")
                bridge_id = None
        return self._get(ApiSectionsEnum.BRIDGES, "bridgevolume", chain, id=bridge_id)

    def get_bridge_day_stats(self, timestamp: int, chain: str, bridge: Union[str, int] = None) -> List[Dict[Any, Any]]:
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
        
        if chain not in self.chains:
            raise ValueError(f"Invalid chain: {chain}. Available chains: {self.chains}")
        
        if bridge is not None:
            try:
                bridge_id = self._get_bridge_id(bridge)
            except ValueError:
                log.warning(f"Bridge not found: {bridge}. Setting bridge_id to None.")
                bridge_id = None
        return self._get(
            ApiSectionsEnum.BRIDGES, "bridgedaystats", timestamp, chain, id=bridge_id
        )

    def get_bridge_transactions(
        self,
        bridge: Union[str, int],
        start_timestamp: int = None,
        end_timestamp: int = None,
        source_chain: str = None,
        address: str = None,
        limit: int = 200,
    ) -> List[Dict[Any, Any]]:
        """
        Retrieves a list of bridge transactions based on the specified criteria.

        Parameters:
            bridge (Union[str, int]): The identifier or name of the bridge.
            start_timestamp (int, optional): The start timestamp for filtering transactions. Defaults to None.
            end_timestamp (int, optional): The end timestamp for filtering transactions. Defaults to None.
            source_chain (str, optional): The source chain for filtering transactions. Defaults to None.
            address (str, optional): Returns only transactions with specified address as "from" or "to". 
                Addresses are quried in the form {chain}:{address}, where chain is an identifier such as ethereum, bsc,
                polygon, avax... .
            limit (int, optional): The maximum number of transactions to retrieve. Defaults to 200.

        Returns:
            List[Dict[Any, Any]]: A list of bridge transactions matching the specified criteria.
        """
        
        bridge_id = self._get_bridge_id(bridge)
        
        if source_chain and source_chain not in self.chains:
            source_chain = None 
            log.warning("Source chain not found. Setting source chain to None.")      
        
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
        dataType: DataTypeEnum = DataTypeEnum.dailyVolume,
    ) -> Dict[Any, Any]:
        """
        List all DEXes with all summaries of their volumes and dataType history.

        Parameters:
            exclude_total_data_chart (bool, optional): Whether to exclude aggregated chart from response. Defaults to True.
            exclude_total_data_chart_breakdown (bool, optional): Whether to exclude broken down chart from response. Defaults to True.
            dataType (DataTypeEnum, optional): The type of data to retrieve. Defaults to DataTypeEnum.dailyVolume. Options: [DataTypeEnum.dailyVolume, DataTypeEnum.totalVolume]

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
        dataType: DataTypeEnum = DataTypeEnum.dailyVolume,
    ):
        """
        List all DEXes for a specific chain with all summaries of their volumes and dataType history.

        Parameters:
            chain (str): The chain for which to retrieve the volume overview.
            exclude_total_data_chart (bool, optional): Whether to exclude aggregated chart from response. Defaults to True.
            exclude_total_data_chart_breakdown (bool, optional): Whether to exclude broken down chart from response. Defaults to True.
            dataType (DataTypeEnum, optional): The type of data to retrieve. Defaults to DataTypeEnum.dailyVolume. Options: [DataTypeEnum.dailyVolume, DataTypeEnum.totalVolume]

        Raises:
            ValueError: If an invalid chain is provided.

        Returns:
            The volume overview for the specified chain from the DEXes API.
        """
        if chain not in self.dex_chains:
            raise ValueError(f"Invalid chain: {chain}. Available chains: {self.dex_chains}")
        return self._get(
            ApiSectionsEnum.VOLUMES,
            "overview",
            "dexs",
            chain,
            excludeTotalDataChart=exclude_total_data_chart,
            excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
            dataType=dataType,
        )
        
    @cached_property
    def dex_protocols(self):
        return [slugify(x['name']) for x in self.get_dexes_volume_overview()['protocols']]
    
    @cached_property
    def dex_chains(self):
        return self.get_dexes_volume_overview()['allChains']

    def get_summary_of_dex_volume_with_historical_data(
        self,
        protocol: str,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        dataType: DataTypeEnum = DataTypeEnum.dailyVolume,
    ):
        if protocol not in self.dex_protocols:
            raise ValueError(f"Invalid protocol: {protocol}. Available protocols: {self.dex_protocols}")
        
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
        dataType: OptionsDataTypeEnum = OptionsDataTypeEnum.dailyPremiumVolume,
    ):
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
        chain: str = "ethereum",
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        dataType: OptionsDataTypeEnum = OptionsDataTypeEnum.dailyPremiumVolume,
    ):
        return self._get(
            ApiSectionsEnum.VOLUMES,
            "overview",
            "options",
            chain,
            excludeTotalDataChart=exclude_total_data_chart,
            excludeTotalDataChartBreakdown=exclude_total_data_chart_breakdown,
            dataType=dataType,
        )

    def get_summary_of_options_volume_with_historical_data(
        self,
        protocol: str = "lyra",
        dataType: OptionsDataTypeEnum = OptionsDataTypeEnum.dailyPremiumVolume,
    ):
        return self._get(
            ApiSectionsEnum.VOLUMES, "summary", "options", protocol, dataType=dataType
        )

    def get_fees_and_revenues_for_all_protocols(
        self,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        dataType: FeesDataTypeEnum = FeesDataTypeEnum.dailyFees,
    ):
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
        chain: str = "ethereum",
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        dataType: FeesDataTypeEnum = FeesDataTypeEnum.dailyFees,
    ):
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
        protocol: str = "lyra",
        dataType: FeesDataTypeEnum = FeesDataTypeEnum.dailyFees,
    ):
        return self._get(
            ApiSectionsEnum.FEES, "summary", "fees", protocol, dataType=dataType
        )

    def get_current_prices_of_tokens_by_contract_address(
        self,
        coins: str = "ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1,coingecko:ethereum,bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878,ethereum:0xdB25f211AB05b1c97D595516F45794528a807ad8",
        search_width: str = "6h",
    ):
        """
        The goal of this API is to price as many tokens as possible, including exotic ones that never get traded, which makes them impossible to price by looking at markets.

        The base of our data are prices pulled from coingecko, which is then extended through multiple means:

        We price all bridged tokens by using the price of the token in it's original chain, so we fetch all bridged versions of USDC on arbitrum, fantom, avax... and price all them using the price for the token on Ethereum, which we know. Right now we support 10 different bridging protocols.

        We have multiple adapters to price specialized sets of tokens by running custom code:

        We price yearn's yToken LPs by checking how much underlying token can be withdrawn for each LP

        Aave, compound and euler LP tokens are also priced based on their relationship against underlying tokens

        Uniswap, curve, balancer and stargate LPs are priced using the underlying tokens in each pair

        GMX's GLP token is priced based on the value of tokens given on withdrawal (which includes calculations based on trader's PnL)

        Synthetix tokens are priced using forex prices of the coin they are pegged to

        For tokens that we haven't been able to price in any other way, we find the pool with most liquidity for each on uniswap, curve and serum and then use the prices provided on those exchanges.

        Unlike all the other tokens, we can't confirm that these prices are correct, so we only ingest the ones that have sufficient liquidity and, even in that case, we attach a confidence value to them that is related to the depth of liquidity and which represents our confidence in the quality of each price. API consumers can choose to filter out prices with low confidence values.

        Our API server is fully open source and we are constantly adding more pricing adapters, extending the amount of tokens we support.

        Tokens are queried using {chain}:{address}, where chain is an identifier such as ethereum, bsc, polygon, avax... You can also get tokens by coingecko id by setting coingecko as the chain, eg: coingecko:ethereum, coingecko:bitcoin. Examples:

        ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1
        bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878
        coingecko:ethereum
        arbitrum:0x4277f8f2c384827b5273592ff7cebd9f2c1ac258
        """

        return self._get(
            ApiSectionsEnum.COINS, "prices", "current", coins, searchWidth=search_width
        )

    def get_historical_prices_of_tokens_by_contract_address(
        self,
        coins: str = "ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1,coingecko:ethereum,bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878,ethereum:0xdB25f211AB05b1c97D595516F45794528a807ad8",
        timestamp: int = 1648680149,
        search_width: str = "6h",
    ):
        return self._get(
            ApiSectionsEnum.COINS,
            "prices",
            "historical",
            timestamp,
            coins,
            searchWidth=search_width,
        )

    def get_batch_historical_prices(
        self,
        coins: dict = {
            "avax:0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e": [1666876743, 1666862343],
            "coingecko:ethereum": [1666869543, 1666862343],
        },
        search_width: str = "6h",
    ):
        return self._get(
            ApiSectionsEnum.COINS,
            "batchHistorical",
            coins=json.dumps(coins),
            searchWidth=search_width,
        )

    def get_token_prices_candle(
        self,
        coins: str = "ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1,coingecko:ethereum,bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878,ethereum:0xdB25f211AB05b1c97D595516F45794528a807ad8",
        start: int = None,
        end: int = None,
        span: int = 10,
        period: str = "24h",
        search_width: str = None,
    ):
        if start is None:
            start = (
                datetime.datetime.now().timestamp()
                - datetime.timedelta(days=90).total_seconds()
            )

        return self._get(
            ApiSectionsEnum.COINS,
            "chart",
            coins,
            start=start,
            end=end,
            span=span,
            period=period,
            searchWidth=search_width,
        )

    def get_percentage_change_in_coin_price(
        self,
        coins: str = "ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1,coingecko:ethereum,bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878,ethereum:0xdB25f211AB05b1c97D595516F45794528a807ad8",
        timestamp: int = None,
        look_forward: bool = False,
        period: str = "24h",
    ):
        return self._get(
            ApiSectionsEnum.COINS,
            "percentage",
            coins,
            timestamp=timestamp,
            lookForward=look_forward,
            period=period,
        )

    def get_earliest_timestamp_price_record_for_coins(
        self,
        coins: str = "ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1,coingecko:ethereum,bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878,ethereum:0xdB25f211AB05b1c97D595516F45794528a807ad8",
    ):
        return self._get(ApiSectionsEnum.COINS, "prices", "first", coins)

    def get_the_closest_block_to_timestamp(
        self, chain: str = "ethereum", timestamp: int = 1648680149
    ):
        return self._get(ApiSectionsEnum.COINS, "block", chain, timestamp)
