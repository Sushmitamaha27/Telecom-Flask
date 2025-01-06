import csv
import random
from datetime import datetime, timedelta

# File path for the output CSV
output_file = "telecom_data.csv"  # Unique data CSV

# Generate random dates within a range
def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# Define constants for data generation
start_date_range = datetime(2022, 1, 1)
end_date_range = datetime(2023, 12, 31)
service_types = ["Broadband", "TV"]
technology_options = {
    "Broadband": ["DSL", "VDSL", "GPON", "PON"],
    "TV": ["IPTV", "Satellite", "OTT"]
}
order_statuses = ["Active", "Pending", "Completed", "Cancelled"]
contract_types = ["Freehold", "1-Year", "2-Year", "3-Year"]

# Create unique mappings for ServiceID and TechnologyID
service_id_mapping = {service: idx + 1 for idx, service in enumerate(service_types)}
unique_technologies = {tech for techs in technology_options.values() for tech in techs}
technology_id_mapping = {tech: idx + 1 for idx, tech in enumerate(unique_technologies)}

# Generate unique telecom data
num_rows = 100  # Number of rows to generate
existing_ids = set()  # Track unique IDs
new_data = []

for _ in range(num_rows):
    # Ensure unique OrderID
    while True:
        order_id = random.randint(1000, 9999)
        if order_id not in existing_ids:
            existing_ids.add(order_id)
            break

    customer_id = random.randint(1, 5000)
    is_new_customer = random.choice(["Yes", "No"])
    service_type = random.choice(service_types)
    service_id = service_id_mapping[service_type]
    technology = random.choice(technology_options[service_type])
    technology_id = technology_id_mapping[technology]

    start_date = random_date(start_date_range, end_date_range)
    end_date = random_date(start_date, end_date_range)
    order_status = random.choice(order_statuses)
    contract_type = random.choice(contract_types)
    price_per_month = round(random.uniform(20.0, 100.0), 2)
    installation_fee = round(random.uniform(50.0, 200.0), 2)
    order_date = random_date(start_date_range, start_date)

    # Append row to new_data
    new_data.append([
        order_id,
        customer_id,
        is_new_customer,
        service_type,
        service_id,
        technology,
        technology_id,
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d") if end_date else "",
        order_status,
        contract_type,
        price_per_month,
        installation_fee,
        order_date.strftime("%Y-%m-%d"),
    ])

# Write to new CSV file
header = [
    "OrderID",
    "CustomerID",
    "IsNewCustomer",
    "ServiceType",
    "ServiceID",
    "Technology",
    "TechnologyID",
    "StartDate",
    "EndDate",
    "OrderStatus",
    "ContractType",
    "PricePerMonth",
    "InstallationFee",
    "OrderDate",
]

with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(new_data)

print(f"Telecom data with {len(new_data)} unique rows has been written to {output_file}")
