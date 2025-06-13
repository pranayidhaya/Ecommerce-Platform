import streamlit as st

# Set page title and layout
st.set_page_config(page_title="E-Commerce Platform", layout="wide")

# Sidebar navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/891/891419.png", width=50)
    st.title("🛍️ E-Commerce")

    # Show login status
    if 'user_id' in st.session_state:
        st.success(f"Hi, user {st.session_state.user_id} 👋")
    else:
        st.info("🔐 Please log in")

    st.markdown("---")
    st.page_link("pages/1_Login.py", label="🔐 Login / Register")
    st.page_link("pages/2_Browse.py", label="🛒 Browse Products")
    st.page_link("pages/3_Cart.py", label="🧺 View Cart")
    st.page_link("pages/4_Checkout.py", label="💳 Checkout")
    st.page_link("pages/5_Orders.py", label="📦 My Orders")
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit")

# Main content
st.title("🛒 Welcome to the E-Commerce Platform!")
st.markdown("""
Explore our wide range of products and enjoy a smooth shopping experience.
Use the **sidebar** to navigate through different sections of the app.
""")
