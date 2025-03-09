import streamlit as st
from database import add_food, get_foods, log_food, get_food_logs

def app():
    st.title("Food Log")
    if 'user_id' not in st.session_state or st.session_state['user_id'] is None:
        st.warning("Please log in to log food.")
        return

    user_id = st.session_state['user_id']

    st.subheader("Add New Food Item")
    new_food_name = st.text_input("Food Name")
    new_food_calories = st.number_input("Calories per 100g", min_value=0.0, step=0.1, value=0.0)
    if st.button("Add Food"):
        if add_food(new_food_name, new_food_calories):
            st.success(f"Added {new_food_name}!")
        else:
            st.error("Food already exists or error occurred!")

    st.subheader("Log Food")
    foods = get_foods()
    if foods:
        food_options = {f["name"]: f["id"] for f in foods}
        selected_food = st.selectbox("Select Food", list(food_options.keys()))
        quantity = st.number_input("Quantity (g)", min_value=0.0, step=0.1, value=100.0)
        if st.button("Log Food"):
            if log_food(user_id, food_options[selected_food], quantity):
                st.success(f"Logged {quantity}g of {selected_food}!")
                st.rerun()
            else:
                st.error("Failed to log food!")
    else:
        st.write("No foods available. Add some first!")

    st.subheader("Recent Food Logs")
    logs = get_food_logs(user_id)[:5]
    if logs:
        for log in logs:
            food = next((f for f in get_foods() if f["id"] == log["food_id"]), {"name": "Unknown"})
            st.write(f"{log['date']}: {food['name']} - {log['quantity']}g, {food['calories'] * log['quantity'] / 100:.1f} cal")
    else:
        st.write("No food logs yet!")