import streamlit as st
from db.connection import get_connection

st.subheader("🛒 Your Shopping Cart")

# Ensure user is logged in
if 'user_id' not in st.session_state:
    st.warning("Please log in to view your cart.")
    st.stop()

def get_cart_items(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT Cart.Cart_ID, Product.Name AS ProductName, Cart.Price, Cart.Quantity, Product.Brand
        FROM Cart
        JOIN Product ON Cart.Product_ID = Product.Product_ID
        WHERE Cart.User_ID = %s
    """, (user_id,))
    items = cursor.fetchall()
    conn.close()
    return items

def remove_cart_item(cart_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Cart WHERE Cart_ID = %s", (cart_id,))
    conn.commit()
    conn.close()
    st.success("Item removed from cart.")

cart_items = get_cart_items(st.session_state.user_id)

if not cart_items:
    st.info("Your cart is empty.")
else:
    total = 0
    for item in cart_items:
        col1, col2, col3 = st.columns([4, 2, 2])
        with col1:
            st.write(f"**{item['ProductName']}** - {item['Brand']}")
        with col2:
            st.write(f"₹{item['Price']} × {item['Quantity']}")
        with col3:
            if st.button("🗑️ Remove", key=item['Cart_ID']):
                remove_cart_item(item['Cart_ID'])
                st.rerun()

        total += item['Price'] * item['Quantity']

    st.markdown("---")
    st.markdown(f"### 🧾 Total: ₹{total:.2f}")
