import requests
import pprint
from exc import InvalidResponseDataException, InvalidResponseStatusCodeException
from utils import get_retry_session
from log import get_logger


log = get_logger(__name__)


class DefiLlamaClient:
    def __init__(self, **kwargs) -> None:
        self._base_url: str = "https://api.llama.fi"
        self._stablecoins_url: str = "https://stablecoins.llama.fi"
        self._session: requests.Session = get_retry_session()

        if "headers" in kwargs:
            self._session.headers.update(kwargs["headers"])

    @property
    def session(self) -> requests.Session:
        return self._session

    def _format_url(self, endpoint: str) -> str:
        return f"{self._base_url}/{endpoint}"

    def _get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._session.get(self._format_url(endpoint), **kwargs)

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

    def get_protocols(self):
        r = self.session.get(f"{self._base_url}/protocols")
        return self._handle_response(r)

    def get_protocol(self, protocol):
        r = self.session.get(f"{self._base_url}/protocol/{protocol}")
        return self._handle_response(r)

    def get_historical_tvl_for_all_chains(self):
        r = self.session.get(f"{self._base_url}/v2/historicalChainTvl")
        return self._handle_response(r)

    def get_historical_tvl_for_chain(self, chain):
        r = self.session.get(f"{self._base_url}/v2/historicalChainTvl/{chain}")
        return self._handle_response(r)

    def get_historical_tvl_for_protocol(self, protocol):
        r = self.session.get(f"{self._base_url}/tvl/{protocol}")
        return self._handle_response(r)

    def get_current_tvl_of_all_chains(self):
        r = self.session.get(f"{self._base_url}/v2/chains")
        return self._handle_response(r)

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
