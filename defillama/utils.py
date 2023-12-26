import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def get_retry_session(retries=6, backoff_factor=0.1) -> requests.Session:
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
