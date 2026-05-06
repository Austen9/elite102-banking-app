import sqlite3

# Re-create the database (each cell runs independently)
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, balance REAL DEFAULT 0.0)')
cursor.execute('CREATE TABLE transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER, type TEXT, amount REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
conn.commit()

# --- Core Banking Functions ---

def create_account(name, initial_deposit=0.0):
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, initial_deposit))
    conn.commit()
    account_id = cursor.lastrowid
    if initial_deposit > 0:
        cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'deposit', ?)", (account_id, initial_deposit))
        conn.commit()
    print(f"Account created for {name} (ID: {account_id}) with balance ${initial_deposit:.2f}")
    return account_id

def deposit(account_id, amount):
    if amount <= 0:
        print("Error: Deposit amount must be positive.")
        return
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'deposit', ?)", (account_id, amount))
    conn.commit()
    balance = check_balance(account_id)
    print(f"Deposited ${amount:.2f}. New balance: ${balance:.2f}")

def withdraw(account_id, amount):
    if amount <= 0:
        print("Error: Withdrawal amount must be positive.")
        return
    balance = check_balance(account_id)
    if amount > balance:
        print(f"Error: Insufficient funds. Balance: ${balance:.2f}, Requested: ${amount:.2f}")
        return
    cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'withdrawal', ?)", (account_id, amount))
    conn.commit()
    new_balance = check_balance(account_id)
    print(f"Withdrew ${amount:.2f}. New balance: ${new_balance:.2f}")

def check_balance(account_id):
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    row = cursor.fetchone()
    if row is None:
        print(f"Error: Account {account_id} not found.")
        return 0.0
    return row[0]

# --- Try it out! ---
alice_id = create_account("Alice", 1000.00)
bob_id = create_account("Bob", 500.00)

deposit(alice_id, 250.00)
withdraw(bob_id, 100.00)

print(f"\nAlice's balance: ${check_balance(alice_id):.2f}")
print(f"Bob's balance: ${check_balance(bob_id):.2f}")