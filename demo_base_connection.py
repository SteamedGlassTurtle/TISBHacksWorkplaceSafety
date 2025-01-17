import mysql.connector

# Connect to MySQL server (without specifying a database)
connection = mysql.connector.connect(
    host='localhost',        # Replace with your host
    user='root',    # Replace with your username
    password='jerome1234', # Replace with your password
    database='employees'
)

cursor = connection.cursor()

# Create the database if it doesn't exist
try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS employees;")
    print("Database 'employees' created or already exists.")
except mysql.connector.Error as e:
    print(f"Error creating database: {e}")
finally:
    cursor.close()
    connection.close()
