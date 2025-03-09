import streamlit as st
from database import log_workout, get_workouts

def app():
    st.title("Workout Logging")
    user_id = st.session_state['user_id']

    st.subheader("Log Workout")
    exercise = st.text_input("Exercise Name")
    sets = st.number_input("Sets", min_value=1, value=1)
    reps = st.number_input("Reps", min_value=1, value=10)
    weight = st.number_input("Weight (kg)", min_value=0.0, value=0.0)
    if st.button("Log"):
        log_workout(user_id, exercise, sets, reps, weight)
        st.success("Workout logged!")

    st.subheader("Workout History")
    workouts = get_workouts(user_id)
    for w in workouts:
        st.write(f"{w['date']}: {w['exercise']} - {w['sets']} sets, {w['reps']} reps, {w['weight']} kg")