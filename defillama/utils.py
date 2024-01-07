import datetime
import json
import pathlib
from typing import Dict, List, Union

import requests
from requests import HTTPError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from defillama.dtypes import Coin
from defillama.log import get_logger

log = get_logger(__name__)

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
RESOURCES_DIR = PROJECT_ROOT / "resources"


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
    return session


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
        log.error("Error retrieving CoinGecko ID's. Reason: %s", str(e))
        raise HTTPError("Error retrieving CoinGecko IDs") from e
    return [coin["id"] for coin in response.json()]


def read_coingecko_ids_from_file() -> List[str]:
    """Retrieves a list of CoinGecko coin IDs from a file.

    Returns:
        list[str]: A list of CoinGecko coin IDs.
    """
    coins_path = RESOURCES_DIR / "coingecko_ids.json"
    with open(coins_path, "r") as f:
        coingecko_ids = json.load(f)["coins"]
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
    if isinstance(token, dict):
        return f"{token['chain']}:{token['address']}"
    return token


def prepare_coins_for_request(
    coins: Union[str, Coin, Dict[str, str], List[Coin], List[Dict[str, str]]]
) -> str:
    """
    Prepare tokens for a request.

    Args:
        coins (Union[List[Union[Coin, Dict[str, str]]], str]): The tokens to prepare for the request.
        It can be either a list of coins or a string.

    Returns:
        str: The prepared tokens as a comma-separated string.

    Example:
        >>> coins = "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984","ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
        >>> prepare_tokens_for_request(coins)
        >>> ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984

        >>> coins = [
            {"chain":"ethereum","address":"0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"},
            {"chain":"ethereum","address":"0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"}
            ]
        >>> prepare_tokens_for_request(coins)
        >>> ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984

        >>> coins = [
            Coin("ethereum","0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"),
            Coin("ethereum","0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984")
            ]
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


def get_previous_timestamp(delta_days: int = 90) -> int:
    """
    Generate a timestamp representing a specified number of days before the current time.

    Args:
        delta_days (int): The number of days to go back in time. Defaults to 90.

    Returns:
        int: The timestamp representing the specified number of days before the current time.
    """
    print(">>>>>>", datetime.datetime.now())
    return int(
        datetime.datetime.now().timestamp()
        - datetime.timedelta(days=delta_days).total_seconds()
    )


def get_stablecoin_id(stablecoin: Union[str, int], stablecoins: Dict[str, str]) -> int:
    """
    Returns the ID of a stablecoin based on its name or ID.

    Parameters:
        stablecoin (Union[str, int]): The name or ID of the stablecoin.
        stablecoins (Dict[str, str]): A dictionary mapping stablecoin IDs to their names.

    Returns:
        int: The ID of the stablecoin.

    Raises:
        ValueError: If the stablecoin is invalid or not found in the stablecoins dictionary.
    """
    if isinstance(stablecoin, str) and not stablecoin.isnumeric():
        stablecoin_id = next(
            (
                k
                for k, v in stablecoins.items()
                if v == stablecoin or v.lower() == stablecoin.lower()
            ),
            None,
        )
        if stablecoin_id is None:
            raise ValueError(
                f"Invalid stablecoin: {stablecoin}. Available stablecoins: {stablecoins}"
            )
    elif isinstance(stablecoin, (int, str)):
        stablecoin_id = int(stablecoin)
    else:
        raise ValueError("Invalid stablecoin")

    validate_searched_entity(stablecoin_id, stablecoins, "stablecoin")
    return stablecoin_id


def get_bridge_id(bridge: Union[str, int], bridges: Dict[str, str]) -> int:
    """
    Get the bridge ID based on the provided bridge name or ID.

    Args:
        bridge (Union[str, int]): The name or ID of the bridge.
        bridges (Dict[str, str]): A dictionary mapping bridge IDs to bridge names.

    Returns:
        int: The ID of the bridge.

    Raises:
        ValueError: If the provided bridge is invalid and not found in the available bridges.

    Examples:
        >>> bridges = {'1': 'Bridge 1', '2': 'Bridge 2'}
        >>> get_bridge_id('Bridge 1', bridges)
        >>> 1
        >>> get_bridge_id(2, bridges)
        >>> 2
        >>> get_bridge_id('Invalid Bridge', bridges)
        ValueError: Invalid bridge: Invalid Bridge. Available bridges: {'1': 'Bridge 1', '2': 'Bridge 2'}
    """
    if isinstance(bridge, str) and not bridge.isnumeric():
        bridge_id = next(
            (
                k
                for k, v in bridges.items()
                if v == bridge or v.lower() == bridge.lower()
            ),
            None,
        )
        if bridge_id is None:
            raise ValueError(f"Invalid bridge: {bridge}. Available bridges: {bridges}")
    else:
        bridge_id = int(bridge)

    validate_searched_entity(bridge_id, bridges, "bridge")
    return bridge_id


def validate_searched_entity(
    entity: Union[str, int], entities: List[str], entity_type: str = ""
) -> None:
    """
    Validates the searched entity by checking if it exists in the list of entities.

    Parameters:
        entity (Union[str, int]): The entity to be validated.
        entities (List[str]): The list of entities to search in.
        entity_type (str): The type of the entity (optional).

    Raises:
        ValueError: If the entity is not found in the list of entities.

    Returns:
        None
    """
    if entity not in entities:
        raise ValueError(f"Invalid {entity_type}: {entity}. Available: {entities}")


_DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%m/%d/%Y",
    "%m/%d/%Y %H:%M:%S",
    "%d-%b-%Y",
    "%d-%b-%y",
    "%b %d, %Y",
    "%b %d, %Y %H:%M:%S",
    "%d %b %Y",
    "%d %b %Y %H:%M:%S",
    "%Y%m%d",
    "%Y%m%d%H%M%S",
    "%Y/%m/%d",
    "%Y/%m/%d %H:%M:%S",
    "%Y%m%d %H:%M:%S",
    "%Y/%m/%d %I:%M:%S %p",
    "%Y-%m-%dT%H:%M:%S.%fZ",
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%S%z",
    "%m-%d-%Y",
    "%m-%d-%Y %H:%M:%S",
    "%m/%d/%y",
    "%m/%d/%y %H:%M:%S",
    "%b %d %Y",
    "%b %d %Y %H:%M:%S",
    "%b. %d, %Y",
    "%b. %d, %Y %H:%M:%S",
    "%d %b, %Y",
    "%d %b, %Y %H:%M:%S",
    "%d %B %Y",
    "%d %B %Y %H:%M:%S",
    "%B %d %Y",
    "%B %d %Y %H:%M:%S",
]


def convert_to_timestamp(
    date: Union[datetime.datetime, datetime.date, str, int]
) -> int:
    """
    Convert the given date to a timestamp.

    Parameters:
        date (Union[datetime.datetime, datetime.date, str, int]): The date to be converted.
        formats (List[str], optional): A list of date formats to try when converting a string to a
            datetime object. Defaults to _DATE_FORMATS.

    Returns:
        int: The timestamp representation of the given date.

    Raises:
        ValueError: If the date format is invalid and no valid format is found in the formats list.
        TypeError: If the date format is not supported.

    """

    if isinstance(date, datetime.datetime):
        timestamp = date.timestamp()
    elif isinstance(date, datetime.date):
        timestamp = datetime.datetime(date.year, date.month, date.day).timestamp()
    elif isinstance(date, str):
        for format in _DATE_FORMATS:
            try:
                timestamp = datetime.datetime.timestamp(
                    datetime.datetime.strptime(date, format)
                )
                break
            except ValueError:
                pass
        else:
            raise ValueError(
                "Invalid date format. If you want't to specify another format override DATE_FORMATS argument"
            )
    elif isinstance(date, int) and date not in [0, 1]:
        timestamp = date
    else:
        raise TypeError(
            "Unsupported date format. Use datetime.datetime, datetime.date, str, or int"
        )
    return int(timestamp)


def convert_from_timestamp(
    timestamp: int, as_str=False, fmt: str = "%Y-%m-%d %H:%M:%S"
) -> Union[str, datetime.datetime]:
    """
    Convert a Unix timestamp to a formatted string or a datetime object.

    Parameters:
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
