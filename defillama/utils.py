import datetime
import json
import pathlib
from typing import Dict, Union, List
import requests
from requests.adapters import HTTPAdapter
from requests import HTTPError
from requests.packages.urllib3.util.retry import Retry
from dtypes import Coin
from log import get_logger


log = get_logger(__name__)

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def get_retry_session(retries=5, backoff_factor=0.1) -> requests.Session:
    """Get a Session object with retry capabilities.

    Args:
        retries: The number of retries to attempt before giving up.
        backoff_factor: The factor by which to increase the wait time between retries.

    Returns:
        A Session object with retry capabilities.
    """
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504, 406],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        }
    )
    return session



def timestamp_converter(timestamp: int, as_str = False, fmt: str = "%Y-%m-%d %H:%M:%S") -> Union[str, datetime.datetime]:
    """
    Convert a Unix timestamp to a formatted string or a datetime object.
    
    Args:
        timestamp (int): The Unix timestamp to convert.
        as_str (bool, optional): If True, return the formatted timestamp as a string. 
            If False, return the datetime object. Defaults to False.
        fmt (str, optional): The format string to use when returning the formatted timestamp. 
            Defaults to "%Y-%m-%d %H:%M:%S".
    
    Returns:
        Union[str, datetime.datetime]: If `as_str` is True, returns the formatted timestamp as a string.
            If `as_str` is False, returns the datetime object.
    """
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt.strftime(fmt) if as_str else dt


def get_coingecko_coin_ids() -> List[str]:
    """Retrieves a list of CoinGecko coin IDs.

    Returns:
        list[str]: A list of CoinGecko coin IDs.
    """
    session = get_retry_session()
    response = session.get("https://api.coingecko.com/api/v3/coins/list")
    try:
        response.raise_for_status()
    except HTTPError as e:
        log.error(f"Error retrieving CoinGecko ID's. Reason: {str(e)}")
        raise HTTPError("Error retrieving CoinGecko IDs") from e
    return [coin["id"] for coin in response.json()]



def read_coingecko_ids_from_file() -> List[str]:
    """Retrieves a list of CoinGecko coin IDs from a file.

    Returns:
        list[str]: A list of CoinGecko coin IDs.
    """
    coins_path = DATA_DIR / "coingecko_ids.json"
    with open(coins_path, "r") as f:
        coingecko_ids = json.load(f)['coins']
    return coingecko_ids



def _prepare_token(token: Union[Coin, str, Dict[str, str]]) -> str:
    """
    Prepare a token for processing.

    Args:
        token (Union[Coin, str, Dict[str, str]]): The token to be prepared.

    Returns:
        str: The prepared token.
    """
    if isinstance(token, Coin):
        return f"{token.chain}:{token.address}"
    elif isinstance(token, dict):
        return f"{token['chain']}:{token['address']}"
    return token


def prepare_coins_for_request(coins: Union[str, Coin, Dict[str, str], List[Coin], List[Dict[str, str]]]) -> str:
    """
    Prepare tokens for a request.

    Args:
        coins (Union[List[Union[Coin, Dict[str, str]]], str]): The tokens to prepare for the request. It can be either a list of coins or a string.

    Returns:
        str: The prepared tokens as a comma-separated string.
        
    Example:
        >>> coins = "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984","ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
        >>> prepare_tokens_for_request(coins)
        >>> ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
            
        >>> coins = [{"chain":"ethereum","address":"0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"},{"chain":"ethereum","address":"0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"}]
        >>> prepare_tokens_for_request(coins)
        >>> ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
        
        >>> coins = [Coin("ethereum","0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"),Coin("ethereum","0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984")]
        >>> prepare_tokens_for_request(coins)
        >>> ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
        
        >>> coins = Coin("ethereum","0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984")
        >>> prepare_tokens_for_request(coins)
        >>> ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
        
        >>> coins = {"chain":"ethereum","address":"0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"}
        >>> prepare_tokens_for_request(coins)
        >>> ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
        
    """
    if isinstance(coins, str):
        return coins
    if isinstance(coins, list):
        return ",".join([_prepare_token(token) for token in coins])
    if isinstance(coins, (Coin, dict)):
        return _prepare_token(coins)
    raise ValueError(f"Unsupported type: {type(coins)}")


