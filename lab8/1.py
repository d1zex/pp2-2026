import psycopg2
import pandas as pd
import re
import json

# DB connection
conn = psycopg2.connect(
    dbname="phonebook_db",
    user="postgres",
    password="lolpopqwerty",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) UNIQUE,
    phone VARCHAR(15)
)
""")

# FUNCTION: search by pattern
cur.execute("""
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p TEXT)
RETURNS TABLE(first_name VARCHAR, phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.first_name, c.phone
    FROM phonebook c
    WHERE c.first_name ILIKE '%' || p || '%'
       OR c.phone ILIKE '%' || p || '%';
END;
$$;
""")

# PROCEDURE: insert or update
cur.execute("""
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;
""")

# PROCEDURE: insert many users
cur.execute("""
CREATE OR REPLACE PROCEDURE insert_many_contacts(users JSONB)
LANGUAGE plpgsql
AS $$
DECLARE
    u JSONB;
    invalid JSONB := '[]';
BEGIN
    FOR u IN SELECT * FROM jsonb_array_elements(users)
    LOOP
        IF (u->>'phone') ~ '^\\+7\\d{10}$' THEN
            CALL upsert_contact(u->>'name', u->>'phone');
        ELSE
            invalid := invalid || u;
        END IF;
    END LOOP;

    RAISE NOTICE 'Invalid data: %', invalid;
END;
$$;
""")

# FUNCTION: pagination
cur.execute("""
CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    ORDER BY id
    LIMIT lim OFFSET off;
END;    
$$;
""")

# PROCEDURE: delete
cur.execute("""
CREATE OR REPLACE PROCEDURE delete_contact(identifier VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = identifier OR phone = identifier;
END;
$$;
""")

conn.commit()

# Validation helpers
def is_valid_name(name):
    return name.isalpha()

def is_valid_phone(phone):
    return re.fullmatch(r"\+7\d{10}", phone) is not None


# Insert manually
def insert_from_console():
    name = input("Enter name: ")

    if not is_valid_name(name):
        print("Only letters allowed")
        return

    phone = input("Enter phone (+7XXXXXXXXXX): ")

    if not is_valid_phone(phone):
        print("Invalid format")
        return

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    print("Saved 👍")


# Insert from CSV
def insert_from_csv():
    path = input("Enter CSV path: ")

    try:
        df = pd.read_csv(path)
    except Exception:
        print("File error")
        return

    users = []

    for _, row in df.iterrows():
        name = str(row['first_name'])
        phone = str(row['phone'])
        users.append({"name": name, "phone": phone})

    cur.execute("CALL insert_many_contacts(%s::jsonb)", (json.dumps(users),))
    conn.commit()

    print("CSV loaded 👍")


# Search
def search_pattern():
    pattern = input("Search: ")
    cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)


# Pagination (PAGES)
def show_contacts():
    page = 0
    limit = 10

    while True:
        offset = page * limit

        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s)",
            (limit, offset)
        )

        rows = cur.fetchall()

        if not rows:
            print("No data")
            break

        print(f"\n--- Page {page + 1} ---")
        for row in rows:
            print(row)

        action = input("[n-next | p-prev | q-quit]: ").lower()

        if action == "n":
            page += 1
        elif action == "p" and page > 0:
            page -= 1
        elif action == "q":
            break


# Delete
def delete_entry():
    identifier = input("Enter name or phone: ")
    cur.execute("CALL delete_contact(%s)", (identifier,))
    conn.commit()
    print("Deleted 👍")


# Insert many manually
def insert_many():
    n = int(input("How many users: "))
    users = []

    for _ in range(n):
        name = input("Name: ")
        phone = input("Phone: ")
        users.append({"name": name, "phone": phone})

    cur.execute("CALL insert_many_contacts(%s::jsonb)", (json.dumps(users),))
    conn.commit()


# Menu
def main():
    while True:
        print("\nPhoneBook Menu:")
        print("1. Add contact")
        print("2. Load CSV")
        print("3. Search")
        print("4. Show contacts (pages)")
        print("5. Delete")
        print("6. Insert many")
        print("7. Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            search_pattern()
        elif choice == "4":
            show_contacts()
        elif choice == "5":
            delete_entry()
        elif choice == "6":
            insert_many()
        elif choice == "7":
            break
        else:
            print("Invalid option")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()