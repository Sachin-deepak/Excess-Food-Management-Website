import streamlit as st
from utils import (
    connect_to_db,
    authenticate_user,
    create_user,
    post_donation,
    fetch_donations,
    upload_image_to_storage,
    delete_donation,
    create_post,
    fetch_posts,
    create_request,
    fetch_requests
)
from datetime import datetime
import pandas as pd

# MongoDB Connection
db = connect_to_db()

# Streamlit App Setup
st.set_page_config(page_title="Food Donation App", layout="wide")

# Add custom CSS for animations and smooth navigation
st.markdown(
    """
    <style>
    body {
        transition: background-color 0.5s ease;
    }
    .nav-link {
        transition: color 0.3s ease;
    }
    .nav-link:hover {
        color: #ff6347; /* Change color on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# User Session State
if "user" not in st.session_state:
    st.session_state["user"] = None
if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = "Home"  # Default tab

# Navigation Tabs
navigation_tabs = [
    "Home", "Login", "Signup",
    "Donor Dashboard", "Receiver Dashboard",
    "Forum", "Food Requests", "Analytics"
]
with st.sidebar:
    selected_tab = st.radio("Navigation", navigation_tabs, index=navigation_tabs.index(st.session_state["selected_tab"]))

# Update selected tab in session state
if selected_tab != st.session_state["selected_tab"]:
    st.session_state["selected_tab"] = selected_tab
    st.experimental_rerun()

# Home Page
if st.session_state["selected_tab"] == "Home":
    #st.title("Welcome to the Food Donation App")
    st.markdown("<h1 class='animated-title'>Welcome to the Food Donation App</h1>", unsafe_allow_html=True)
    st.image("home.jpg", use_column_width=True)
    st.write("A platform to reduce food wastage and help those in need.")

# Login Page
elif st.session_state["selected_tab"] == "Login":
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate_user(db, username, password)
        if user:
            st.session_state["user"] = user
            st.success(f"Welcome, {username}!")
            if user["role"] == "Donor":
                st.session_state["selected_tab"] = "Donor Dashboard"
            else:
                st.session_state["selected_tab"] = "Receiver Dashboard"
            st.experimental_rerun()
        else:
            st.error("Invalid credentials. Please try again.")

# Signup Page
elif st.session_state["selected_tab"] == "Signup":
    st.title("Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Donor", "Receiver"])
    bio = st.text_area("Bio")
    profile_picture = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])

    if st.button("Signup"):
        if create_user(db, username, password, role, bio, profile_picture):
            st.success("Account created successfully! Please log in.")
        else:
            st.error("Username already exists. Try another one.")

# Donor Dashboard
elif st.session_state["selected_tab"] == "Donor Dashboard":
    if st.session_state["user"] and st.session_state["user"]["role"] == "Donor":
        st.title("Donor Dashboard")
        st.subheader("Post a Food Donation")
        food_name = st.text_input("Food Name")
        expiry_date = st.date_input("Expiry Date")
        location = st.text_input("Pickup Location")
        contact_details = st.text_input("Contact Details")
        map_location = st.text_input("Map Location (URL or Coordinates)")
        details = st.text_area("Details")
        image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
        if st.button("Submit Donation"):
            if food_name and location and details and contact_details and map_location:
                image_url = upload_image_to_storage(image) if image else None
                expiry_datetime = datetime.combine(expiry_date, datetime.min.time())
                post_donation(
                    db,
                    st.session_state["user"]["username"],
                    food_name,
                    expiry_datetime,
                    location,
                    contact_details,
                    map_location,
                    details,
                    image_url
                )
                st.success("Donation posted successfully!")
            else:
                st.error("Please fill in all fields.")
    else:
        st.error("Please log in as a Donor to access this page.")

# Receiver Dashboard
elif st.session_state["selected_tab"] == "Receiver Dashboard":
    if st.session_state["user"] and st.session_state["user"]["role"] == "Receiver":
        st.title("Receiver Dashboard")
        st.subheader("Available Donations")
        donations = fetch_donations(db)
        if donations:
            df = pd.DataFrame(donations)
            for index, row in df.iterrows():
                st.write(f"*Food Name:* {row['name']}")
                st.write(f"*Expiry Date:* {row['expiry_date']}")
                st.write(f"*Location:* {row['location']}")
                st.write(f"*Contact Details:* {row['contact_details']}")
                st.write(f"*Map Location:* {row['map_location']}")
                st.write(f"*Details:* {row['details']}")
                if st.button(f"Accept Donation {index}"):
                    delete_donation(db, row['_id'])
                    st.success(f"Accepted donation for {row['name']}!")
                    st.experimental_rerun()
        else:
            st.write("No donations available.")
    else:
        st.error("Please log in as a Receiver to access this page.")

# Forum
elif st.session_state["selected_tab"] == "Forum":
    st.title("Grocery Deals Forum")
    
    if st.session_state["user"]:
        # Create two columns for the form
        col1, col2 = st.columns(2)
        
        with col1:
            store_name = st.text_input("Store Name")
            product_details = st.text_area("Product Details", placeholder="List the grocery items...")
            expiry_date = st.date_input("Expiry Date")
            price = st.number_input("Price (₹)", min_value=0.0, step=1.0)
            
        with col2:
            contact_details = st.text_input("Contact Details")
            map_link = st.text_input("Google Maps Link")
            upi_id = st.text_input("UPI ID")
            post_image = st.file_uploader("Upload Product Image", type=["png", "jpg", "jpeg"], key="post_image")

        if st.button("Post Deal"):
            if store_name and product_details and contact_details:
                try:
                    post_image_url = upload_image_to_storage(post_image) if post_image else None
                    success = create_post(
                        db,
                        st.session_state["user"]["username"],
                        product_details,
                        store_name,
                        expiry_date,
                        price,
                        contact_details,
                        map_link,
                        upi_id,
                        post_image_url
                    )
                    if success:
                        st.success("Your deal has been posted!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to post deal. Please try again.")
                except Exception as e:
                    st.error(f"Error posting deal: {str(e)}")
            else:
                st.error("Please fill in all required fields.")

        st.markdown("---")
        st.subheader("Available Deals")

        try:
            posts = fetch_posts(db)
            if posts:
                for post in posts:
                    with st.container():
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"### {post.get('store_name', 'Unknown Store')}")
                            st.markdown(f"*Posted by:* {post.get('username', 'Anonymous')}")
                            st.write("*Product Details:*")
                            st.write(post.get('content', 'No details available'))
                            st.markdown(f"*Price:* ₹{post.get('price', 0.0)}")
                            st.markdown(f"*Expiry Date:* {post.get('expiry_date', 'Not specified')}")
                            
                            with st.expander("Contact Information"):
                                st.write(f"*Contact:* {post.get('contact_details', 'Not provided')}")
                                if post.get('upi_id'):
                                    st.write(f"*UPI ID:* {post['upi_id']}")
                                if post.get('map_link'):
                                    st.markdown(f"[View Store Location]({post['map_link']})")
                        
                        with col2:
                            if post.get('image_url'):
                                try:
                                    st.image(post['image_url'], use_column_width=True)
                                except Exception:
                                    st.error("Error loading image")
                        
                        st.markdown(f"Posted on: {post.get('timestamp', 'Unknown time')}")
                        st.markdown("---")
            else:
                st.info("No deals posted yet. Be the first to share a deal!")
        except Exception as e:
            st.error(f"Error loading posts: {str(e)}")
    else:
        st.error("Please log in to view and post deals.")

# Food Requests
elif st.session_state["selected_tab"] == "Food Requests":
    st.title("Food Requests")
    request_content = st.text_area("What food do you need?")
    request_image = st.file_uploader("Upload an Image for your request", type=["png", "jpg", "jpeg"], key="request_image")
    if st.button("Request"):
        if request_content:
            request_image_url = upload_image_to_storage(request_image) if request_image else None
            create_request(db, st.session_state["user"]["username"], request_content, request_image_url)
            st.success("Request created successfully!")
        else:
            st.error("Please enter your food requirement.")

# Analytics
elif st.session_state["selected_tab"] == "Analytics":
    st.title("Analytics")
    donations = fetch_donations(db)
    if donations:
        df = pd.DataFrame(donations)
        st.write("### Donations by Location")
        st.bar_chart(df["location"].value_counts())
    else:
        st.write("No data available.")