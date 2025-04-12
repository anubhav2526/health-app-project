import streamlit as st
from database import update_profile, get_profile

def app():
    st.write(f"Current user_id: {st.session_state.get('user_id', 'Not set')}")
    st.title("Profile")
    user_id = st.session_state['user_id']
    profile = get_profile(user_id) or {}

    age = st.number_input("Age", min_value=1, value=int(profile.get('age') if profile.get('age') is not None else 18))
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(profile.get('gender', "Male")))
    height = st.number_input("Height (cm)", min_value=1.0, value=profile.get('height', 170.0))
    weight = st.number_input("Weight (kg)", min_value=1.0, value=profile.get('weight', 70.0))
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"],
                                  index=["Sedentary", "Light", "Moderate", "Active", "Very Active"].index(profile.get('activity_level', "Moderate")))

    if st.button("Save Profile"):
        update_profile(user_id, gender, age, height, weight, activity_level)
        st.success("Profile updated!")