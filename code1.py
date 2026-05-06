import mysql.connector

# Step 1: Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",           # your MySQL username
    password="AusNet$O33",  # the password you set during MySQL install
    database="banking_app"
)
cursor = conn.cursor()

# Step 2: Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        balance DECIMAL(10, 2)
    )
''')

# Step 3: Insert data
cursor.execute("INSERT INTO accounts VALUES (1, 'Maria', 500.00)")
conn.commit()   # IMPORTANT: saves your changes!

# Step 4: Query data
cursor.execute("SELECT * FROM accounts")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Always close when done
conn.close()