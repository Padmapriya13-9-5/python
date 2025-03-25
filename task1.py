import sqlite3
import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd

conn = sqlite3.connect('contacts.db')
cursor = conn.cursor()

# Create a table for storing contacts
cursor.execute('''
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL
)
''')

# Function to insert a new contact
def insert_contact():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    
    if name and email and phone:  # Check if fields are not empty
        cursor.execute('INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)', (name, email, phone))
        conn.commit()
        messagebox.showinfo("Success", "Contact added successfully!")
        clear_entries()
        display_contacts()  # Refresh the contact list
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

# Function to display all contacts using Pandas
def display_contacts():
    contacts_list.delete(0, tk.END)  # Clear the listbox before displaying
    cursor.execute('SELECT * FROM contacts')
    records = cursor.fetchall()
    
    # Create a DataFrame using Pandas
    df = pd.DataFrame(records, columns=['ID', 'Name', 'Email', 'Phone'])
    
    # Display contacts in the listbox
    for index, row in df.iterrows():
        contacts_list.insert(tk.END, f'ID: {row["ID"]}, Name: {row["Name"]}, Email: {row["Email"]}, Phone: {row["Phone"]}')

# Function to update a contact
def update_contact():
    selected_contact = contacts_list.curselection()
    if not selected_contact:
        messagebox.showwarning("Selection Error", "Please select a contact to update.")
        return
    
    contact_id = contacts_list.get(selected_contact).split(",")[0].split(":")[1].strip()
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    
    if name and email and phone:  # Check if fields are not empty
        cursor.execute('UPDATE contacts SET name = ?, email = ?, phone = ? WHERE id = ?', (name, email, phone, contact_id))
        conn.commit()
        messagebox.showinfo("Success", "Contact updated successfully!")
        clear_entries()
        display_contacts()  # Refresh the contact list
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

# Function to delete a contact
def delete_contact():
    selected_contact = contacts_list.curselection()
    if not selected_contact:
        messagebox.showwarning("Selection Error", "Please select a contact to delete.")
        return
    
    contact_id = contacts_list.get(selected_contact).split(",")[0].split(":")[1].strip()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    messagebox.showinfo("Success", "Contact deleted successfully!")
    display_contacts()  # Refresh the contact list

# Function to clear input fields
def clear_entries():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

# Function to analyze phone numbers using NumPy
def analyze_phone_numbers():
    cursor.execute('SELECT phone FROM contacts')
    phone_numbers = cursor.fetchall()
    
    # Extract phone numbers into a NumPy array
    phone_array = np.array([phone[0] for phone in phone_numbers])
    
    # Calculate lengths of phone numbers
    lengths = np.vectorize(len)(phone_array)
    
    # Display statistics
    if lengths.size > 0:
        avg_length = np.mean(lengths)
        max_length = np.max(lengths)
        min_length = np.min(lengths)
        messagebox.showinfo("Phone Number Analysis", 
                            f"Average Length: {avg_length}\nMax Length: {max_length}\nMin Length: {min_length}")
    else:
        messagebox.showinfo("Phone Number Analysis", "No phone numbers found.")

# Create the main window
root = tk.Tk()
root.title("Contact Manager")

# Create input fields
tk.Label(root, text="Name").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Email").grid(row=1, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=1, column=1)

tk.Label(root, text="Phone").grid(row=2, column=0)
phone_entry = tk.Entry(root)
phone_entry.grid(row=2, column=1)

# Create buttons
tk.Button(root, text="Add Contact", command=insert_contact).grid(row=3, column=0, columnspan=2)
tk.Button(root, text="Update Contact", command=update_contact).grid(row=4, column=0, columnspan=2)
tk.Button(root, text="Delete Contact", command=delete_contact).grid(row=5, column=0, columnspan=2)
tk.Button(root, text="Analyze Phone Numbers", command=analyze_phone_numbers).grid(row=8, column=0, columnspan=2)

# Create a listbox to display contacts
contacts_list = tk.Listbox(root, width=50)
contacts_list.grid(row=6, column=0, columnspan=2)

# Start the GUI event loop
root.mainloop()

# Close the connection when the application is closed
conn.close()
