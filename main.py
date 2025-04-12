
import streamlit as st
from modules import login, profile, workout, food, weight, bmi, dashboard, settings, chat

import streamlit as st
import base64
import os

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Adjust the path to your image. For example, if it's in the "images" folder:
image_path = os.path.join("background.jpg")
# Or if it's in the same directory as your main file, simply:
# image_path = "background.jpg"
encoded_image = get_base64_of_bin_file(image_path)

# Inject custom CSS to set the background image
st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/jpeg;base64,{encoded_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'just_logged_in' not in st.session_state:
    st.session_state['just_logged_in'] = False

# Handle just logged in state
if st.session_state['just_logged_in']:
    st.session_state['just_logged_in'] = False
    page = "Dashboard"  # Set default page after login
else:
    # Sidebar navigation
    st.sidebar.title("Fitness & Nutrition App")
    page = st.sidebar.radio("Navigate", ["Login", "Profile", "Workout", "Food", "Weight", "BMI", "Dashboard", "Settings", "Chat"])

# Page routing
if page == "Login":
    login.app()
elif st.session_state['user_id'] is not None:
    if page == "Profile":
        profile.app()
    elif page == "Workout":
        workout.app()
    elif page == "Food":
        food.app()
    elif page == "Weight":
        weight.app()
    elif page == "BMI":
        bmi.app()
    elif page == "Dashboard":
        dashboard.app()
    elif page == "Settings":
        settings.app()
    elif page == "Chat":
        chat.app()
else:
    st.warning("Please log in to access this page.")
