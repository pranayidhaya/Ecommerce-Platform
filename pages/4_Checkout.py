import streamlit as st
from db.connection import get_connection

st.subheader("🧾 Checkout")

# Ensure user is logged in
if 'user_id' not in st.session_state:
    st.warning("Please log in to proceed to checkout.")
    st.stop()

user_id = st.session_state.user_id

# Fetch cart items with product name, price, quantity
conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("""
    SELECT c.Quantity, p.Name, p.Brand, p.Price
    FROM Cart c
    JOIN Product p ON c.Product_ID = p.Product_ID
    WHERE c.User_ID = %s
""", (user_id,))

cart_items = cursor.fetchall()

if not cart_items:
    st.info("Your cart is empty. Add items before proceeding to checkout.")
    conn.close()
    st.stop()

# Show order summary
st.write("### 🛍️ Order Summary")
total = 0
for item in cart_items:
    st.write(f"- **{item['Name']}** ({item['Brand']}) - ₹{item['Price']} × {item['Quantity']}")
    total += item['Price'] * item['Quantity']

st.markdown(f"### 💵 Total Amount: ₹{total:.2f}")
st.markdown("---")

# Payment method
payment_method = st.selectbox("Select Payment Method", ["UPI", "Credit Card", "Debit Card", "Cash on Delivery"])

# Input for payment details
bank_details = st.text_input("Bank Name")
account_details = st.text_input("Account Details")

upi = credit_card = debit_card = None
cod = False

if payment_method == "UPI":
    upi = st.text_input("UPI ID")
elif payment_method == "Credit Card":
    credit_card = st.text_input("Credit Card Number")
elif payment_method == "Debit Card":
    debit_card = st.text_input("Debit Card Number")
else:
    cod = True

# Address input
address = st.text_area("Delivery Address")

# Confirm order
if st.button("✅ Confirm Order"):
    # Insert into Payment table
    cursor.execute("""
        INSERT INTO Payment (Bank_Details, Account_Details, UPI, Credit_Card, Debit_Card, Cash_On_Delivery)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (bank_details, account_details, upi, credit_card, debit_card, cod))
    payment_id = cursor.lastrowid

    # Build product details string
    product_details = ', '.join(
        [f"{item['Name']} (Qty: {item['Quantity']})" for item in cart_items]
    )

    # Insert into Orders table
    cursor.execute("""
        INSERT INTO Orders (Product_Details, Address, User_ID, Payment_ID)
        VALUES (%s, %s, %s, %s)
    """, (product_details, address, user_id, payment_id))

    # Clear cart
    cursor.execute("DELETE FROM Cart WHERE User_ID = %s", (user_id,))
    conn.commit()
    conn.close()

    st.success("🎉 Order placed successfully!")
    st.balloons()
    st.rerun()
else:
    conn.close()
