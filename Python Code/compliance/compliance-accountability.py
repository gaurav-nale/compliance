# Streamlit UI code
# import streamlit as st
# from datetime import date
# import mysql.connector

# def get_db_connection():
#     return mysql.connector.connect(
#         host = 'localhost',
#         user = 'root',
#         password = "",
#         database = "compliance"
#     )

# def add_name(name, filename = "system"):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     today = date.today().isoformat()

#     cursor.execute("""
#         INSERT INTO `sdn-list` (`SDN Name`, `filename`, `start_date`, `end_date`)
#         VALUES (%s, %s, %s, NULL)
#     """, (name, filename, today))

#     conn.commit()
#     conn.close()
#     st.success(f"Added '{name}' on {today} for filename: {filename}")

# def delete_name(name, filename):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     today = date.today().isoformat()

#     cursor.execute("""
#         UPDATE `sdn-list`
#         SET `end_date` = %s
#         WHERE `SDN Name` = %s AND `end_date` IS NULL AND `filename` = %s
#         ORDER BY `id` DESC
#         LIMIT 1
#     """, (today, name, filename))
#     conn.commit()

#     if cursor.rowcount:
#         st.success(f"Deleted (ended) '{name}' on {today} for filename : {filename}")
#     else:
#         st.warning(f"No active record found for '{name} for filename : {filename}'")
#     conn.close()

# def check_name(name, check_date, filename):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT * FROM `sdn-list`
#         WHERE `SDN Name` = %s
#         AND `start_date` <= %s
#         AND (`end_date` IS NULL OR `end_date` >= %s)
#         AND `filename` = %s
#     """, (name, check_date, check_date, filename))

#     result = cursor.fetchall()
#     conn.close()
#     if result:
#         st.success(f"'{name}' was active on {check_date} for filename : {filename}")
#     else:
#         st.error(f"'{name}' was NOT active on {check_date} for filename : {filename}")

# st.title("Compliance Auditability")

# st.sidebar.title("Actions")
# action = st.sidebar.radio("Select Action", ["Add", "Delete", "Check name"])

# if action == "Add":
#     st.header("Add Name")
#     name = st.text_input("Name")
#     filename = st.text_input("Filename", value="system")
#     if st.button("Add Name"):
#         if name:
#             add_name(name, filename)
#         else:
#             st.warning("Please enter a name.")


# elif action == "Delete":
#     st.header("Delete Name (End Record)")
#     name = st.text_input("Name to Delete")
#     filename = st.text_input("Filename", value="system")
#     if st.button("Delete Name"):
#         if name:
#             delete_name(name, filename)
#         else:
#             st.warning("Please enter a name.")

# elif action == "Check name":
#     st.header("Check if Name was Active")
#     name = st.text_input("Name to Check")
#     check_date = st.date_input("Date to Check", value=date.today())
#     filename = st.text_input("Filename", value="system")
#     if st.button("Check Name"):
#         if name:
#             check_name(name, check_date.isoformat(),filename)
#         else:
#             st.warning("Please enter a name.")

# postman code
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
import mysql.connector

app = FastAPI()

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='compliance'
    )

class SDNEntry(BaseModel):
    name: str
    filename: str = "system"

class CheckRequest(BaseModel):
    name: str
    check_date: date
    filename: str = "system"

@app.post("/add")
def add_name(entry: SDNEntry):
    conn = get_db_connection()
    cursor = conn.cursor()
    today = date.today().isoformat()

    cursor.execute("""
        INSERT INTO `sdn-list` (`SDN Name`, `filename`, `start_date`, `end_date`)
        VALUES (%s, %s, %s, NULL)
    """, (entry.name, entry.filename, today))

    conn.commit()
    conn.close()
    return {"message": f"Added '{entry.name}' on {today} for filename: {entry.filename}"}

@app.post("/delete")
def delete_name(entry: SDNEntry):
    conn = get_db_connection()
    cursor = conn.cursor()
    # today = date.today().isoformat()
    today = "2025-04-26"

    cursor.execute("""
        UPDATE `sdn-list`
        SET `end_date` = %s
        WHERE `SDN Name` = %s AND `end_date` IS NULL AND `filename` = %s
        ORDER BY `id` DESC
        LIMIT 1
    """, (today, entry.name, entry.filename))
    conn.commit()
    rowcount = cursor.rowcount
    conn.close()

    if rowcount:
        return {"message": f"Deleted (ended) '{entry.name}' on {today} for filename: {entry.filename}"}
    else:
        raise HTTPException(status_code=404, detail=f"No active record found for '{entry.name}' with filename: {entry.filename}")

@app.post("/check")
def check_name(entry: CheckRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM `sdn-list`
        WHERE `SDN Name` = %s
        AND `start_date` <= %s
        AND (`end_date` IS NULL OR `end_date` >= %s)
        AND `filename` = %s
    """, (entry.name, entry.check_date, entry.check_date, entry.filename))

    result = cursor.fetchall()
    conn.close()

    if result:
        return {"message": f"'{entry.name}' was active on {entry.check_date} for filename: {entry.filename}"}
    else:
        raise HTTPException(status_code=404, detail=f"'{entry.name}' was NOT active on {entry.check_date} for filename: {entry.filename}'")



# Add names to the DB
# import csv
# from datetime import date
# import mysql.connector

# FILENAME = "consolidated"
# CSV_PATH = "consolidated.csv"  # <-- Update this

# def get_db_connection():
#     return mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='',
#         database='compliance'
#     )

# def load_and_insert_names(csv_path):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     today = date.today().isoformat()
#     inserted = 0

#     with open(csv_path, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             name = row.get("name")
#             if name:
#                 try:
#                     cursor.execute("""
#                         INSERT INTO `sdn-list` (`SDN Name`, `filename`, `start_date`, `end_date`)
#                         VALUES (%s, %s, %s, NULL)
#                     """, (name.strip(), FILENAME, today))
#                     inserted += 1
#                 except Exception as e:
#                     print(f"Error inserting '{name}': {e}")

#     conn.commit()
#     conn.close()
#     print(f"✅ Inserted {inserted} names into database with filename '{FILENAME}'.")

# # Run the function
# if __name__ == "__main__":
#     load_and_insert_names(CSV_PATH)

