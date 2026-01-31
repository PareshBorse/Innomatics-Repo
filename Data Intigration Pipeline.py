import pandas as pd
import json
import sqlite3
import re

orders_df = pd.read_csv('orders.csv')

with open('users.json', 'r') as f:
    users_data = json.load(f)
users_df = pd.DataFrame(users_data)


with open('restaurants.sql', 'r') as f:
    sql_script = f.read()

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

try:
    cursor.executescript(sql_script)
    restaurants_df = pd.read_sql_query("SELECT * FROM restaurants", conn)
except Exception as e:

    print(f"SQL execution error: {e}")

print("Orders Head:")
print(orders_df.head())
print("\nUsers Head:")
print(users_df.head())
print("\nRestaurants Head:")
print(restaurants_df.head())

merged_df = orders_df.merge(users_df, on='user_id', how='left')

merged_df = merged_df.merge(restaurants_df, on='restaurant_id', how='left', suffixes=('', '_rest'))

merged_df.to_csv('final_food_delivery_dataset.csv', index=False)

print("\nMerged Data Info:")
print(merged_df.info())
print("\nMerged Data Head:")
print(merged_df.head())