import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Fetch reservations
cursor.execute("SELECT * FROM reservation")
reservations = cursor.fetchall()
print("Reservations:")
for res in reservations:
    print(res)

# Fetch contact messages
cursor.execute("SELECT * FROM contact")
contacts = cursor.fetchall()
print("\nContacts:")
for contact in contacts:
    print(contact)

conn.close()
