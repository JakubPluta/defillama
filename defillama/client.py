import requests
import pprint
DEFI_LLAMA_BASE_URL="https://api.llama.fi"


def get_session():
    return requests.Session()


def get_protocols():
    r = get_session().get(
        f"{DEFI_LLAMA_BASE_URL}/protocols"
    )
    return r.json()

def get_protocol(protocol):
    r = get_session().get(
        f"{DEFI_LLAMA_BASE_URL}/protocol/{protocol}"
    )
    return r.json()

def get_historical_all_chains_tvl():
    r = get_session().get(
        f"{DEFI_LLAMA_BASE_URL}/v2/historicalChainTvl"
    )
    return r.json()

def get_historical_tvl_for_chain(chain):
    r = get_session().get(
        f"{DEFI_LLAMA_BASE_URL}/v2/historicalChainTvl/{chain}"
    )
    return r.json()

def get_current_tvl_of_protocol(protocol):
    r = get_session().get(
        f"{DEFI_LLAMA_BASE_URL}/tvl/{protocol}"
    )
    return r.json()

def get_current_tvl_of_all_chains():
    r = get_session().get(
        f"{DEFI_LLAMA_BASE_URL}/v2/chains"
    )
    return r.json()



