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

Retrieve all DEXes with all summaries of their volumes and dataType history.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> dex_volumes = client.get_dexes_volume_overview()
>>> dex_volumes.keys()
dict_keys(['totalDataChart', 'totalDataChartBreakdown', 'protocols', 'allChains', 'chain', 'total24h', 'total48hto24h', 'total7d', 'total14dto7d', 'total60dto30d', 'total30d', 'total1y', 'average1y', 'change_1d', 'change_7d', 'change_1m', 'totalVolume7d', 'totalVolume30d', 'change_7dover7d', 'change_30dover30d', 'breakdown24h'])
```

Retrieve all DEXes for a specific chain with all summaries of their volumes and dataType history.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To get all available chains use: client.list_dex_chains()
>>> chain = 'osmosis'
>>> dex_volumes = client.get_dexes_volume_overview_for_chain(chain)
>>> dex_volumes
{'totalDataChart': [], 'totalDataChartBreakdown': [], 'protocols': [{'defillamaId': '383', 'name': 'Osmosis DEX', 'disabled': False, 'displayName': 'Osmosis DEX', 'module': 'osmosis', 'category': 'Dexes', 'logo': 'https://icons.llamao.fi/icons/protocols/osmosis-dex.jpg', 'change_1d': -30.2, 'change_7d': 66.12, 'change_1m': 102.38, 'change_7dover7d': 25.05, 'change_30dover30d': 151.18, 'total24h': 37482383.20423146, 'total48hto24h': 53696406.00738978, 'total7d': 334952155.6249361, 'total30d': 1301084253.332036, 'total14dto7d': 267846597.9014448, 'total60dto30d': 517982028.2959299, 'total1y': 4458728450.627966, 'average1y': 342979111.5867666, 'totalAllTime': 24896301747.20423, 'breakdown24h': {'osmosis': {'osmosis': 37482383.20423146}}, 'chains': ['Osmosis'], 'protocolType': 'protocol', 'methodologyURL': 'https://github.com/DefiLlama/dimension-adapters/blob/master/dexs/osmosis', 'methodology': {'UserFees': 'Swap fees paid by users', 'Fees': 'Swap fees paid by users', 'Revenue': 'Percentage of swap fees going to treasury and/or token holders', 'ProtocolRevenue': 'Percentage of swap fees going to treasury', 'HoldersRevenue': 'Money going to governance token holders', 'SupplySideRevenue': 'Liquidity providers revenue'}, 'latestFetchIsOk': True, 'dailyVolume': 37482383.20423146, 'totalVolume7d': 22562856.27460225, 'totalVolume30d': 18520905}], 'allChains': ['Ethereum', 'Polygon', 'Starknet', 'Arbitrum', 'Mixin', 'zkSync Era', 'Base', 'opBNB', 'Polygon zkEVM', 'BSC', 'KCC', 'Fantom', 'Kava', 'Acala', 'Sui', 'Mantle', 'Avalanche', 'Solana', 'Stacks', 'Algorand', 'CORE', 'Telos', 'Aurora', 'Horizen EON', 'MultiversX', 'Terra Classic', 'Terra2', 'Injective', 'Neutron', 'Velas', 'Aptos', 'Gnosis', 'Moonbeam', 'Optimism', 'smartBCH', 'Bitcoin', 'MEER', 'Canto', 'Cube', 'EnergyWeb', 'Radix', 'Fusion', 'OKTChain', 'Linea', 'Klaytn', 'Concordium', 'Cronos', 'Cardano', 'Harmony', 'EOS', 'Wax', 'DefiChain', 'Carbon', 'Persistence', 'Scroll', 'Manta', 'LightLink', 'Elastos', 'Fuse', 'IoTeX', 'Energi', 'Findora', 'XDC', 'NEO', 'Evmos', 'Boba', 'Moonriver', 'FunctionX', 'GodwokenV1', 'Hedera', 'Onus', 'Metis', 'MAP Relay Chain', 'CLV', 'Hydra', 'HydraDX', 'Bitgert', 'ICP', 'Flow', 'Meter', 'OntologyEVM', 'Ultron', 'JBC', 'Kardia', 'KARURA', 'Ronin', 'Mode', 'Tombchain', 'PulseChain', 'Viction', 'Stellar', 'Heco', 'Bittorrent', 'TON', 'Celo', 'Conflux', 'Milkomeda C1', 'EOS EVM', 'Oraichain', 'Near', 'Osmosis', 'Obyte', 'Syscoin', 'Rollux', 'ENULS', 'Tezos', 'Sora', 'Rangers', 'SXnetwork', 'ShimmerEVM', 'Neon', 'Callisto', 'Ergo', 'Step', 'Tron', 'Arbitrum Nova', 'ThunderCore', 'Oasys', 'Thorchain', 'Icon', 'Vision', 'VeChain', 'Wanchain', 'WEMIX3.0', 'Dogechain', 'Godwoken', 'zkSync Lite', 'Zilliqa', 'Juno'], 'chain': 'Osmosis', 'total24h': 37482383.20423146, 'total48hto24h': None, 'total7d': 334952155.6249361, 'total14dto7d': 267846597.9014448, 'total60dto30d': 517982028.2959299, 'total30d': 1301084253.332036, 'total1y': 4458728450.627966, 'average1y': 342979111.5867666, 'change_1d': -30.2, 'change_7d': 66.12, 'change_1m': 102.38, 'totalVolume7d': 22562856.27460225, 'totalVolume30d': 18520905, 'change_7dover7d': 25.05, 'change_30dover30d': 151.18, 'breakdown24h': None}
```

Retrieve the summary of the DEX volume with historical data for given protocol.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To get all available protocols use: client.list_dex_protocols()
>>> protocol = 'balancer-v2'
>>> dex_volumes = client.get_summary_of_dex_volume_with_historical_data(protocol)
>>> dex_volumes.keys()
dict_keys(['defillamaId', 'name', 'displayName', 'disabled', 'logo', 'address', 'url', 'description', 'audits', 'category', 'twitter', 'audit_links', 'gecko_id', 'totalDataChart', 'totalDataChartBreakdown', 'total24h', 'total48hto24h', 'total14dto7d', 'totalAllTime', 'change_1d', 'module', 'protocolType', 'chains', 'methodologyURL', 'methodology', 'latestFetchIsOk', 'parentProtocol', 'childProtocols'])
```

Retrieve all options dexs along with summaries of their options and dataType history.


```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> dex_volumes = client.get_overview_dexes_options()
>>> dex_volumes.keys()
dict_keys(['totalDataChart', 'totalDataChartBreakdown', 'protocols', 'allChains', 'chain', 'total24h', 'total48hto24h', 'total7d', 'total14dto7d', 'total60dto30d', 'total30d', 'total1y', 'average1y', 'change_1d', 'change_7d', 'change_1m', 'totalVolume7d', 'totalVolume30d', 'change_7dover7d', 'change_30dover30d', 'breakdown24h', 'dailyPremiumVolume'])
```

Retrieve all options dexs along with summaries of their options and dataType history for specific chain.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To get all available chains use: client.list_options_chains()
>>> chain = 'bsc'
>>> options_volumes = client.get_overview_dexes_options_for_chain(chain)
>>> options_volumes
{'totalDataChart': [], 'totalDataChartBreakdown': [], 'protocols': [{'defillamaId': '534', 'name': 'Thales', 'disabled': False, 'displayName': 'Thales', 'module': 'thales', 'category': 'Prediction Market', 'logo': 'https://icons.llamao.fi/icons/protocols/thales.png', 'change_1d': None, 'change_7d': None, 'change_1m': None, 'change_7dover7d': 0, 'change_30dover30d': 0, 'total24h': 0, 'total48hto24h': 0, 'total7d': 0, 'total30d': 0, 'total14dto7d': 0, 'total60dto30d': 0, 'total1y': 3444.9842889749316, 'average1y': 264.99879145961023, 'totalAllTime': 7402.343703935723, 'breakdown24h': {'bsc': {'thales': 0}}, 'chains': ['BSC'], 'protocolType': 'protocol', 'methodologyURL': 'https://github.com/DefiLlama/dimension-adapters/blob/master/options/thales', 'methodology': {}, 'latestFetchIsOk': True, 'dailyPremiumVolume': 0, 'totalVolume7d': 0, 'totalVolume30d': 0}], 'allChains': ['Ethereum', 'Arbitrum', 'Polygon', 'Optimism', 'Fantom', 'BSC', 'Sui'], 'chain': 'BSC', 'total24h': 1997.9062889538222, 'total48hto24h': None, 'total7d': 1997.9062889538222, 'total14dto7d': 0, 'total60dto30d': 99.89919288360352, 'total30d': 2057.0447988141764, 'total1y': 17953.493427723526, 'average1y': 1496.124452310293, 'change_1d': 0, 'change_7d': 0, 'change_1m': 0, 'totalVolume7d': 0, 'totalVolume30d': 0, 'change_7dover7d': 0, 'change_30dover30d': 1959.12, 'breakdown24h': None}
```


Retrieve the summary of options volume with historical data for a given protocol.
To list available options protocols use: `client.list_options_protocols()`

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To get all available chains use: client.list_options_protocols()
>>> protocol = 'hegic'
>>> options_volumes = client.get_summary_of_options_volume_with_historical_data_for_protocol(protocol)
>>> options_volumes.keys()
dict_keys(['defillamaId', 'name', 'displayName', 'disabled', 'logo', 'address', 'url', 'description', 'audits', 'category', 'twitter', 'audit_links', 'gecko_id', 'totalDataChart', 'totalDataChartBreakdown', 'total24h', 'total48hto24h', 'total14dto7d', 'totalAllTime', 'change_1d', 'module', 'protocolType', 'chains', 'methodologyURL', 'methodology', 'latestFetchIsOk', 'childProtocols'])
```

Retrieve the fees and revenues for all protocols.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> fees = client.get_fees_and_revenues_for_all_protocols()
>>> fees.keys()
dict_keys(['totalDataChart', 'totalDataChartBreakdown', 'protocols', 'allChains', 'chain', 'total24h', 'total48hto24h', 'total7d', 'total14dto7d', 'total60dto30d', 'total30d', 'total1y', 'average1y', 'change_1d', 'change_7d', 'change_1m', 'totalVolume7d', 'totalVolume30d', 'change_7dover7d', 'change_30dover30d', 'breakdown24h', 'dailyRevenue', 'dailyUserFees', 'dailyHoldersRevenue', 'dailySupplySideRevenue', 'dailyProtocolRevenue', 'dailyBribesRevenue', 'dailyTokenTaxes'])
```

Retrieve fees and revenues for all protocols for a given chain.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To get all available chains use: client.list_fees_chains()
>>> chain = 'moonbeam'
>>> fees = client.get_fees_and_revenues_for_all_protocols_for_chain(chain)
>>> fees.keys()
dict_keys(['totalDataChart', 'totalDataChartBreakdown', 'protocols', 'allChains', 'chain', 'total24h', 'total48hto24h', 'total7d', 'total14dto7d', 'total60dto30d', 'total30d', 'total1y', 'average1y', 'change_1d', 'change_7d', 'change_1m', 'totalVolume7d', 'totalVolume30d', 'change_7dover7d', 'change_30dover30d', 'breakdown24h', 'dailyRevenue', 'dailyUserFees', 'dailyHoldersRevenue', 'dailySupplySideRevenue', 'dailyProtocolRevenue'])
```

Retrieve the summary of fees and revenue for a specific protocol.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To get all available chains use: client.list_fees_chains()
>>> protocol = 'fantom'
>>> fees = client.get_summary_of_protocols_fees_and_revenue(chain)
>>> fees.keys()
dict_keys(['defillamaId', 'name', 'displayName', 'disabled', 'logo', 'category', 'gecko_id', 'totalDataChart', 'totalDataChartBreakdown', 'total24h', 'total48hto24h', 'total14dto7d', 'totalAllTime', 'change_1d', 'module', 'protocolType', 'chains', 'methodologyURL', 'methodology', 'latestFetchIsOk', 'childProtocols'])
```

Retrieve the current prices of tokens by contract address.
To see all available chains use `client.list_chains()`
To see all available coingecko ids use `client.get_coingecko_coin_ids()`
You can use coingecko as a chain, and then use coin gecko ids instead of contract addresses:
`coins = "coingecko:uniswap,coingecko:ethereum"` or `coins = Coin("coingecko:uniswap")` or
`coins = {"chain": "coingecko", "address": "uniswap"}`

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()

# Use string with chain:address,chain:address syntax as an input parameter
>>> coins = "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,coingecko:ethereum"
>>> prices = client.get_current_prices_of_tokens_by_contract_address(coins)

# Use list of dictionaries as input parameter
>>> coins = [{"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"},{"chain": "coingecko","address": "uniswap"}]
>>> prices = client.get_current_prices_of_tokens_by_contract_address(coins)

# It can also be a single dict
>>> coin = {"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"}
>>> prices = client.get_current_prices_of_tokens_by_contract_address(coins)

# Or use Coin named tuple 
>>> coins = [Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"), Coin("bsc", "0x762539b45a1dcce3d36d080f74d1aed37844b878")]
>>> prices = client.get_current_prices_of_tokens_by_contract_address(coins)

# Or single Coin
>>> prices = client.get_current_prices_of_tokens_by_contract_address(Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"))
>>> prices
{'coins': {'ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984': {'decimals': 18, 'symbol': 'UNI', 'price': 6.24, 'timestamp': 1704744330, 'confidence': 0.99}}}
```


Retrieve the historical prices of tokens by contract address.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()

# Use string with chain:address,chain:address syntax as an input parameter
>>> coins = "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,coingecko:ethereum"
>>> prices = client.get_historical_prices_of_tokens_by_contract_address(coins, timestamp=1650000000)

# Use list of dictionaries as input parameter
>>> coins = [{"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"},{"chain": "coingecko","address": "uniswap"}]
>>> prices = client.get_historical_prices_of_tokens_by_contract_address(coins, timestamp=1650000000)

# It can also be a single dict
>>> coin = {"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"}
>>> prices = client.get_historical_prices_of_tokens_by_contract_address(coins, timestamp=1650000000)

# Or use Coin named tuple 
>>> coins = [Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"), Coin("bsc", "0x762539b45a1dcce3d36d080f74d1aed37844b878")]
>>> prices = client.get_historical_prices_of_tokens_by_contract_address(coins, timestamp=1650000000)

# Or single Coin
>>> prices = client.get_historical_prices_of_tokens_by_contract_address(Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"), timestamp=1650000000)
>>> prices
{'coins': {'ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984': {'decimals': 18, 'symbol': 'UNI', 'price': 9.778883768551262, 'timestamp': 1649999936}}}
```

Retrieve token prices at regular time intervals.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()

# Use string with chain:address,chain:address syntax as an input parameter
>>> coins = "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,coingecko:ethereum"
>>> prices = client.get_token_prices_candle(coins)

# Use list of dictionaries as input parameter
>>> coins = [{"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"},{"chain": "coingecko","address": "uniswap"}]
>>> prices = client.get_token_prices_candle(coins)

# It can also be a single dict
>>> coin = {"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"}
>>> prices = client.get_token_prices_candle(coins)

# Or use Coin named tuple 
>>> coins = [Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"), Coin("bsc", "0x762539b45a1dcce3d36d080f74d1aed37844b878")]
>>> prices = client.get_token_prices_candle(coins)

# Or single Coin
>>> prices = client.get_token_prices_candle(Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"))
>>> prices
{'coins': {'ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984': {'symbol': 'UNI', 'confidence': 0.99, 'decimals': 18, 'prices': [{'timestamp': 1704744928, 'price': 6.22}]}}}
```

Retrieve token price percentage change over time.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()

# Use string with chain:address,chain:address syntax as an input parameter
>>> coins = "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,coingecko:ethereum"
>>> prices = client.get_percentage_change_in_coin_price(coins)

# Use list of dictionaries as input parameter
>>> coins = [{"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"},{"chain": "coingecko","address": "uniswap"}]
>>> prices = client.get_percentage_change_in_coin_price(coins)

# It can also be a single dict
>>> coin = {"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"}
>>> prices = client.get_percentage_change_in_coin_price(coins)

# Or use Coin named tuple 
>>> coins = [Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"), Coin("bsc", "0x762539b45a1dcce3d36d080f74d1aed37844b878")]
>>> prices = client.get_percentage_change_in_coin_price(coins)

# Or single Coin
>>> prices = client.get_percentage_change_in_coin_price(Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"))
>>> prices
{'coins': {'ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984': 0.16155039918093603}}
```

Retrieve the earliest timestamped price record for the given coins.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()

# Use string with chain:address,chain:address syntax as an input parameter
>>> coins = "ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,coingecko:ethereum"
>>> prices = client.get_earliest_timestamp_price_record_for_coins(coins)

# Use list of dictionaries as input parameter
>>> coins = [{"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"},{"chain": "coingecko","address": "uniswap"}]
>>> prices = client.get_earliest_timestamp_price_record_for_coins(coins)

# It can also be a single dict
>>> coin = {"chain": "ethereum","address": "0xdF574c24545E5FfEcb9a659c229253D4111d87e1"}
>>> prices = client.get_earliest_timestamp_price_record_for_coins(coins)

# Or use Coin named tuple 
>>> coins = [Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"), Coin("bsc", "0x762539b45a1dcce3d36d080f74d1aed37844b878")]
>>> prices = client.get_earliest_timestamp_price_record_for_coins(coins)

# Or single Coin
>>> prices = client.get_earliest_timestamp_price_record_for_coins(Coin("ethereum", "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"))
>>> prices
{'coins': {'ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984': {'symbol': 'UNI', 'price': 2.9696706531528196, 'timestamp': 1600308306}, 'coingecko:ethereum': {'symbol': 'ETH', 'price': 2.83162, 'timestamp': 1438905600}}}
```

Retrieve the closest block to the given timestamp for a specific chain.

```Python
>>> from defillama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> chain = 'ethereum'
>>> prices = client.get_the_closest_block_to_timestamp(chain, timestamp=1600308306)
>>> prices
{'height': 10876852, 'timestamp': 1600308344}


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