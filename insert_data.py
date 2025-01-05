import mysql.connector
from datetime import datetime
import json

# Database Configuration
db_config = {
    'host': 'localhost',         # Replace with your database host
    'user': 'root',              # Your MySQL username
    'password': 'Tarun9392440350', # Your MySQL password
    'database': 'robo'      # Your database name
}

# Function to insert packaged goods into the database
def insert_packaged_goods(data):
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert query
        insert_query = """
            INSERT INTO  grocery(timestamp, brand, expiry_date, count, expired, expected_life_span_days)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Prepare data for insertion
        for item in data:
            if "TotalItems" in item:  # Skip "TotalItems" object
                continue
            timestamp = item['Timestamp']
            brand = item['Brand']
            expiry_date = None if item['Expiry date'] == "NA" else datetime.strptime(item['Expiry date'], "%d/%m/%Y").date()
            count = item['Count']
            expired = item['Expired']
            expected_life_span_days = None if item['Expected life span (Days)'] == "NA" else item['Expected life span (Days)']

            # Insert record into the database
            cursor.execute(insert_query, (timestamp, brand, expiry_date, count, expired, expected_life_span_days))

        # Commit the transaction
        connection.commit()
        print("Packaged goods data inserted successfully!")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# # Example processed data (mock response)
# processed_data = [
#     {
#         "Sl no": 1,
#         "Timestamp": "2024-11-29T05:14:01",
#         "Brand": "Parle-G",
#         "Expiry date": "12/9/2027",
#         "Count": 5,
#         "Expired": "No",
#         "Expected life span (Days)": 1045
#     },
#     {
#         "Sl no": 2,
#         "Timestamp": "2024-11-29T05:14:01",
#         "Brand": "Tata Tea",
#         "Expiry date": "9/5/2026",
#         "Count": 2,
#         "Expired": "No",
#         "Expected life span (Days)": 645
#     },
#     {
#         "Sl no": 3,
#         "Timestamp": "2024-11-29T05:14:01",
#         "Brand": "Horlicks",
#         "Expiry date": "1/11/2024",
#         "Count": 1,
#         "Expired": "Yes",
#         "Expected life span (Days)": 0
#     }
# ]

# # Insert data into the database
# insert_packaged_goods(processed_data)


def insert_fresh_produce(data):
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert query (excluding sl_no, which auto-increments)
        insert_query = """
            INSERT INTO fresh(produce, freshness, expected_life_span_days, timestamp)
            VALUES (%s, %s, %s, %s)
        """

        # Prepare and execute the insert for each item in the data
        for item in data:
            produce = item['Produce']
            freshness = int(item['Freshness'])
            expected_life_span_days = int(item['Expected life span (Days)'])
            timestamp = item['Timestamp']

            cursor.execute(insert_query, (produce, freshness, expected_life_span_days, timestamp))

        # Commit the transaction
        connection.commit()
        print("Fresh produce data inserted successfully!")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# # Example fresh produce data
# fresh_data = [
#     {'Sl no': '1', 'Produce': 'Orange', 'Freshness': '3', 'Expected life span (Days)': '0', 'Timestamp': '2024-12-30 17:48:48'},
#     {'Sl no': '2', 'Produce': 'Apple', 'Freshness': '2', 'Expected life span (Days)': '0', 'Timestamp': '2024-12-30 17:48:48'},
#     {'Sl no': '3', 'Produce': 'Apple', 'Freshness': '1', 'Expected life span (Days)': '0', 'Timestamp': '2024-12-30 17:48:48'},
#     {'Sl no': '4', 'Produce': 'Pear', 'Freshness': '1', 'Expected life span (Days)': '0', 'Timestamp': '2024-12-30 17:48:48'},
#     {'Sl no': '5', 'Produce': 'Apple', 'Freshness': '2', 'Expected life span (Days)': '0', 'Timestamp': '2024-12-30 17:48:48'},
#     {'Sl no': '6', 'Produce': 'Apple', 'Freshness': '1', 'Expected life span (Days)': '0', 'Timestamp': '2024-12-30 17:48:48'}
# ]

# # Insert the fresh produce data into the database
# insert_fresh_produce(fresh_data)
