import streamlit as st
from database import log_weight, get_weights

def app():
    st.title("Weight Log")
    if 'user_id' not in st.session_state or st.session_state['user_id'] is None:
        st.warning("Please log in to log your weight.")
        return

    user_id = st.session_state['user_id']
    st.subheader("Log Your Weight")
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1, value=70.0)
    if st.button("Log Weight"):
        if log_weight(user_id, weight):
            st.success(f"Logged weight: {weight} kg!")
            st.rerun()
        else:
            st.error("Failed to log weight!")

    st.subheader("Recent Weight Entries")
    weights = get_weights(user_id)[:5]
    if weights:
        for w in weights:
            st.write(f"{w['date']}: {w['weight']} kg")
    else:
        st.write("No weight entries logged yet!")

    st.subheader("Weight Trend")
    if weights:
        dates = [w['date'] for w in weights]
        values = [w['weight'] for w in weights]
        st.line_chart({"Date": dates, "Weight (kg)": values})
    else:
        st.write("No weight data to display.")