import flet as ft
import sqlite3

# SQLite database setup
conn = sqlite3.connect("example.db",check_same_thread=False)
cursor = conn.cursor()

# Create a table with 8 columns
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    prename TEXT,
                    dateN TEXT,
                    age INTEGER,
                    email TEXT,
                    adresse TEXT,
                    Ncin TEXT,
                    ntel TEXT
                )''')
conn.commit()

# Function to fetch all users from the database
def fetch_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Function to insert user into the database
def insert_user(name, prename, dateN, age, email, adresse, Ncin, ntel):
    cursor.execute('''INSERT INTO users (name, prename, dateN, age, email, adresse, Ncin, ntel) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (name, prename, dateN, age, email, adresse, Ncin, ntel))
    conn.commit()

# Function to update user in the database
def update_user(user_id, name, prename, dateN, age, email, adresse, Ncin, ntel):
    cursor.execute('''UPDATE users
                      SET name = ?, prename = ?, dateN = ?, age = ?, email = ?, adresse = ?, Ncin = ?, ntel = ?
                      WHERE id = ?''', 
                   (name, prename, dateN, age, email, adresse, Ncin, ntel, user_id))
    conn.commit()

# Function to delete user from the database
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

# Flet UI setup
def main(page: ft.Page):
    page.title = "family database"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor=ft.colors.PINK
    page.padding = 20

    # Input fields
    name = ft.TextField(label="Name",bgcolor=ft.colors.DEEP_ORANGE, width=300)
    prename = ft.TextField(label="Prename",bgcolor=ft.colors.DEEP_ORANGE, width=300)
    dateN = ft.TextField(label="Date of Birth",bgcolor=ft.colors.DEEP_ORANGE, width=300)
    age = ft.TextField(label="Age", bgcolor=ft.colors.DEEP_ORANGE,width=300)
    email = ft.TextField(label="Email",bgcolor=ft.colors.DEEP_ORANGE, width=300)
    adresse = ft.TextField(label="Address",bgcolor=ft.colors.DEEP_ORANGE, width=300)
    Ncin = ft.TextField(label="National ID",bgcolor=ft.colors.DEEP_ORANGE, width=300)
    ntel = ft.TextField(label="Phone Number",bgcolor=ft.colors.DEEP_ORANGE, width=300)

    # Functions to update the data table after CRUD operations
    def update_data_table():
        users = fetch_users()
        data_table.rows.clear()
        for user in users:
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(user[1])),
                        ft.DataCell(ft.Text(user[2])),
                        ft.DataCell(ft.Text(user[3])),
                        ft.DataCell(ft.Text(str(user[4]))),
                        ft.DataCell(ft.Text(user[5])),
                        ft.DataCell(ft.Text(user[6])),
                        ft.DataCell(ft.Text(user[7])),
                        ft.DataCell(ft.Text(user[8])),
                    ]
                )
            )
        page.update()

    # Button actions
    def add_user(e):
        if name.value and prename.value and dateN.value and age.value and email.value and adresse.value and Ncin.value and ntel.value:
            insert_user(name.value, prename.value, dateN.value, age.value, email.value, adresse.value, Ncin.value, ntel.value)
            update_data_table()
            clear_fields()

    def update_user_action(e):
        if name.value and prename.value and dateN.value and age.value and email.value and adresse.value and Ncin.value and ntel.value:
            user_id = int(selected_user_id.value)
            update_user(user_id, name.value, prename.value, dateN.value, age.value, email.value, adresse.value, Ncin.value, ntel.value)
            update_data_table()
            clear_fields()

    def delete_user_action(e):
        if selected_user_id.value:
            user_id = int(selected_user_id.value)
            delete_user(user_id)
            update_data_table()
            clear_fields()

    # Clear input fields
    def clear_fields():
        name.value = ""
        prename.value = ""
        dateN.value = ""
        age.value = ""
        email.value = ""
        adresse.value = ""
        Ncin.value = ""
        ntel.value = ""
        selected_user_id.value = ""
        page.update()

    # Table to display data
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Name")),
            ft.DataColumn(label=ft.Text("Prename")),
            ft.DataColumn(label=ft.Text("Date of Birth")),
            ft.DataColumn(label=ft.Text("Age")),
            ft.DataColumn(label=ft.Text("Email")),
            ft.DataColumn(label=ft.Text("Address")),
            ft.DataColumn(label=ft.Text("National ID")),
            ft.DataColumn(label=ft.Text("Phone Number")),
        ],
        rows=[],
        column_spacing=20,
        heading_row_color=ft.colors.CYAN_400,
    )

    # Initialize data in the table
    update_data_table()

    # App bar
    page.appbar = ft.AppBar(
        title=ft.Text("NOTRE FICHIER"),
        bgcolor=ft.colors.INDIGO,
    )

    # Buttons
    add_button = ft.ElevatedButton(text="Add User", on_click=add_user, bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE)
    update_button = ft.ElevatedButton(text="Update User", on_click=update_user_action, bgcolor=ft.colors.YELLOW_600, color=ft.colors.WHITE)
    delete_button = ft.ElevatedButton(text="Delete User", on_click=delete_user_action, bgcolor=ft.colors.RED_600, color=ft.colors.WHITE)

    # Selected user ID (hidden, used for update/delete)
    selected_user_id = ft.TextField(visible=False)

    # Main content layout
    page.add(
        ft.Column(
            [
                
                ft.Row([name, prename], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([dateN, age, email], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([adresse, Ncin, ntel], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([add_button, update_button, delete_button], alignment=ft.MainAxisAlignment.CENTER),
                data_table,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

# Run the app
ft.app(target=main)
