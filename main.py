import streamlit as st
from pages import login, profile, workout, food, weight, bmi, dashboard, settings, chat

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