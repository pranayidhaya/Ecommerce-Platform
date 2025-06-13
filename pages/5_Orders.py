import streamlit as st
from db.connection import get_connection

st.subheader("📦 My Orders")

# Ensure user is logged in
if 'user_id' not in st.session_state:
    st.warning("Please log in to view your orders.")
    st.stop()

def get_orders(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.Order_ID, o.Product_Details, o.Address,
               p.UPI, p.Credit_Card, p.Debit_Card, p.Cash_On_Delivery
        FROM Orders o
        JOIN Payment p ON o.Payment_ID = p.Payment_ID
        WHERE o.User_ID = %s
        ORDER BY o.Order_ID DESC
    """, (user_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders

orders = get_orders(st.session_state.user_id)

if not orders:
    st.info("You haven't placed any orders yet.")
else:
    for order in orders:
        with st.container(border=True):
            st.write(f"🧾 **Order ID:** {order['Order_ID']}")
            st.write(f"📦 **Products:** {order['Product_Details']}")
            st.write(f"📍 **Address:** {order['Address']}")

            if order['UPI']:
                payment_mode = f"UPI ({order['UPI']})"
            elif order['Credit_Card']:
                payment_mode = f"Credit Card ({order['Credit_Card']})"
            elif order['Debit_Card']:
                payment_mode = f"Debit Card ({order['Debit_Card']})"
            elif order['Cash_On_Delivery']:
                payment_mode = "Cash On Delivery"
            else:
                payment_mode = "Unknown"

            st.write(f"💳 **Payment Mode:** {payment_mode}")
            st.markdown("---")
