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


    def _get(self, section: ApiSectionsEnum, endpoint: str, *args, **query_params) -> requests.Response:
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

    def get_stablecoins(self, include_prices: bool = True):
        "include prices -> query params"
        r = self.session.get(
            f"{self._stablecoins_url}/stablecoins",
            params={"includePrices": include_prices},
        )
        return self._handle_response(r)

    def get_current_stablecoins_mcap(
        self,
    ):
        """stablecoin query params"""
        r = self.session.get(
            f"{self._stablecoins_url}/stablecoinchains",
        )
        return self._handle_response(r)

    def get_historical_stablecoins_mcap(self, stablecoin_id: int):
        """stablecoin query params"""
        r = self.session.get(
            f"{self._stablecoins_url}/stablecoincharts/all",
            params={"stablecoin": stablecoin_id},
        )
        return self._handle_response(r)

    def get_historical_stablecoins_mcap_on_chain(
        self, chain: str = "Ethereum", stablecoin_id: int = 1
    ):
        """stablecoin query params"""
        r = self.session.get(
            f"{self._stablecoins_url}/stablecoincharts/all",
            params={"stablecoin": stablecoin_id, "chain": chain},
        )
        return self._handle_response(r)

    def get_historical_stablecoins_mcap_and_distribution(self, stablecoin_id: int = 1):
        """stablecoin query params"""
        r = self.session.get(
            f"{self._stablecoins_url}/stablecoin/{stablecoin_id}",
        )
        return self._handle_response(r)

    def get_historical_stablecoins_prices(self):
        """stablecoin query params"""
        r = self.session.get(
            f"{self._stablecoins_url}/stablecoinprices",
        )
        return self._handle_response(r)

