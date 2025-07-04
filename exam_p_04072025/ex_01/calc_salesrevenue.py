import csv
import datetime
import json
import os

data = []

# read csv
try:
    with open('sales.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['Date'], '%Y-%m-%d').date()
                product = row['Product']
                category = row['Category']
                quantity = int(row['Quantity'])
                price = float(row['Price'])

                data.append({
                    'Date': date,
                    'Product': product,
                    'Category': category,
                    'Quantity': quantity,
                    'Price': price
                })

            except Exception as e:
                print(f"Fehler beim Parsen einer Zeile: {e}")

except FileNotFoundError:
    print("Datei sales.csv wurde nicht gefunden.")
    exit()

# calc revenue
daily_revenue = {}
category_revenue = {}

for row in data:
    revenue = row['Quantity'] * row['Price']

    date_key = row['Date']
    daily_revenue[date_key] = daily_revenue.get(date_key, 0) + revenue

    cat_key = row['Category']
    category_revenue[cat_key] = category_revenue.get(cat_key, 0) + revenue

# create json
os.makedirs('data_json', exist_ok=True)

with open('data_json/daily_revenue.json', 'w', encoding='utf-8') as f:
    json.dump({str(k): round(v, 2) for k, v in daily_revenue.items()}, f, indent=2)

with open('data_json/category_revenue.json', 'w', encoding='utf-8') as f:
    json.dump({k: round(v, 2) for k, v in category_revenue.items()}, f, indent=2)

# Top3
print("Top 3 Tage nach Umsatz:")
for date, revenue in sorted(daily_revenue.items(), key=lambda x: x[1], reverse=True)[:3]:
    print(f"{date}: {revenue:.2f} €")

print("\nTop 3 Kategorien nach Umsatz:")
for cat, revenue in sorted(category_revenue.items(), key=lambda x: x[1], reverse=True)[:3]:
    print(f"{cat}: {revenue:.2f} €")
