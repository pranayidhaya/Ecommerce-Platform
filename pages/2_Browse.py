import streamlit as st
from db.connection import get_connection

st.subheader("🛍️ Browse Products")

# Ensure user is logged in
if 'user_id' not in st.session_state:
    st.warning("Please log in to browse and add products to your cart.")
    st.stop()

# Fetch products from DB
def get_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    conn.close()
    return products

# Add to cart by fetching product details from DB using Product_ID
def add_to_cart(product_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Price FROM Product WHERE Product_ID = %s", (product_id,))
    product = cursor.fetchone()

    if not product:
        st.error("Product not found.")
        conn.close()
        return

    try:
        cursor = conn.cursor()
        # Insert into Cart with valid columns only
        cursor.execute("""
            INSERT INTO Cart (Product_ID, Price, Quantity, User_ID)
            VALUES (%s, %s, %s, %s)
        """, (
            product_id,
            product['Price'],
            1,
            st.session_state.user_id
        ))
        conn.commit()
        st.success("Product added to your cart!")
    except Exception as e:
        st.error(f"Failed to add to cart: {e}")
    finally:
        conn.close()



# Render products
products = get_products()
for product in products:
    with st.container(border=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            image_url = product.get('Image') or "https://via.placeholder.com/150"
            try:
                st.image(image_url, use_container_width=True)
            except Exception:
                st.image("https://via.placeholder.com/150?text=Image+Error", use_container_width=True)
        with col2:
            st.markdown(f"### {product['Name']}")
            st.write(f"**Brand:** {product['Brand']}")
            st.write(f"**Price:** ₹{product['Price']:.2f}")
            st.write(f"**Description:** {product['Description']}")
            if st.button("➕ Add to Cart", key=f"add_{product['Product_ID']}"):
                add_to_cart(product['Product_ID'])
