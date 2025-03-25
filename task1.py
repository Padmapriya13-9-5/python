import sqlite3

# Connect to the SQLite database (it will create a new database file if it doesn't exist)
conn = sqlite3.connect('contacts.db')
cursor = conn.cursor()

# Create a table to store contact information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
''')

# Function to insert a contact into the database
def insert_contact(name, email, phone):
    cursor.execute('''
        INSERT INTO contacts (name, email, phone)
        VALUES (?, ?, ?)
    ''', (name, email, phone))
    conn.commit()

# Function to retrieve all contacts from the database
def get_all_contacts():
    cursor.execute('SELECT * FROM contacts')
    return cursor.fetchall()

# Simple interface to add contacts
while True:
    print("Enter contact details (or type 'exit' to quit):")
    
    name = input("Name: ")
    if name.lower() == 'exit':
        break
    
    email = input("Email: ")
    phone = input("Phone: ")

    # Insert contact into the database
    insert_contact(name, email, phone)

    print("Contact added successfully!")

# Display all contacts
print("\nAll contacts in the database:")
contacts = get_all_contacts()
for contact in contacts:
    print(f"ID: {contact[0]}, Name: {contact[1]}, Email: {contact[2]}, Phone: {contact[3]}")

# Close the connection to the database
conn.close()
