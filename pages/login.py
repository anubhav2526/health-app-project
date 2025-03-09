import streamlit as st
from database import get_user
from bcrypt import checkpw

def app():
    st.title("Login")

    # Initialize session state variables if they don't exist
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None

    # Check if the user is already logged in
    if st.session_state['user_id'] is not None:
        st.success(f"Logged in as {st.session_state['username']}")
        # You can add additional functionality for logged-in users here
        return  # Exit the function if the user is logged in

    # Get username and password inputs
    username = st.text_input("Username").strip()
    password = st.text_input("Password", type="password").strip()

    if st.button("Login"):
        print("Login button clicked")  # Debugging output
        user = get_user(username)
        print("User retrieved:", user)  # Debugging output
        if user:
            print("Checking password...")  # Debugging output
            password_check = checkpw(password.encode(), user['password_hash'].encode())
            print("Password check result:", password_check)  # Debugging output
            if password_check:
                st.session_state['user_id'] = user['id']
                st.session_state['username'] = user['username']
                st.success(f"Logged in as {user['username']}")
                print("User logged in successfully.")  # Debugging output
                st.rerun()
            else:
                st.error("Invalid username or password")
        else:
            st.error("User not found.")

    # Sign Up section
    new_username = st.text_input("New Username")  # Moved this line up to ensure it's defined
    new_password = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        if get_user(new_username):
            st.error("Username already exists!")
        else:
            from database import create_user
            user = create_user(new_username, new_password)
            if user:
                st.success(f"User {new_username} created! Please log in.")
            else:
                st.error("Error creating user")