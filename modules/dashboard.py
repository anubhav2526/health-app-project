import streamlit as st
from database import get_workouts, get_food_logs, get_weights, get_bmi_records
from agents import get_reminders_agent

def app():
    st.title("Progress Dashboard")

    if 'user_id' not in st.session_state or st.session_state['user_id'] is None:
        st.warning("You need to login to access this page.")
        return
    st.write("Welcome to the Dashboard!")
    st.write(f"Current user_id: {st.session_state.get('user_id', 'Not set')}")
    user_id = st.session_state['user_id']

    if 'reminders_agent' not in st.session_state:
        try:
            st.session_state['reminders_agent'] = get_reminders_agent(user_id)
        except ValueError as e:
            st.error(f"Error initializing agent: {e}")
            return

    st.subheader("Reminders & Messages")
    task_description = "Generate reminders or motivational messages based on the user's recent activity."
    # Create a simple task object
    class SimpleTask:
        def __init__(self, description):
            self.description = description
    
    task = SimpleTask(task_description)

    try:
        response = st.session_state['reminders_agent'].execute_task(task)
        messages = response.split('\n') if response else []
        for msg in messages:
            if msg.strip():  # Only display non-empty messages
                st.info(msg)
    except Exception as e:
        st.error(f"Error generating reminders: {e}")
        st.info("AI-powered reminders are currently unavailable. Stay motivated by setting regular workout schedules!")

    st.subheader("Recent Workouts")
    workouts = get_workouts(user_id)[:5]
    if workouts:
        for w in workouts:
            st.write(f"{w['date']}: {w['exercise']} - {w['sets']} sets, {w['reps']} reps")
    else:
        st.write("No recent workouts logged. Add some on the Workout page!")

    st.subheader("Recent Food Logs")
    logs = get_food_logs(user_id)[:5]
    if logs:
        for l in logs:
            food_name = l.get('name', 'Unknown food')
            quantity = l['quantity']
            calories = l.get('calories', 0)  # Default to 0 if calories is None
            if calories is not None:
                st.write(f"{l['date']}: {food_name} - {quantity}g, {calories * quantity / 100} cal")
            else:
                st.write(f"{l['date']}: {food_name} - {quantity}g, calories unknown")
    else:
        st.write("No recent food logs. Add some on the Food page!")

    st.subheader("Weight Trend")
    weights = get_weights(user_id)
    if weights:
        dates = [w['date'] for w in weights]
        values = [w['weight'] for w in weights]
        st.line_chart({"Date": dates, "Weight (kg)": values})
    else:
        st.write("No weight data available. Add some on the Weight page!")

    st.subheader("BMI Trend")
    bmis = get_bmi_records(user_id)
    if bmis:
        dates = [b['date'] for b in bmis]
        values = [b['bmi'] for b in bmis]
        st.line_chart({"Date": dates, "BMI": values})
    else:
        st.write("No BMI data available. Add some on the BMI page!")