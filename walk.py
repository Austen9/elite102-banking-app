import sqlite3


conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, balance REAL DEFAULT 0.0)')
cursor.execute('CREATE TABLE transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER, type TEXT, amount REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
conn.commit()

def make_acc(name, init_dep=0.0):
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, init_dep))
    conn.commit()
    acc_id = cursor.lastrowid
    if init_dep > 0:
        cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'deposit', ?)", (acc_id, init_dep))
        conn.commit()
    print(f"Account created for {name} (ID: {acc_id}) with balance ${init_dep:.2f}")
    return acc_id

def deposit(acc_id, amm):
    if amm <= 0:
        print("Error: Deposit too small")
        return
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amm, acc_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'deposit', ?)", (acc_id, amm))
    conn.commit()
    balance = update_balance(acc_id)
    print(f"Deposited ${amm:.2f}. New balance: ${balance:.2f}")


def withdraw(acc_id, amm):
    if amm <= 0:
        print('error withdrawl too small')
        return
    balance = update_balance(acc_id)
    if amm > balance:
        print(f"Error: Insufficient funds. Balance: ${balance:.2f}, Requested: ${amm:.2f}")
        return
    cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amm, acc_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'withdrawal', ?)", (acc_id, amm))
    conn.commit()
    balance = update_balance(acc_id)

    print(f"took out ${amm:.2f}. New balance: ${balance:.2f}")


def update_balance(account_id):
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    row = cursor.fetchone()
    if row is None:
        print(f"Error: Account {account_id} not found.")
        return 0.0
    return row[0]


def menu():
    while True:
        print("\n=== Banking App ===")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Exit")

        option = input("Select a action:")
        if option == '1':
            name = input("Enter account name:")
            init_dep = float(input("Enter initial deposit (or 0):"))
            make_acc(name, init_dep)
