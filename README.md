# 🪙 Crypto Market Data Exporter

A Python script to fetch the latest cryptocurrency data using the CoinMarketCap API and export it to an Excel file. You can specify your own symbols or use a curated default list of tokens.

---

## 🚀 Features

- Fetches **latest market data** for cryptocurrencies via the CoinMarketCap API.
- Outputs data including **name, symbol, price, market cap, volume (24h), and supply %**.
- Option to use a **default list** of curated tokens with `--cp`.
- Automatically saves results in **Excel format**, sorted by price.
- Clean modular structure for easy extension or reuse.

---

## 📦 Requirements

- Python 3.7+
- `pandas`
- `requests`
- `openpyxl`
- `python-dotenv`

Install requirements:

```bash
pip install -r requirements.txt
```

---

## 🔑 API Setup

1. Create a `.env` file in the root directory of the project.
2. Add your CoinMarketCap API key:

```
API_KEY=your_api_key_here
```

You can get a free API key from [CoinMarketCap Developer Portal](https://pro.coinmarketcap.com/).

---

## ⚙️ Usage

### Basic usage (default output: `crypto_table.xlsx`)

```bash
python crypto_exporter.py -s BTC ETH SOL
```

### Use default token list

```bash
python crypto_exporter.py --cp
```

### Customize output file path

```bash
python crypto_exporter.py -s BTC ETH -o my_output.xlsx
```

---

## 📋 Arguments

| Argument       | Description                                         |
|----------------|-----------------------------------------------------|
| `-s`, `--symbols` | List of crypto symbols (e.g., `BTC ETH SOL`)       |
| `-o`, `--output`  | Output Excel file path (default: `crypto_table.xlsx`) |
| `--cp`            | Use predefined list of ~100 curated tokens        |

---

## 📁 Output

An Excel file with the following columns:

- **Name**
- **Symbol**
- **Price**
- **Market Cap**
- **Volume(24h)**
- **Supply %**

---

## 🛠️ File Structure

```
crypto_exporter.py
.env
README.md
requirements.txt
```

---

## ✅ Example

```bash
python main.py --cp -o top_100_cryptos.xlsx
```

This command exports the default token list data into `top_100_cryptos.xlsx`.

---

## ⚠️ Notes

- Ensure your API key's quota isn't exceeded.
- If a symbol is missing in the response, it will be printed and added with an empty row in the Excel file.

---

## 📄 License

MIT License. Feel free to use and modify!
