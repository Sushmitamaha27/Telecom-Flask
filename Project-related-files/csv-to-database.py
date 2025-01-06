import pandas as pd
import psycopg2
from psycopg2 import sql
import csv

# Database connection setup
try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        user="postgres",
        password="root",
        dbname="Telecom_database"
    )
    conn.autocommit = False
    print("Successfully connected to the PostgreSQL database")
except psycopg2.Error as e:
    print(f"Error connecting to database: {e}")
    exit()

cursor = conn.cursor()

# File path for the CSV file
file_path = "C:/Users/sushm/Desktop/telecom_data_with_flask/telecom_data.csv"
failed_records_file = "failure_insertion.csv"

# Prepare failure file with headers
with open(file_path, mode='r') as original_csv:
    reader = csv.reader(original_csv)
    headers = next(reader)

with open(failed_records_file, mode='w', newline='') as failure_csv:
    writer = csv.writer(failure_csv)
    writer.writerow(headers)

# Reading the CSV file in chunks
chunk_size = 1000
for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    for _, row in chunk.iterrows():
        try:
            # Insert into Customers table
            cursor.execute(
                """
                INSERT INTO Customers (customer_id, is_new_customer)
                VALUES (%s, %s)
                ON CONFLICT (customer_id) DO NOTHING
                """,
                (row['CustomerID'], row['IsNewCustomer'] == 'Yes')
            )

            # Insert into Technology table
            cursor.execute(
                """
                INSERT INTO Technology (technology_id, technology_type)
                VALUES (%s, %s)
                ON CONFLICT (technology_id) DO NOTHING
                """,
                (row['TechnologyID'], row['Technology'])
            )

            # Insert into Services table
            cursor.execute(
                """
                INSERT INTO Services (service_id, service_type)
                VALUES (%s, %s)
                ON CONFLICT (service_id) DO NOTHING
                """,
                (row['ServiceID'], row['ServiceType'])
            )

            # Insert into Orders table
            cursor.execute(
                """
                INSERT INTO Orders (
                    order_id, customer_id, service_id, technology_id, order_date,
                    start_date, end_date, order_status, contract_type,
                    price_per_month, installation_fee
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (order_id) DO UPDATE SET
                    order_status = EXCLUDED.order_status,
                    end_date = EXCLUDED.end_date
                """,
                (
                    row['OrderID'], row['CustomerID'], row['ServiceID'], row['TechnologyID'],
                    row['OrderDate'], row['StartDate'], row['EndDate'], row['OrderStatus'],
                    row['ContractType'], row['PricePerMonth'], row['InstallationFee']
                )
            )

            # Insert into Contracts table
            cursor.execute(
                """
                INSERT INTO Contracts (order_id, contract_type, start_date, end_date)
                VALUES (%s, %s, %s, %s)
                """,
                (row['OrderID'], row['ContractType'], row['StartDate'], row['EndDate'])
            )

        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")
            # Write the failed record to failure_insertion.csv
            with open(failed_records_file, mode='a', newline='') as failure_csv:
                writer = csv.writer(failure_csv)
                writer.writerow(row.values)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Data has been successfully inserted in chunks. Failed records are logged in failure_insertion.csv.")
