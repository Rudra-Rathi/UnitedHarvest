import csv
import random
from datetime import datetime, timedelta

# Parameters
total_rows = 1000
product_ids = [1, 2, 3, 4, 5]  # Assume 5 products
start_date = datetime(2025, 5, 1)

# Generate synthetic data
rows = []
for i in range(1, total_rows + 1):
    product_id = random.choice(product_ids)
    price = round(random.uniform(20, 80), 2)
    date = start_date + timedelta(days=random.randint(0, 30))
    timestamp = date.replace(
        hour=random.randint(8, 17),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
        microsecond=random.randint(0, 999999)
    )
    rows.append([i, product_id, price, timestamp])

# Save to CSV
with open("synthetic_mandi_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "product_id", "price", "date"])
    writer.writerows(rows)

print("Generated 1000 rows in 'synthetic_mandi_data.csv'")
# This code generates a CSV file with 1000 rows of synthetic data for product prices over time.
# The data includes a product ID, price, and timestamp for each entry.