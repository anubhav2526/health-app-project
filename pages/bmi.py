import streamlit as st
from database import get_profile, log_bmi, get_bmi_records

def app():
    st.title("BMI Calculator")
    user_id = st.session_state['user_id']
    profile = get_profile(user_id) or {}

    height = st.number_input("Height (cm)", min_value=1.0, value=profile.get('height', 170.0))
    weight = st.number_input("Weight (kg)", min_value=1.0, value=profile.get('weight', 70.0))
    if st.button("Calculate BMI"):
        bmi = weight / ((height / 100) ** 2) if height > 0 else 0
        st.write(f"Your BMI: {bmi:.2f}")
        log_bmi(user_id, weight, height)
        st.success("BMI logged!")

    st.subheader("BMI History")
    records = get_bmi_records(user_id)
    for r in records:
        st.write(f"{r['date']}: {r['bmi']:.2f}")