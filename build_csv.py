import json
import pandas as pd

# Load your country codes JSON so we can filter out regions
with open('country_codes.json', 'r') as f:
    MASTER_TABLE = json.load(f)

files = {
    'SP.POP.TOTL': 'population.json',
    'NY.GDP.PCAP.CD': 'gdp.json',
    'SP.DYN.LE00.IN': 'life.json'
}

all_data = []

for indicator, filename in files.items():
    print(f"Processing {indicator}...")
    with open(filename, 'r') as f:
        data = json.load(f)[1]
    
    for item in data:
        if item['value'] is not None:
            country_name = item['country']['value']
            
            # --- CRITICAL FIX: Only keep countries that exist in your MASTER_TABLE ---
            if country_name in MASTER_TABLE:
                all_data.append({
                    'country': country_name,
                    'indicator': indicator,
                    'year': int(item['date']),
                    'value': float(item['value'])
                })
            # ----------------------------------------------------------------------

df = pd.DataFrame(all_data)
df.to_csv('local_data.csv', index=False)
print("✅ Done! local_data.csv has been created with ONLY valid countries.")