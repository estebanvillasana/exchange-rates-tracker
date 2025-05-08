import pandas as pd
import requests
from datetime import date
import os

# Settings
currencies = ['usd', 'eur', 'mxn', 'rub', 'gel', 'gbp', 'jpy', 'aud', 'aed']
today = date.today().isoformat()
csv_path = "exchange_rates.csv"
sep = ","  # or ";" if needed

# Load existing data
if os.path.exists(csv_path):
    df_existing = pd.read_csv(csv_path, sep=sep)
else:
    df_existing = pd.DataFrame()

# Check if today's rates already exist
if not df_existing.empty and today in df_existing['date'].values:
    print("✅ Today's data already exists.")
    exit(0)

# Build new rows
new_rows = []

for i, base in enumerate(currencies, start=1):
    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        actual_date = data['date']
        rates = data[base]

        row = {'date': today, 'id': i, 'code': base}
        for target in currencies:
            if base == target:
                row[target] = 1.0
            else:
                value = rates.get(target)
                if value is None:
                    # fallback to last available rate
                    recent = df_existing[(df_existing['code'] == base) & (df_existing[target].notnull())]
                    if not recent.empty:
                        value = recent.sort_values('date', ascending=False).iloc[0][target]
                row[target] = value
        new_rows.append(row)

    except Exception as e:
        print(f"⚠️ Failed to fetch {base.upper()} rates: {e}")

# Save updated file
df_new = pd.DataFrame(new_rows)
df_all = pd.concat([df_existing, df_new], ignore_index=True)
df_all.to_csv(csv_path, index=False, sep=sep)

print(f"✅ Appended today's rates ({today}) to {csv_path}")
