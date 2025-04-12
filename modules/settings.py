import streamlit as st
from database import update_settings, get_settings, update_goals, get_goals

def app():
    st.title("Settings")
    user_id = st.session_state['user_id']
    settings = get_settings(user_id) or {}
    goals = get_goals(user_id) or {}

    st.subheader("Preferences")
    units = st.selectbox("Units", ["Metric", "Imperial"], index=["Metric", "Imperial"].index(settings.get('units', "Metric") or "Metric"))
    notifications = st.checkbox("Enable Notifications", value=settings.get('notifications', "on") == "on")
    if st.button("Save Settings"):
        update_settings(user_id, "on" if notifications else "off", units)
        st.success("Settings saved!")

    st.subheader("Goals")
    calorie_target = st.number_input("Daily Calorie Target", min_value=0.0, value=goals.get('calorie_target', 2000.0))
    # protein_ratio = st.number_input("Protein Ratio (%)", min_value=0.0, max_value=100.0, value=float(goals.get('macro_ratios', "30,40,30").split(',')[0]))
    # carbs_ratio = st.number_input("Carbs Ratio (%)", min_value=0.0, max_value=100.0, value=float(goals.get('macro_ratios', "30,40,30").split(',')[1]))
    # fats_ratio = st.number_input("Fats Ratio (%)", min_value=0.0, max_value=100.0, value=float(goals.get('macro_ratios', "30,40,30").split(',')[2]))
    dietary_restrictions = st.multiselect("Dietary Restrictions", ["Vegetarian", "Vegan", "Gluten-Free"], default=goals.get('dietary_restrictions', "").split(',') if goals.get('dietary_restrictions') else [])
    if st.button("Save Goals"):
        # macro_ratios = f"{protein_ratio},{carbs_ratio},{fats_ratio}"
        update_goals(user_id, weight_goal=None, calorie_goal=calorie_target,)
        st.success("Goals saved!")