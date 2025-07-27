import csv

# Define sample data
data = [
    ["product_id", "sku", "product_name"],
    ["1", "SKU123", "Apple iPhone 14 Pro"],
    ["2", "sku123", "apple iphone14 pro"],
    ["3", "SKU456", "Samsung Galaxy S23"],
    ["4", "sku456", "Samsung Galaxy S23"],
    ["5", "SKU789", "Pixel 8"]
]

# Write to CSV
with open("data/raw_products.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("raw_products.csv file created successfully in data/ folder.")
