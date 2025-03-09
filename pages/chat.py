import streamlit as st
from agents import get_health_assistant
from crewai import Task

def app():
    st.title("Chat with AI Health Assistant")
    user_id = st.session_state['user_id']

    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = []

    if 'health_assistant' not in st.session_state:
        st.session_state['health_assistant'] = get_health_assistant(user_id)

    for msg in st.session_state['conversation']:
        st.write(f"**{msg['role']}**: {msg['content']}")

    user_input = st.text_input("Ask a question:")
    if st.button("Send"):
        st.session_state['conversation'].append({"role": "User", "content": user_input})
        # Create a Task object for the user input
        task = Task(description=user_input, expected_output="A response to the user's query")
        response = st.session_state['health_assistant'].execute_task(task)
        st.session_state['conversation'].append({"role": "Assistant", "content": response})
        st.rerun()