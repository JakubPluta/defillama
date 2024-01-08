# DefiLlama
Python wrapper do Defi Llama API - an open and transparent DeFi analytics.
See more: [DefiLlama](https://defillama.com/)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)


## Installation

### Install with pip as package 

```bash
pip install defillama
```

### Install locally by cloning repository

```bash
# clone repo
git clone https://github.com/JakubPluta/defillama.git

# navigate to cloned project and create virtual environment
python -m venv env

# activate virtual environment
source env/Scripts/activate # or source env/bin/activate

# install poetry
pip install poetry

# install packages
poetry install
```


```Python
```


## Usage

Initialize client
```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
```

Retrieve all protocols on Defi Llama along with their TVL.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> protocols = client.get_protocols()
>>> protocols[0]
{
  "id": "2269",
  "name": "Binance CEX",
  "address": null,
  "symbol": "-",
  "url": "https://www.binance.com",
  "description": "Binance is a cryptocurrency exchange which is the largest exchange in the world in terms of daily trading volume of cryptocurrencies",
  "chain": "Multi-Chain",
  "logo": "https://icons.llama.fi/binance-cex.jpg",
  "audits": "0",
  "audit_note": null,
  "gecko_id": null,
  "cmcId": null,
  "category": "CEX",
  "chains": [
    "Bitcoin",
    "Ethereum",
    ...
  ],
  "module": "binance/index.js",
  "twitter": "binance",
  "forkedFrom": [],
  "oracles": [],
  "listedAt": 1668170565,
  "methodology": "We collect the wallets from this binance blog post https://www.binance.com/en/blog/community/our-commitment-to-transparency-2895840147147652626. We are not counting the Binance Recovery Fund wallet",
  "slug": "binance-cex",
  "tvl": 80255910530.16031,
  "chainTvls": {
    "Solana": 2034893648.1849031,
    "Aptos": 0,
    "Algorand": 97629726.26151134,
    "Ripple": 1343007667.2440999,
    "Binance": 10201465424.406801,
    "Fantom": 33.01604691,
    "Avalanche": 676475165.9217455,
    "Optimism": 869414892.4903527,
    "Polygon": 324707251.90665936,
    "Arbitrum": 2789490253.507592,
    "Polkadot": 724639629.7400626,
    "Tron": 14329408120.732595,
    "Ethereum": 21480280480.448257,
    "Bitcoin": 25040749893.72573,
    "Litecoin": 343748342.5739437
  },
  "change_1h": 0.08228675635628235,
  "change_1d": -1.3934001692790048,
  "change_7d": 1.1214132432391608,
  "tokenBreakdowns": {},
  "mcap": null
}

```

Retrieve historical TVL of a protocol and breakdowns by token and chain.
```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To check available protocol slugs you can use client.list_protocols()
>>> protocol_slug = 'astroport'
>>> protocol = client.get_protocol(protocol_slug)
protocol.keys()
dict_keys(['id', 'name', 'address', 'symbol', 'url', 'description', 'chain', 'logo', 'audits', 'audit_note', 'gecko_id', 'cmcId', 'category', 'chains', 'module', 'twitter', 'audit_links', 'openSource', 'listedAt', 'github', 'chainTvls', 'tvl', 'tokensInUsd', 'tokens', 'currentChainTvls', 'raises', 'metrics', 'mcap', 'methodology', 'misrepresentedTokens'])
```

Retrieve the historical total value locked (TVL) of decentralized finance (DeFi) on all chains. It excludes liquid staking and double counted tvl.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> defi_tvl = client.get_historical_tvl_of_defi_on_all_chains()
>>> defi_tvl[0]
{'date': 1530230400, 'tvl': 20541.94079040033}
```

Retrieve the historical total value locked (TVL) for a specific chain.
```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To see all available chains use client.list_chains() method
>>> chain = 'karura'
>>> defi_tvl = client.get_historical_tvl_for_chain(chain)
>>> defi_tvl[0]
{'date': 1628640000, 'tvl': 43936159.24741249}
```

Retrieve current total value locked (TVL) for a given protocol.
```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To check available protocol slugs you can use client.list_protocols()
>>> protocol_slug = 'astroport'
>>> tvl = client.get_current_tvl_for_protocol(protocol_slug)
>>> tvl
75725738.61222199
```

Retrieve current total value locked (TVL) of all chains.
```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> tvl = client.get_current_tvl_of_all_chains()
>>> tvl[0]
{'gecko_id': 'harmony', 'tvl': 4205486.363487561, 'tokenSymbol': 'ONE', 'cmcId': '3945', 'name': 'Harmony', 'chainId': 1666600000}
```

Retrieve all stablecoins along with their circulating ammounts.
```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> stables = client.get_stablecoins()
>>> stables[0]
{
    "id": "1",
    "name": "Tether",
    "symbol": "USDT",
    "gecko_id": "tether",
    "pegType": "peggedUSD",
    "priceSource": "defillama",
    "pegMechanism": "fiat-backed",
    "circulating": {...},
    "chains": [
        "Tron",
        "Ethereum",
        "BSC",
        ...
        "Everscale"
    ]
}
```

Retrieve the current market capitalization of stablecoins on each chain.
```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> stables = client.get_current_stablecoins_market_cap()
>>> stables[0]
{'gecko_id': None, 'totalCirculatingUSD': {'peggedUSD': 609658085.590443, 'peggedEUR': 1195711.7665694586, 'peggedVAR': 46327.625434798625, 'peggedJPY': 0.683455}, 'tokenSymbol': None, 'name': 'Optimism'}
```

Retrieve the current market capitalization of stablecoins on each chain.
```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To list stablecoins use client.list_stablecoins()
>>> stablecoin = 'USDC'
>>> stable = client.get_stablecoin_historical_market_cap(stablecoin)
>>> stable[0]
{'date': '1609372800', 'totalCirculating': {'peggedUSD': 3705248341.68}, 'totalUnreleased': {'peggedUSD': 0}, 'totalCirculatingUSD': {'peggedUSD': 3707668173.71}, 'totalMintedUSD': {'peggedUSD': 0}, 'totalBridgedToUSD': {'peggedUSD': 0}}
```

Retrieve the historical market cap and distribution of stablecoins in the specified blockchain.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> chain = 'ethereum'
>>> stables = client.get_stablecoins_historical_martket_cap_in_chain(chain)
>>> stables[0]
{'date': '1609372800', 'totalCirculating': {'peggedUSD': 19526560545.14, 'peggedEUR': 3330246.81}, 'totalUnreleased': {'peggedUSD': 60543897.49, 'peggedEUR': 0}, 'totalCirculatingUSD': {'peggedUSD': 19559297838.5, 'peggedEUR': 4068063.32}, 'totalMintedUSD': {'peggedUSD': 19927590563.72, 'peggedEUR': 4068063.32}, 'totalBridgedToUSD': {'peggedUSD': 133578118.32, 'peggedEUR': 0}}
```

Retrieve the historical market cap and chain distribution of a stablecoin.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> stablecoin = 'USDT'
>>> stables = client.get_stablecoins_historical_market_cap_and_chain_distribution(stablecoin)
>>> stables.keys()
dict_keys(['id', 'name', 'address', 'symbol', 'url', 'description', 'mintRedeemDescription', 'onCoinGecko', 'gecko_id', 'cmcId', 'pegType', 'pegMechanism', 'priceSource', 'auditLinks', 'twitter', 'wiki', 'chainBalances', 'currentChainBalances', 'price', 'tokens'])
```

Retrieve the historical prices of stablecoins.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> stables = client.get_stablecoins_historical_prices()
>>> stables[-1]
{
    'date': 1704672000,
    'prices': {
        'czusd': None,
        'silk-bcec1136-561c-4706-a42c-8b67d0d7f7d2': 1.09,
        'spiceusd': 0.089291,
        'usd-balance': 0.02704806,
        'colb-usd-stablecolb': 0.999871,
        'euroe-stablecoin': 1.092,
        'interest-protocol': None,
        'mountain-protocol-usdm': 1.002,
        'lugh': None,
        'first-digital-usd': 1,
        'offshift-anonusd': None,
        'neutrino': 0.056039,
        'rai': 2.86,
        'true-usd': 0.998922,
        'aryze-egbp': None,
        'vai': 0.997994,
        'paxos-standard': 1,
        'float-protocol-float': None,
        'e-money-eur': 1.072,
        # ...
    }
}
```

Retrieve the latest data for all pools, including enriched information such as predictions

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> pools = client.get_pools()
>>> pools[0]
{'chain': 'Ethereum', 'project': 'lido', 'symbol': 'STETH', 'tvlUsd': 20602827600, 'apyBase': 3.1, 'apyReward': None, 'apy': 3.1, 'rewardTokens': None, 'pool': '747c1d2a-c668-4682-b9f9-296708a3dd90', 'apyPct1D': -0.1, 'apyPct7D': None, 'apyPct30D': None, 'stablecoin': False, 'ilRisk': 'no', 'exposure': 'single', 'predictions': {'predictedClass': 'Down', 'predictedProbability': 51, 'binnedConfidence': 1}, 'poolMeta': None, 'mu': 4.42794, 'sigma': 0.04746, 'count': 589, 'outlier': False, 'underlyingTokens': ['0x0000000000000000000000000000000000000000'], 'il7d': None, 'apyBase7d': None, 'apyMean30d': 3.47797, 'volumeUsd1d': None, 'volumeUsd7d': None, 'apyBaseInception': None}
```

Retrieve the historical APY and TVL for a specific pool.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To list all available pools: client.list_pools()
>>> pool = 'USDC-WBTC' # by symbol or by id  pool = '1019c2a4-5330-467f-ad97-852448003878'
>>> pools = client.get_pool_historical_apy_and_tvl(pool)
>>> pools[0]
{'timestamp': '2023-11-10T23:01:27.607Z', 'tvlUsd': 1166, 'apy': 0, 'apyBase': 0, 'apyReward': None, 'il7d': None, 'apyBase7d': 0}
```

Retrieve a list of bridges.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> bridges = client.get_bridges()
>>> bridges[0]
{'id': 26, 'name': 'zksync', 'displayName': 'zkSync Era Bridge', 'icon': 'chain:zksync era', 'volumePrevDay': 55186404, 'volumePrev2Day': 46093693, 'lastHourlyVolume': 1449731.8487357053, 'currentDayVolume': 30964194.86409574, 'lastDailyVolume': 55186404, 'dayBeforeLastVolume': 46093693, 'weeklyVolume': 310121296, 'monthlyVolume': 1274364417, 'chains': ['Ethereum', 'zkSync Era'], 'destinationChain': 'zkSync Era'}
```

Retrieve the summary od bridge volume and volume breakdown by chain.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To list bridges use client.list_bridges()
>>> bridge = 'zksync' # or by id bridge = 26
>>> bridge_data = client.get_bridge(bridge)
>>> bridge_data
{'id': 26, 'name': 'zksync', 'displayName': 'zkSync Era Bridge', 'lastHourlyVolume': 0, 'currentDayVolume': 24797192.753594384, 'lastDailyVolume': 55186404, 'dayBeforeLastVolume': 46093693, 'weeklyVolume': 248951380, 'monthlyVolume': 1274364417, 'lastHourlyTxs': {'deposits': 0, 'withdrawals': 0}, 'currentDayTxs': {'deposits': 5260, 'withdrawals': 5260}, 'prevDayTxs': {'deposits': 20128, 'withdrawals': 20128}, 'dayBeforeLastTxs': {'deposits': 17768, 'withdrawals': 17768}, 'weeklyTxs': {'deposits': 33149, 'withdrawals': 33149}, 'monthlyTxs': {'deposits': 218956, 'withdrawals': 218956}, 'chainBreakdown': {'Ethereum': {'lastHourlyVolume': 0, 'currentDayVolume': 12398596.376797192, 'lastDailyVolume': 27593202, 'dayBeforeLastVolume': 23046846.5, 'weeklyVolume': 124475690, 'monthlyVolume': 637182208.5, 'lastHourlyTxs': {'deposits': 0, 'withdrawals': 0}, 'currentDayTxs': {'deposits': 2336, 'withdrawals': 2924}, 'prevDayTxs': {'deposits': 1718, 'withdrawals': 18410}, 'dayBeforeLastTxs': {'deposits': 4751, 'withdrawals': 13017}, 'weeklyTxs': {'deposits': 17051, 'withdrawals': 16098}, 'monthlyTxs': {'deposits': 104638, 'withdrawals': 114318}}, 'zkSync Era': {'lastHourlyVolume': 0, 'currentDayVolume': 12398596.376797192, 'lastDailyVolume': 27593202, 'dayBeforeLastVolume': 23046846.5, 'weeklyVolume': 124475690, 'monthlyVolume': 637182208.5, 'lastHourlyTxs': {'deposits': 0, 'withdrawals': 0}, 'currentDayTxs': {'deposits': 2924, 'withdrawals': 2336}, 'prevDayTxs': {'deposits': 18410, 'withdrawals': 1718}, 'dayBeforeLastTxs': {'deposits': 13017, 'withdrawals': 4751}, 'weeklyTxs': {'deposits': 16098, 'withdrawals': 17051}, 'monthlyTxs': {'deposits': 114318, 'withdrawals': 104638}}}, 'destinationChain': 'zkSync Era'}
```

Retrieve the volume of a bridge in a specific chain.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To list dex chains use client.list_dex_chains()
>>> chain = 'arbitrum' 
>>> bridge_data = client.get_bridge_volume(chain)
>>> bridge_data[0]
{'date': '1665964800', 'depositUSD': 179991, 'withdrawUSD': 321396, 'depositTxs': 7, 'withdrawTxs': 96}
```

Retrieve the bridge day statistics for a specific timestamp, chain, and bridge.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To list dex chains use client.list_dex_chains()
>>> chain, ts = 'ethereum', 1665964800
>>> bridge_data = client.get_bridge_day_stats(ts, chain)
>>> bridge_data[0]
{'date': 1665964800, 'totalTokensDeposited': {}, 'totalTokensWithdrawn': {}, 'totalAddressDeposited': {}, 'totalAddressWithdrawn': {}}
```

Retrieves a list of bridge transactions based on the specified criteria.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To list bridges use client.list_bridges()
>>> bridge = 'arbitrum'
>>> bridge_data = client.get_bridge_transactions(bridge)
>>> bridge_data[0]
{'tx_hash': '0x458bc85a857590a85bef7f8e7dfc4a67c60a8c0d16cab3383f823de228830e38', 'ts': '2024-01-08T15:43:23.000Z', 'tx_block': 18963268, 'tx_from': '0xB639039bd7ba74b21971bA4Eab89a6EEB9512c5C', 'tx_to': '0xa3A7B6F88361F48403514059F1F16C8E78d60EeC', 'token': '0x514910771AF9Ca656af840dff83E8264EcF986CA', 'amount': '1000000000000000000', 'is_deposit': True, 'chain': 'ethereum', 'bridge_name': 'arbitrum', 'usd_value': None}
```

## Run tests
```bash
make test 
# or 
pytest tests/ -vv -ss

# pytest cov
make cov
# or 
coverage run --source=defillama -m pytest tests/ -vv -ss && coverage report -m
```


## Contributing

You're welcome to add pull requests.


## Todo
- Pagination (most endpoints doesn't support pagination, so it needs to be done on client side)
- Possibility to use different types of data fromat/timestamp in some endpoints - with automatic conversion 