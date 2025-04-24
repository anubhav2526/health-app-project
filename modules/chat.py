import streamlit as st
from agents import get_health_assistant
from crewai import Task

def app():
    st.title("Chat with AI Health Assistant")
    user_id = st.session_state['user_id']

    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = []

    # Create (or retrieve) the Health Assistant agent.
    if 'health_assistant' not in st.session_state:
        st.session_state['health_assistant'] = get_health_assistant(user_id)

    # Display conversation history.
    for msg in st.session_state['conversation']:
        st.write(f"**{msg['role']}**: {msg['content']}")

    # Input field for user's question.
    user_input = st.text_input("Ask a question:")
    if st.button("Send"):
        st.session_state['conversation'].append({"role": "User", "content": user_input})
        
        # Check if health_assistant is an Agent or a dict with error message
        health_assistant = st.session_state['health_assistant']
        
        if isinstance(health_assistant, dict) and 'error' in health_assistant:
            # Handle error case
            error_msg = health_assistant['error']
            response = f"Sorry, I couldn't process your request. {error_msg} Please contact the app administrator."
        else:
            try:
                # Attempt to use the agent
                task = Task(description=user_input, expected_output="A response to the user's query")
                response = health_assistant.execute_task(task)
            except Exception as e:
                # Fallback response if agent execution fails
                response = f"I apologize, but I encountered an error processing your request: {str(e)}. Please try again later or contact support."
        
        st.session_state['conversation'].append({"role": "Assistant", "content": response})
        try:
            st.experimental_rerun()
        except AttributeError:
            pass
