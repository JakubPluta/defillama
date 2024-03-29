# DefiLlama (dfllama)

[![codecov](https://codecov.io/gh/JakubPluta/defillama/graph/badge.svg?token=LSF4LTJFF8)](https://codecov.io/gh/JakubPluta/defillama)
[![PyPI version](https://badge.fury.io/py/dfllama.svg)](https://badge.fury.io/py/dfllama)
<a target="new" href="https://github.com/JakubPluta/defillama"><img border=0 src="https://img.shields.io/github/stars/JakubPluta/defillama.svg?style=social&label=Star&maxAge=60" alt="Star this repo"></a>


The Python wrapper for the Defi Llama API that provides open and transparent DeFi analytics. It allows you to easily access and retrieve data from the Defi Llama platform, which offers comprehensive insights into the decentralized finance ecosystem
See more: [DefiLlama](https://defillama.com/)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)


## Installation

### Install with pip as a package [pip](https://pypi.org/project/dfllama)

```bash
pip install dfllama
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


## Usage

Initialize client
```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
```

Retrieve all protocols on Defi Llama along with their TVL.

```Python
>>> from dfllama import DefiLlamaClient, Coin
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
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To check available protocol slugs you can use client.list_protocols()
>>> protocol_slug = 'astroport'
>>> protocol = client.get_protocol(protocol_slug)
protocol
{
  "id": "3117",
  "name": "Astroport",
  "address": "terra:terra1nsuqsk6kh58ulczatwev87ttq2z6r3pusulg9r24mfj2fvtzd4uq3exn26",
  "symbol": "ASTRO",
  "url": "https://astroport.fi",
  "description": "The meta AMM of Cosmos",
  "chain": "Terra2",
  "logo": "https://icons.llama.fi/astroport.jpg",
  "audits": "2",
  "audit_note": null,
  "gecko_id": "astroport-fi",
  "cmcId": "23374",
  "category": "Dexes",
  "chains": [
    "Neutron",
    "Terra2",
    "Injective",
    "Sei"
  ],
  "module": "astroport/index.js",
  "twitter": "astroport_fi",
  "audit_links": [
    "https://github.com/astroport-fi/astro-audits"
  ],
  "openSource": true,
  "listedAt": 1686894797,
  "github": [
    "astroport-fi"
  ],
  "chainTvls": {
    "Neutron": {
      "tvl": [
        {
          "date": 1686873600,
          "totalLiquidityUSD": 14421444.06292
        },
        ...
      ],
      "tokensInUsd": [
        {
          "date": 1686873600,
          "tokens": {
            "AXLUSDC": 4638587.85655,
            "ATOM": 9782856.20637
          }
        },
        ...
      ],
      "tokens": [
        {
          "date": 1692230400,
          "tokens": {
            "USDCET": 66783.71223,
            "USDTBS": 19.15192,
            "WBTC": 0,
            "USDCAR": 55403.62737,
            "USDCSO": 103.37941,
            "SEI": 9916.47926,
            "WETH": 0.06588
          }
        },
        ...
      ]
    },
    "Terra2": {
      ...
    },
    "Injective": {
      ...
    },
    "Sei": {
      ...
    }
  },
  "tvl": [    {
    "date": 1686873600,
    "totalLiquidityUSD": 24839233.07235
  },
  ...
  ],
  "tokensInUsd": [
    {
      "date": 1686873600,
      "tokens": {
        "XPRT": 0.00001,
        "OSMO": 49.74612,
        "AXLUSDC": 4638587.85655,
        "INJ": 3367742.90694,
        "ASTRO": 698984.42626,
        "USDT": 232493.04293,
        "ATOM": 10382054.05079,
        "WSTETH": 74.35649,
        "GF": 0,
        "LUNA": 5519246.68627
      }
    },
    ...
  ],
  "tokens": [
    {
      "date": 1686873600,
      "tokens": {
        "XPRT": 0.00005,
        "OSMO": 107.58569,
        "AXLUSDC": 4629329.19815,
        "INJ": 564111.03969,
        "ASTRO": 20181686.17738,
        "USDT": 232663.81817,
        "ATOM": 1186520.46295,
        "WSTETH": 0.0394,
        "GF": 0,
        "LUNA": 9379184.35208
      },
      ...
    }
  ],
  "currentChainTvls": {
    "Neutron": 50055369.84474,
    "Terra2": 17425482.05631,
    "Injective": 3729626.09133,
    "Sei": 10571526.35363
  },
  "raises": [],
  "metrics": {
    "dexs": true
  },
  "mcap": 137947266.24143237,
  "methodology": "Liquidity on the DEX",
  "misrepresentedTokens": true
}
```

Retrieve the historical total value locked (TVL) of decentralized finance (DeFi) on all chains. It excludes liquid staking and double counted tvl.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> defi_tvl = client.get_historical_tvl_of_defi_on_all_chains()
>>> defi_tvl[0]
{'date': 1530230400, 'tvl': 20541.94079040033}
```

Retrieve the historical total value locked (TVL) for a specific chain.
```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To see all available chains use client.list_chains() method
>>> chain = 'karura'
>>> defi_tvl = client.get_historical_tvl_for_chain(chain)
>>> defi_tvl[0]
{'date': 1628640000, 'tvl': 43936159.24741249}
```

Retrieve current total value locked (TVL) for a given protocol.
```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To check available protocol slugs you can use client.list_protocols()
>>> protocol_slug = 'astroport'
>>> tvl = client.get_current_tvl_for_protocol(protocol_slug)
>>> tvl
75725738.61222199
```

Retrieve current total value locked (TVL) of all chains.
```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> tvl = client.get_current_tvl_of_all_chains()
>>> tvl[0]
{
  "gecko_id": "harmony",
  "tvl": 4342729.138696362,
  "tokenSymbol": "ONE",
  "cmcId": "3945",
  "name": "Harmony",
  "chainId": 1666600000
}
```

Retrieve all stablecoins along with their circulating ammounts.
```Python
>>> from dfllama import DefiLlamaClient, Coin
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
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> stables = client.get_current_stablecoins_market_cap()
>>> stables[0]
{'gecko_id': None, 'totalCirculatingUSD': {'peggedUSD': 609658085.590443, 'peggedEUR': 1195711.7665694586, 'peggedVAR': 46327.625434798625, 'peggedJPY': 0.683455}, 'tokenSymbol': None, 'name': 'Optimism'}
```

Retrieve the current market capitalization of stablecoins on each chain.
```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To list stablecoins use client.list_stablecoins()
>>> stablecoin = 'USDC'
>>> stable = client.get_stablecoin_historical_market_cap(stablecoin)
>>> stable[0]
{
    "date": "1609372800",
    "totalCirculating": {
        "peggedUSD": 3705248341.68
    },
    "totalUnreleased": {
        "peggedUSD": 0
    },
    "totalCirculatingUSD": {
        "peggedUSD": 3707668173.71
    },
    "totalMintedUSD": {
        "peggedUSD": 0
    },
    "totalBridgedToUSD": {
        "peggedUSD": 0
    }
}
```

Retrieve the historical market cap and distribution of stablecoins in the specified blockchain.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> chain = 'ethereum'
>>> stables = client.get_stablecoins_historical_martket_cap_in_chain(chain)
>>> stables[0]
{
    "date": "1609372800",
    "totalCirculating": {
        "peggedUSD": 19526560545.14,
        "peggedEUR": 3330246.81
    },
    "totalUnreleased": {
        "peggedUSD": 60543897.49,
        "peggedEUR": 0
    },
    "totalCirculatingUSD": {
        "peggedUSD": 19559297838.5,
        "peggedEUR": 4068063.32
    },
    "totalMintedUSD": {
        "peggedUSD": 19927590563.72,
        "peggedEUR": 4068063.32
    },
    "totalBridgedToUSD": {
        "peggedUSD": 133578118.32,
        "peggedEUR": 0
    }
}
```

Retrieve the historical market cap and chain distribution of a stablecoin.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> stablecoin = 'USDT'
>>> stables = client.get_stablecoins_historical_market_cap_and_chain_distribution(stablecoin)
>>> stables
{
  "id": "1",
  "name": "Tether",
  "address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
  "symbol": "USDT",
  "url": "https://tether.to/",
  "description": "Launched in 2014, Tether tokens pioneered the stablecoin model. Tether tokens are pegged to real-world currencies on a 1-to-1 basis. This offers traders, merchants and funds a low volatility solution when exiting positions in the market.",
  "mintRedeemDescription": "Tether customers who have undergone a verification process can exchange USD for USDT and redeem USDT for USD.",
  "onCoinGecko": "true",
  "gecko_id": "tether",
  "cmcId": "825",
  "pegType": "peggedUSD",
  "pegMechanism": "fiat-backed",
  "priceSource": "defillama",
  "auditLinks": [
    "https://tether.to/en/transparency/#reports"
  ],
  "twitter": "https://twitter.com/Tether_to",
  "wiki": "https://wiki.defillama.com/wiki/USDT",
  "chainBalances" : {
    "Optimism" : {
      ...
    },
    ...
  },
  "currentChainBalances": {
    "Optimism": {
      "peggedUSD": 318446549.575766
    },
   ...
  },
  "price": 0.999947,
  "tokens": [
    {
      "date": 1652313600,
      "circulating": {
        "peggedUSD": 79485744715.4551
      },
      "minted": 0,
      "unreleased": {
        "peggedUSD": 4222390429.416619
      },
      "bridgedTo": 0
    },
  ...
  ]

}



```

Retrieve the historical prices of stablecoins.

```Python
>>> from dfllama import DefiLlamaClient, Coin
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
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> pools = client.get_pools()
>>> pools[0]
{
    "chain": "Ethereum",
    "project": "lido",
    "symbol": "STETH",
    "tvlUsd": 20602827600,
    "apyBase": 3.1,
    "apyReward": null,
    "apy": 3.1,
    "rewardTokens": null,
    "pool": "747c1d2a-c668-4682-b9f9-296708a3dd90",
    "apyPct1D": -0.1,
    "apyPct7D": null,
    "apyPct30D": null,
    "stablecoin": false,
    "ilRisk": "no",
    "exposure": "single",
    "predictions": {
        "predictedClass": "Down",
        "predictedProbability": 51,
        "binnedConfidence": 1
    },
    "poolMeta": null,
    "mu": 4.42794,
    "sigma": 0.04746,
    "count": 589,
    "outlier": false,
    "underlyingTokens": [
        "0x0000000000000000000000000000000000000000"
    ],
    "il7d": null,
    "apyBase7d": null,
    "apyMean30d": 3.47797,
    "volumeUsd1d": null,
    "volumeUsd7d": null,
    "apyBaseInception": null
}
```

Retrieve the historical APY and TVL for a specific pool.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To list all available pools: client.list_pools()
>>> pool = 'USDC-WBTC' # by symbol or by id  pool = '1019c2a4-5330-467f-ad97-852448003878'
>>> pools = client.get_pool_historical_apy_and_tvl(pool)
>>> pools[0]
{
    "timestamp": "2023-11-10T23:01:27.607Z",
    "tvlUsd": 1166,
    "apy": 0,
    "apyBase": 0,
    "apyReward": null,
    "il7d": null,
    "apyBase7d": 0
}
```

Retrieve a list of bridges.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> bridges = client.get_bridges()
>>> bridges[0]
{
    "id": 26,
    "name": "zksync",
    "displayName": "zkSync Era Bridge",
    "icon": "chain:zksync era",
    "volumePrevDay": 55186404,
    "volumePrev2Day": 46093693,
    "lastHourlyVolume": 1449731.8487357053,
    "currentDayVolume": 30964194.86409574,
    "lastDailyVolume": 55186404,
    "dayBeforeLastVolume": 46093693,
    "weeklyVolume": 310121296,
    "monthlyVolume": 1274364417,
    "chains": [
        "Ethereum",
        "zkSync Era"
    ],
    "destinationChain": "zkSync Era"
}
```

Retrieve the summary od bridge volume and volume breakdown by chain.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To list bridges use client.list_bridges()
>>> bridge = 'zksync' # or by id bridge = 26
>>> bridge_data = client.get_bridge(bridge)
>>> bridge_data
{
    "id": 26,
    "name": "zksync",
    "displayName": "zkSync Era Bridge",
    "lastHourlyVolume": 0,
    "currentDayVolume": 24797192.753594384,
    "lastDailyVolume": 55186404,
    "dayBeforeLastVolume": 46093693,
    "weeklyVolume": 248951380,
    "monthlyVolume": 1274364417,
    "lastHourlyTxs": {
        "deposits": 0,
        "withdrawals": 0
    },
    "currentDayTxs": {
        "deposits": 5260,
        "withdrawals": 5260
    },
    "prevDayTxs": {
        "deposits": 20128,
        "withdrawals": 20128
    },
    "dayBeforeLastTxs": {
        "deposits": 17768,
        "withdrawals": 17768
    },
    "weeklyTxs": {
        "deposits": 33149,
        "withdrawals": 33149
    },
    "monthlyTxs": {
        "deposits": 218956,
        "withdrawals": 218956
    },
    "chainBreakdown": {
        "Ethereum": {
            "lastHourlyVolume": 0,
            "currentDayVolume": 12398596.376797192,
            "lastDailyVolume": 27593202,
            "dayBeforeLastVolume": 23046846.5,
            "weeklyVolume": 124475690,
            "monthlyVolume": 637182208.5,
            "lastHourlyTxs": {
                "deposits": 0,
                "withdrawals": 0
            },
            "currentDayTxs": {
                "deposits": 2336,
                "withdrawals": 2924
            },
            "prevDayTxs": {
                "deposits": 1718,
                "withdrawals": 18410
            },
            "dayBeforeLastTxs": {
                "deposits": 4751,
                "withdrawals": 13017
            },
            "weeklyTxs": {
                "deposits": 17051,
                "withdrawals": 16098
            },
            "monthlyTxs": {
                "deposits": 104638,
                "withdrawals": 114318
            }
        },
        "zkSync Era": {
            "lastHourlyVolume": 0,
            "currentDayVolume": 12398596.376797192,
            "lastDailyVolume": 27593202,
            "dayBeforeLastVolume": 23046846.5,
            "weeklyVolume": 124475690,
            "monthlyVolume": 637182208.5,
            "lastHourlyTxs": {
                "deposits": 0,
                "withdrawals": 0
            },
            "currentDayTxs": {
                "deposits": 2924,
                "withdrawals": 2336
            },
            "prevDayTxs": {
                "deposits": 18410,
                "withdrawals": 1718
            },
            "dayBeforeLastTxs": {
                "deposits": 13017,
                "withdrawals": 4751
            },
            "weeklyTxs": {
                "deposits": 16098,
                "withdrawals": 17051
            },
            "monthlyTxs": {
                "deposits": 114318,
                "withdrawals": 104638
            }
        }
```

Retrieve the volume of a bridge in a specific chain.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To list dex chains use client.list_dex_chains()
>>> chain = 'arbitrum' 
>>> bridge_data = client.get_bridge_volume(chain)
>>> bridge_data[0]
{
    "date": "1665964800",
    "depositUSD": 179991,
    "withdrawUSD": 321396,
    "depositTxs": 7,
    "withdrawTxs": 96
}
```

Retrieve the bridge day statistics for a specific timestamp, chain, and bridge.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To list dex chains use client.list_dex_chains()
>>> chain, ts = 'ethereum', 1665964800
>>> bridge_data = client.get_bridge_day_stats(ts, chain)
>>> bridge_data[0]
{
    "date": 1665964800,
    "totalTokensDeposited": {},
    "totalTokensWithdrawn": {},
    "totalAddressDeposited": {},
    "totalAddressWithdrawn": {}
}
```

Retrieves a list of bridge transactions based on the specified criteria.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To list bridges use client.list_bridges()
>>> bridge = 'arbitrum'
>>> bridge_data = client.get_bridge_transactions(bridge)
>>> bridge_data[0]
{
    "tx_hash": "0x458bc85a857590a85bef7f8e7dfc4a67c60a8c0d16cab3383f823de228830e38",
    "ts": "2024-01-08T15:43:23.000Z",
    "tx_block": 18963268,
    "tx_from": "0xB639039bd7ba74b21971bA4Eab89a6EEB9512c5C",
    "tx_to": "0xa3A7B6F88361F48403514059F1F16C8E78d60EeC",
    "token": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
    "amount": "1000000000000000000",
    "is_deposit": true,
    "chain": "ethereum",
    "bridge_name": "arbitrum",
    "usd_value": null
}
```

Retrieve all DEXes with all summaries of their volumes and dataType history.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> dex_volumes = client.get_dexes_volume_overview()
>>> dex_volumes.keys()
dict_keys(['totalDataChart', 'totalDataChartBreakdown', 'protocols', 'allChains', 'chain', 'total24h', 'total48hto24h', 'total7d', 'total14dto7d', 'total60dto30d', 'total30d', 'total1y', 'average1y', 'change_1d', 'change_7d', 'change_1m', 'totalVolume7d', 'totalVolume30d', 'change_7dover7d', 'change_30dover30d', 'breakdown24h'])
```

Retrieve all DEXes for a specific chain with all summaries of their volumes and dataType history.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To get all available chains use: client.list_dex_chains()
>>> chain = 'osmosis'
>>> dex_volumes = client.get_dexes_volume_overview_for_chain(chain)
>>> dex_volumes
{
   "totalDataChart":[
      
   ],
   "totalDataChartBreakdown":[
      
   ],
   "protocols":[
      {
         "defillamaId":"383",
         "name":"Osmosis DEX",
         "disabled":false,
         "displayName":"Osmosis DEX",
         "module":"osmosis",
         "category":"Dexes",
         "logo":"https://icons.llamao.fi/icons/protocols/osmosis-dex.jpg",
         "change_1d":-30.2,
         "change_7d":66.12,
         "change_1m":102.38,
         "change_7dover7d":25.05,
         "change_30dover30d":151.18,
         "total24h":37482383.20423146,
         "total48hto24h":53696406.00738978,
         "total7d":334952155.6249361,
         "total30d":1301084253.332036,
         "total14dto7d":267846597.9014448,
         "total60dto30d":517982028.2959299,
         "total1y":4458728450.627966,
         "average1y":342979111.5867666,
         "totalAllTime":24896301747.20423,
         "breakdown24h":{
            "osmosis":{
               "osmosis":37482383.20423146
            }
         },
         "chains":[
            "Osmosis"
         ],
         "protocolType":"protocol",
         "methodologyURL":"https://github.com/DefiLlama/dimension-adapters/blob/master/dexs/osmosis",
         "methodology":{
            "UserFees":"Swap fees paid by users",
            "Fees":"Swap fees paid by users",
            "Revenue":"Percentage of swap fees going to treasury and/or token holders",
            "ProtocolRevenue":"Percentage of swap fees going to treasury",
            "HoldersRevenue":"Money going to governance token holders",
            "SupplySideRevenue":"Liquidity providers revenue"
         },
         "latestFetchIsOk":true,
         "dailyVolume":37482383.20423146,
         "totalVolume7d":22562856.27460225,
         "totalVolume30d":18520905
      }
   ],
   "allChains":[
      "Ethereum",
      "Polygon",
      ...
   ],
   "chain":"Osmosis",
   "total24h":37482383.20423146,
   "total48hto24h":"None",
   "total7d":334952155.6249361,
   "total14dto7d":267846597.9014448,
   "total60dto30d":517982028.2959299,
   "total30d":1301084253.332036,
   "total1y":4458728450.627966,
   "average1y":342979111.5867666,
   "change_1d":-30.2,
   "change_7d":66.12,
   "change_1m":102.38,
   "totalVolume7d":22562856.27460225,
   "totalVolume30d":18520905,
   "change_7dover7d":25.05,
   "change_30dover30d":151.18,
   "breakdown24h":"None"
}
```

Retrieve the summary of the DEX volume with historical data for given protocol.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To get all available protocols use: client.list_dex_protocols()
>>> protocol = 'balancer-v2'
>>> dex_volumes = client.get_summary_of_dex_volume_with_historical_data(protocol)
>>> dex_volumes
{
  "defillamaId": "2611",
  "name": "Balancer V2",
  "displayName": "Balancer V2",
  "disabled": false,
  "logo": "https://icons.llamao.fi/icons/protocols/balancer-v2.png",
  "address": "0xba100000625a3754423978a60c9317c58a424e3d",
  "url": "https://balancer.finance/",
  "description": "Balancer is a protocol for programmable liquidity.",
  "audits": "2",
  "category": "Dexes",
  "twitter": "BalancerLabs",
  "audit_links": [
    "https://github.com/balancer/balancer-v2-monorepo/tree/master/audits"
  ],
  "gecko_id": null,
  "totalDataChart": [...],
  "totalDataChartBreakdown": [...],
  "total24h": 56084858.1706875,
  "total48hto24h": 41069110.65245331,
  "total14dto7d": 230728911.1108181,
  "totalAllTime": null,
  "change_1d": 36.56,
  "module": "balancer",
  "protocolType": "protocol",
  "chains": [
    "Ethereum",
    "Polygon",
    "Arbitrum",
    "Gnosis",
    "Polygon zkEVM",
    "Avalanche",
    "Base"
  ],
  "methodologyURL": "https://github.com/DefiLlama/dimension-adapters/blob/master/dexs/balancer",
  "methodology": {
    "UserFees": "Swap fees paid by users",
    "Fees": "Swap fees paid by users",
    "Revenue": "Percentage of swap fees going to treasury and/or token holders",
    "ProtocolRevenue": "Percentage of swap fees going to treasury",
    "HoldersRevenue": "Money going to governance token holders",
    "SupplySideRevenue": "Liquidity providers revenue"
  },
  "latestFetchIsOk": true,
  "parentProtocol": "parent#balancer",
  "childProtocols": null
}
```

Retrieve all options dexs along with summaries of their options and dataType history.


```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> dex_volumes = client.get_overview_dexes_options()
>>> dex_volumes
{
  "totalDataChart": [],
  "totalDataChartBreakdown": [],
  "protocols": [
    {
      "defillamaId": "2797",
      "name": "Aevo",
      "disabled": false,
      "displayName": "Aevo",
      "module": "aevo",
      "category": "Options",
      "logo": "https://icons.llamao.fi/icons/protocols/aevo.jpg",
      "change_1d": -23.4,
      "change_7d": -29.77,
      "change_1m": 122.13,
      "change_7dover7d": 1.66,
      "change_30dover30d": 9.55,
      "total24h": 212728.47,
      "total48hto24h": 277719.82,
      "total7d": 1324261.1,
      "total30d": 5209075.82,
      "total14dto7d": 1302699.7400000002,
      "total60dto30d": 4754894.889999999,
      "total1y": 0,
      "average1y": 0,
      "totalAllTime": 20480656.29,
      "breakdown24h": {
        "ethereum": {
          "aevo": 212728.47
        }
      },
      "chains": [
        "Ethereum"
      ],
      "protocolType": "protocol",
      "methodologyURL": "https://github.com/DefiLlama/dimension-adapters/blob/master/options/aevo",
      "methodology": {
        "UserFees": "Fees paid by users",
        "Fees": "Fees paid by users",
        "Revenue": "Treasury and token holders revenue",
        "ProtocolRevenue": "Fees going to treasury",
        "HoldersRevenue": "Fees going to governance token holders",
        "SupplySideRevenue": "LPs revenue"
      },
      "latestFetchIsOk": true,
      "dailyPremiumVolume": 212728.47,
      "totalVolume7d": 302908.12,
      "totalVolume30d": 95769.2
    },
    ...
  ],
  "allChains": [
    "Ethereum",
    "Arbitrum",
    "Polygon",
    "Optimism",
    "Fantom",
    "BSC",
    "Sui"
  ],
  "chain": null,
  "total24h": 368277.292197772,
  "total48hto24h": null,
  "total7d": 2676791.6386477044,
  "total14dto7d": 2333178.459171487,
  "total60dto30d": 9743286.862431295,
  "total30d": 10151924.036016885,
  "total1y": 74650323.75070316,
  "average1y": 944940.8069709247,
  "change_1d": -39.45,
  "change_7d": -31.04,
  "change_1m": 67.88,
  "totalVolume7d": 534067.5086466101,
  "totalVolume30d": 219363.67026232922,
  "change_7dover7d": 14.73,
  "change_30dover30d": 4.19,
  "breakdown24h": null,
  "dailyPremiumVolume": 368277.292197772
}
```

Retrieve all options dexs along with summaries of their options and dataType history for specific chain.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To get all available chains use: client.list_options_chains()
>>> chain = 'bsc'
>>> options_volumes = client.get_overview_dexes_options_for_chain(chain)
>>> options_volumes
{
    'totalDataChart': [],
    'totalDataChartBreakdown': [],
    'protocols': [
        {
            'defillamaId': '534',
            'name': 'Thales',
            'disabled': False,
            'displayName': 'Thales',
            'module': 'thales',
            'category': 'Prediction Market',
            'logo': 'https://icons.llamao.fi/icons/protocols/thales.png',
            'change_1d': None,
            'change_7d': None,
            'change_1m': None,
            'change_7dover7d': 0,
            'change_30dover30d': 0,
            'total24h': 0,
            'total48hto24h': 0,
            'total7d': 0,
            'total30d': 0,
            'total14dto7d': 0,
            'total60dto30d': 0,
            'total1y': 3444.9842889749316,
            'average1y': 264.99879145961023,
            'totalAllTime': 7402.343703935723,
            'breakdown24h': {'bsc': {'thales': 0}},
            'chains': ['BSC'],
            'protocolType': 'protocol',
            'methodologyURL': 'https://github.com/DefiLlama/dimension-adapters/blob/master/options/thales',
            'methodology': {},
            'latestFetchIsOk': True,
            'dailyPremiumVolume': 0,
            'totalVolume7d': 0,
            'totalVolume30d': 0
        }
    ],
    'allChains': ['Ethereum', 'Arbitrum', 'Polygon', 'Optimism', 'Fantom', 'BSC', 'Sui'],
    'chain': 'BSC',
    'total24h': 1997.9062889538222,
    'total48hto24h': None,
    'total7d': 1997.9062889538222,
    'total14dto7d': 0,
    'total60dto30d': 99.89919288360352,
    'total30d': 2057.0447988141764,
    'total1y': 17953.493427723526,
    'average1y': 1496.124452310293,
    'change_1d': 0,
    'change_7d': 0,
    'change_1m': 0,
    'totalVolume7d': 0,
    'totalVolume30d': 0,
    'change_7dover7d': 0,
    'change_30dover30d': 1959.12,
    'breakdown24h': None
}
```


Retrieve the summary of options volume with historical data for a given protocol.
To list available options protocols use: `client.list_options_protocols()`

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To get all available chains use: client.list_options_protocols()
>>> protocol = 'hegic'
>>> options_volumes = client.get_summary_of_options_volume_with_historical_data_for_protocol(protocol)
>>> options_volumes
{
  "defillamaId": "128",
  "name": "Hegic",
  "displayName": "Hegic",
  "disabled": false,
  "logo": "https://icons.llamao.fi/icons/protocols/hegic.jpg",
  "address": "0x584bC13c7D411c00c01A62e8019472dE68768430",
  "url": "https://www.hegic.co/ ",
  "description": "Hegic is an on-chain peer-to-pool options trading protocol on Arbitrum. You can trade ETH and WBTC ATM / OTM Calls / Puts & One-click Option Strategies on Hegic",
  "audits": "2",
  "category": "Options",
  "twitter": "HegicOptions",
  "audit_links": [
    "https://github.com/peckshield/publications/blob/master/audit_reports/PeckShield-Audit-Report-Hegic-v1.0.pdf",
    "https://github.com/hegic/contracts/blob/main/packages/herge/docs/PeckShield-Audit-Report-Hegic-Herge-Protocol-Upgrade-v1.0.pdf"
  ],
  "gecko_id": "hegic",
  "totalDataChart": [...],
  "totalDataChartBreakdown": [...],
  "total24h": 1764.23,
  "total48hto24h": 11353.31,
  "total14dto7d": 135517.19,
  "totalAllTime": 6803534.82,
  "change_1d": -84.46,
  "module": "hegic",
  "protocolType": "protocol",
  "chains": [
    "Arbitrum"
  ],
  "methodologyURL": "https://github.com/DefiLlama/dimension-adapters/blob/master/options/hegic",
  "methodology": {
    "UserFees": "Fees paid by users",
    "Fees": "Fees paid by users",
    "Revenue": "Treasury and token holders revenue",
    "ProtocolRevenue": "Fees going to treasury",
    "HoldersRevenue": "Fees going to governance token holders",
    "SupplySideRevenue": "LPs revenue"
  },
  "latestFetchIsOk": true,
  "childProtocols": null
}
```

Retrieve the fees and revenues for all protocols.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> fees = client.get_fees_and_revenues_for_all_protocols()
>>> fees
{
  "totalDataChart": [...],
  "totalDataChartBreakdown": [...],
  "protocols": [...],
  "allChains": [...
  ],
  "chain": null,
  "total24h": 29714721.42039948,
  "total48hto24h": null,
  "total7d": 193609683.4283434,
  "total14dto7d": 226743155.4572359,
  "total60dto30d": 848816572.6460838,
  "total30d": 1129110286.2909887,
  "total1y": 7287498033.002101,
  "average1y": 2461161.105370538,
  "change_1d": 8.29,
  "change_7d": 1.72,
  "change_1m": -0.01,
  "totalVolume7d": 29213120.626264498,
  "totalVolume30d": 29718139.56076277,
  "change_7dover7d": -14.61,
  "change_30dover30d": 33.02,
  "breakdown24h": null,
  "dailyRevenue": 11459829.023428591,
  "dailyUserFees": 26535308.92626263,
  "dailyHoldersRevenue": 8418660.76396098,
  "dailySupplySideRevenue": 9786193.767494084,
  "dailyProtocolRevenue": 1671804.2239159911,
  "dailyBribesRevenue": 170758.2092075268,
  "dailyTokenTaxes": 21360.880083969234
}
```

Retrieve fees and revenues for all protocols for a given chain.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To get all available chains use: client.list_fees_chains()
>>> chain = 'moonbeam'
>>> fees = client.get_fees_and_revenues_for_all_protocols_for_chain(chain)
>>> fees
{
  "totalDataChart": [],
  "totalDataChartBreakdown": [],
  "protocols": [],
  "allChains": [
    ...
  ],
  "chain": "Moonbeam",
  "total24h": 2473.132558684688,
  "total48hto24h": null,
  "total7d": 19076.514688008763,
  "total14dto7d": 16888.563348835094,
  "total60dto30d": 51612.67360078471,
  "total30d": 100955.97328763249,
  "total1y": 691217.3378974971,
  "average1y": 8429.479730457275,
  "change_1d": -4.17,
  "change_7d": -22.03,
  "change_1m": 8.36,
  "totalVolume7d": 3171.932128273157,
  "totalVolume30d": 2282.3008427249947,
  "change_7dover7d": 12.96,
  "change_30dover30d": 95.6,
  "breakdown24h": null,
  "dailyRevenue": 622.9239479878493,
  "dailyUserFees": 2473.022235571788,
  "dailyHoldersRevenue": 193.0434303870515,
  "dailySupplySideRevenue": 1850.2086106968386,
  "dailyProtocolRevenue": 622.8014479878493
}
```

Retrieve the summary of fees and revenue for a specific protocol.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
# To get all available chains use: client.list_fees_chains()
>>> protocol = 'fantom'
>>> fees = client.get_summary_of_protocols_fees_and_revenue(protocol)
>>> fees
{
  "defillamaId": "3513",
  "name": "Fantom",
  "displayName": "Fantom",
  "disabled": false,
  "logo": "https://icons.llamao.fi/icons/chains/rsz_fantom.jpg",
  "category": "Chain",
  "gecko_id": "fantom",
  "totalDataChart": [...],
  "totalDataChartBreakdown": [...],
  "total24h": 2040.30422365229,
  "total48hto24h": 3221.5813902878276,
  "total14dto7d": 25536.00612584981,
  "totalAllTime": null,
  "change_1d": -36.67,
  "module": "fantom",
  "protocolType": "chain",
  "chains": [
    "Fantom"
  ],
  "methodologyURL": "https://github.com/DefiLlama/dimension-adapters/blob/master/fees/fantom.ts",
  "methodology": {
    "UserFees": "Gas fees paid by users",
    "Fees": "Gas fees paid by users",
    "Revenue": "Burned coins"
  },
  "latestFetchIsOk": true,
  "childProtocols": null
}
```

Retrieve the current prices of tokens by contract address.
To see all available chains use `client.list_chains()`
To see all available coingecko ids use `client.get_coingecko_coin_ids()`
You can use coingecko as a chain, and then use coin gecko ids instead of contract addresses:
`coins = "coingecko:uniswap,coingecko:ethereum"` or `coins = Coin("coingecko:uniswap")` or
`coins = {"chain": "coingecko", "address": "uniswap"}`

```Python
>>> from dfllama import DefiLlamaClient, Coin
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
{
    'coins': {
        'ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984': {
            'decimals': 18,
            'symbol': 'UNI',
            'price': 6.24,
            'timestamp': 1704744330,
            'confidence': 0.99
        }
    }
}
```


Retrieve the historical prices of tokens by contract address.

```Python
>>> from dfllama import DefiLlamaClient, Coin
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
{
    'coins': {
        'ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984': {
            'decimals': 18,
            'symbol': 'UNI',
            'price': 9.778883768551262,
            'timestamp': 1649999936
        }
    }
}
```

Retrieve token prices at regular time intervals.

```Python
>>> from dfllama import DefiLlamaClient, Coin
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
{
    'coins': {
        'ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984': {
            'decimals': 18,
            'symbol': 'UNI',
            'price': 9.778883768551262,
            'timestamp': 1649999936
        }
    }
}
```

Retrieve token price percentage change over time.

```Python
>>> from dfllama import DefiLlamaClient, Coin
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
{
  'coins': {
    'ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984': 0.16155039918093603
    }
}
```

Retrieve the earliest timestamped price record for the given coins.

```Python
>>> from dfllama import DefiLlamaClient, Coin
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
{
    'coins': {
        'ethereum:0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984': {
            'symbol': 'UNI',
            'price': 2.9696706531528196,
            'timestamp': 1600308306
        },
        'coingecko:ethereum': {
            'symbol': 'ETH',
            'price': 2.83162,
            'timestamp': 1438905600
        }
    }
}
```

Retrieve the closest block to the given timestamp for a specific chain.

```Python
>>> from dfllama import DefiLlamaClient, Coin
>>> client = DefiLlamaClient()
>>> chain = 'ethereum'
>>> prices = client.get_the_closest_block_to_timestamp(chain, timestamp=1600308306)
>>> prices
{'height': 10876852, 'timestamp': 1600308344}
```

## Run tests
```bash
make test 
# or 
pytest tests/ -vv -ss

# pytest cov
make cov
# or 
coverage run --source=dfllama -m pytest tests/ -vv -ss && coverage report -m
```


## Contributing

You're welcome to add pull requests.


## Todo
- Pagination (most endpoints doesn't support pagination, so it needs to be done on client side)
- Possibility to use different types of data fromat/timestamp in some endpoints - with automatic conversion 
- Add pandas support for analytics (Consider)
