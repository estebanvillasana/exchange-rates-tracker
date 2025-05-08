import requests
import pandas as pd
from datetime import date

currencies = ['usd', 'eur', 'mxn', 'rub', 'gel', 'gbp', 'jpy', 'aud', 'aed']
base_currencies = currencies

today = date.today().isoformat()
rows = []

for base in base_currencies:
    try:
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        rate_row = {'date': data['date'], 'base': base}
        for target in currencies:
            rate_row[target] = 1.0 if target == base else data.get(base, {}).get(target)
        rows.append(rate_row)
    except Exception as e:
        print(f"Error fetching {base}: {e}")

df = pd.DataFrame(rows)
df.to_csv("exchange_rates.csv", index=False)
