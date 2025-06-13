import streamlit as st
from db.connection import get_connection
from utils.auth import hash_password

def register_user(name, email, dob, age, gender, phone, address, username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO User (Email_ID, Name, DateOfBirth, Age, Gender, Phone_Number, Address) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (email, name, dob, age, gender, phone, address))
    user_id = cursor.lastrowid
    cursor.execute("INSERT INTO Login (User_ID, Username, Password) VALUES (%s,%s,%s)",
        (user_id, username, hash_password(password)))
    
    conn.commit()
    conn.close()

st.subheader("🔐 Login or Register")

option = st.selectbox("Choose an action", ["Login", "Register"])

if option == "Register":
    with st.form("register_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        dob = st.date_input("Date of Birth")
        age = st.number_input("Age", 0, 100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        phone = st.text_input("Phone")
        address = st.text_input("Address")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Register"):
            register_user(name, email, dob, age, gender, phone, address, username, password)
            st.success("User registered! Please log in.")

elif option == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Login WHERE Username=%s AND Password=%s",
            (username, hash_password(password)))
        user = cursor.fetchone()
        if user:
            st.success(f"Welcome, {username}!")
            st.session_state.user_id = user["User_ID"]
            st.write("DEBUG: Logged in user ID:", user["User_ID"])
        else:
            st.error("Invalid credentials.")
