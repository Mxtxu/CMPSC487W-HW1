import mysql.connector

# Create a connection to the MySQL server
conn = mysql.connector.connect(
    host="localhost",    # Your MySQL server hostname
    user="yourusername", # Your MySQL username
    password="yourpassword", # Your MySQL password
    database="yourdatabase"  # Database name
)

# Create a cursor object using the connection
cursor = conn.cursor()

# Execute SQL query
cursor.execute("SELECT DATABASE()")

# Fetch and display result
result = cursor.fetchone()
print("Connected to database:", result)

# Close the cursor and connection
cursor.close()