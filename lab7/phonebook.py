import psycopg2
import pandas as pd

# Connecting to PostgreSQL
conn = psycopg2.connect(
    dbname="phonebook_db",  
    user="postgres",
    password="lolpopqwerty",
    host="localhost",
    port="5432"
)
cur = conn.cursor()


cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) UNIQUE,
        phone VARCHAR(15)
    )
""")
conn.commit()


def insert_from_console():
    first_name = input("Enter first name: ")
    phone = input("Enter phone number: ")
    cur.execute(
        """
        INSERT INTO phonebook (first_name, phone)
        VALUES (%s, %s)
        ON CONFLICT (first_name)
        DO UPDATE SET phone = EXCLUDED.phone
        """,
        (first_name, phone)
    )
    conn.commit()
    print("Data inserted/updated successfully!")


def insert_from_csv():
    path = input("Enter CSV file path: ")
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print("File not found! Check path and try again.")
        return
    except pd.errors.EmptyDataError:
        print("CSV file is empty.")
        return

    # Insert or update all rows
    data = [(row['first_name'], row['phone']) for _, row in df.iterrows()]
    cur.executemany(
        """
        INSERT INTO phonebook (first_name, phone)
        VALUES (%s, %s)
        ON CONFLICT (first_name)
        DO UPDATE SET phone = EXCLUDED.phone
        """,
        data
    )
    conn.commit()
    print("CSV data inserted/updated successfully!")


def update_entry():
    print("1. Update name\n2. Update phone")
    choice = input("Choose option: ")
    if choice == "1":
        old_name = input("Current name: ")
        new_name = input("New name: ")
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
    elif choice == "2":
        name = input("Name: ")
        new_phone = input("New phone: ")
        cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s", (new_phone, name))
    else:
        print("Invalid choice")
        return
    conn.commit()
    print("Data updated successfully!")


def query_data():
    print("1. Show all\n2. Filter by name\n3. Filter by phone prefix")
    choice = input("Choose option: ")
    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
        rows = cur.fetchall()
    elif choice == "2":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
        rows = cur.fetchall()
    elif choice == "3":
        prefix = input("Enter phone prefix: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (prefix + '%',))
        rows = cur.fetchall()
    else:
        print("Invalid option")
        return

    for row in rows:
        print(row)


def delete_entry():
    print("1. Delete by name\n2. Delete by phone")
    choice = input("Choose option: ")
    if choice == "1":
        name = input("Enter name to delete: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    elif choice == "2":
        phone = input("Enter phone to delete: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    else:
        print("Invalid choice")
        return
    conn.commit()
    print("Deleted successfully!")


def main():
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from console")
        print("2. Insert from CSV")
        print("3. Update entry")
        print("4. Query data")
        print("5. Delete entry")
        print("6. Exit")
        choice = input("Choose option: ")
        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            update_entry()
        elif choice == "4":
            query_data()
        elif choice == "5":
            delete_entry()
        elif choice == "6":
            break
        else:
            print("Invalid option")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()