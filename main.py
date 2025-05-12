import os
import requests
import json
from datetime import datetime
import pandas as pd
import argparse
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

api_key = os.getenv("API_KEY")

# Default token list (used when --cp flag is passed)
DEFAULT_TOKENS_NEW = [
    "DFI.Money (YFII)",
    "FIO Protocol (FIO)",
    "Bonfida (FIDA)",
    "Reef (REEF)",
    "Harvest Finance (FARM)",
    "Paris Saint Germain (PSG)",
    "Perpetual Protocol (PERP)",
    "Alien Worlds (TLM)",
    "Radicle (RAD)",
    "Cream Finance (CREAM)",
    "THORChain (RUNE)",
    "Frontier (FRONT)",
    "Acala Token (ACA)",
    "BenQi (QI)",
    "Bancor (BNT)",
    "My Neighbor Alice (ALICE)",
    "Loom Network (LOOM)",
    "WinkLink (WIN)",
    "Bake (BAKE)",
    "Hooked Protocol (HOOK)",
    "Steem (STEEM)",
    "CyberConnect (CYBER)",
    "Sun (SUN)",
    "Hive (HIVE)",
    "Smooth Love Potion (SLP)",
    "Coin98 (C98)",
    "Venus (XVS)",
    "Storj (STORJ)",
    "BabyDoge (BABYDOGE)",
    "Ontology (ONT)",
    "Tellor (TRB)",
    "Harmony (ONE)",
    "Yearn.Finance (YFI)",
    "Jupiter (JUP)",
    "Arkham (ARKM)",
    "Illuvium (ILV)",
    "Basic Attention Token (BAT)",
    "Enjin Coin (ENJ)",
    "Celo (CELO)",
    "Osmosis (OSMO)",
    "Zilliqa (ZIL)",
    "Terra (LUNA)",
    "Memecoin (MEME)",
    "Dash (DASH)",
    "Manta Network (MANTA)",
    "Green Metaverse Token (GMT)",
    "ConstitutionDAO (PEOPLE)",
    "Safepal (SFP)",
    "IoTeX (IOTX)",
    "Kava (KAVA)",
    "Trustwallet (TWT)",
    "1inch (1INCH)",
    "Terra Classic (LUNC)",
    "LayerZero (ZRO)",
    "ApeCoin (APE)",
    "Cake (CAKE)",
    "Compound (COMP)",
    "ZkSync (ZK)",
    "Sats (SATS)",
    "Chiliz (CHZ)",
    "Decentraland (MANA)",
    "Book of Meme (BOME)",
    "Worldcoin (WLD)",
    "MultiversX (EGLD)",
    "The Sandbox (SAND)",
    "Ordi (ORDI)",
    "BitTorrent (BTT)",
    "Gala (GALA)",
    "DYDX (DYDX)",
    "Tezos (XTZ)",
    "EOS (EOS)",
    "Axie Infinity (AXS)",
    "Quant (QNT)",
    "Sei (SEI)",
    "Algorand (ALGO)",
    "Core (CORE)",
    "Celestia (TIA)",
    "Sonic (S)",
    "Pyth Network (PYTH)",
    "Theta Token (THETA)",
    "Floki (FLOKI)",
    "Bonk (BONK)",
    "The Graph (GRT)",
    "AAVE (AAVE)",
    "Dogwifhat (WIF)",
    "Optimism (OP)",
    "Render Token (RENDER)",
    "Injective Protocol (INJ)",
    "Vechain (VET)",
    "Cosmos (ATOM)",
    "Filecoin (FIL)",
    "Stellar Lumens (XLM)",
    "Aptos (APT)",
    "Ethereum Classic (ETC)",
    "Uniswap (UNI)",
    "Internet Computer (ICP)",
    "Pepe (PEPE)",
    "Polygon (MATIC)",
    "Litecoin (LTC)",
    "Near Protocol (NEAR)",
    "Chainlink (LINK)",
    "Polkadot (DOT)",
    "Bitcoin Cash (BCH)",
    "Shiba Inu (SHIB)",
    "Avalanche (AVAX)",
    "Tron (TRX)",
    "Cardano (ADA)",
    "Toncoin (TON)",
    "Dogecoin (DOGE)",
    "Ripple (XRP)",
    "USD Coin (USDC)",
    "Solana (SOL)",
    "Binance (BNB)",
    "Tether (USDT)",
    "Ethereum (ETH)",
    "Bitcoin (BTC)",
    "SuperFarm (SUPER)",
    "Fetch.ai (FET)",
    "Pi (PI)",
    "Hedra (HBAR)",
    "Aixbt (AIXBT)",
    "Ice Open Network (ICE)",
    "Stacks (STX)",
    "Peanut The Squirrel (PNUT)",
    "Official Trum (TRUMP)",
    "Dogs (DOGS)",
    "Sui (SUI)",
]


def get_amount_abbrv(price: int) -> str:
    if price is None:
        return None
    if price > 1e12:
        return f"{price / 1e12:.2f}T"
    elif price > 1e9:
        return f"{price / 1e9:.2f}B"
    elif price > 1e6:
        return f"{price / 1e6:.2f}M"
    elif price > 1e3:
        return f"{price / 1e3:.2f}K"
    return str(price)


def get_token_symbols(tokens_new):
    return [
        token.split(" (")[1].replace("(", "").replace(")", "") for token in tokens_new
    ]


def fetch_crypto_data(symbols):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": api_key}
    params = {"symbol": ",".join(symbols)}
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def build_crypto_table(data):
    crypto_table = {
        "Name": [],
        "Symbol": [],
        "Price": [],
        "Market Cap": [],
        "Volume(24h)": [],
        "Supply %": [],
    }
    for crypto in data["data"].values():
        crypto_table["Name"].append(crypto.get("name"))
        crypto_table["Symbol"].append(crypto.get("symbol"))
        quote = crypto.get("quote", {}).get("USD", {})
        crypto_table["Price"].append(quote.get("price"))
        crypto_table["Market Cap"].append(get_amount_abbrv(quote.get("market_cap")))
        crypto_table["Volume(24h)"].append(quote.get("volume_24h"))
        circ = crypto.get("circulating_supply", 0)
        total = crypto.get("total_supply", 0)
        crypto_table["Supply %"].append(round((circ / total) * 100, 2) if total else "N/A")
    return crypto_table


def save_to_excel(dataframe, output_path):
    dataframe.sort_values(by="Price", ascending=False).to_excel(
        output_path, index=False
    )
    print(f"Exported to {output_path}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--symbols", nargs="+", help="Symbols to fetch (e.g. BTC ETH SOL)"
    )
    parser.add_argument(
        "-o", "--output", default="crypto_table.xlsx", help="Output Excel path"
    )
    parser.add_argument(
        "--cp", action="store_true", help="Use default predefined symbols"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.cp or not args.symbols:
        tokens_new = DEFAULT_TOKENS_NEW
        tokens_updated = get_token_symbols(tokens_new)
    else:
        tokens_updated = args.symbols

    try:
        data = fetch_crypto_data(tokens_updated)
        crypto_table = build_crypto_table(data)
        df = pd.DataFrame(crypto_table)
        existing_symbols = df["Symbol"].str.lower().tolist()
        missing = [val for val in tokens_updated if val.lower() not in existing_symbols]
        if missing:
            print(f"Missing symbols: {missing}")
            df["Symbol"] = pd.concat(
                [df["Symbol"], pd.Series(missing)], ignore_index=True
            )
        save_to_excel(df, args.output)
    except Exception as e:
        print(f"Error fetching data: {e}")


if __name__ == "__main__":
    main()
