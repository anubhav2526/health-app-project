import streamlit as st
from agents import get_health_assistant

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
        
        # Get health assistant
        health_assistant = st.session_state['health_assistant']
        
        try:
            # Create a simple task object if needed
            class SimpleTask:
                def __init__(self, query):
                    self.description = query
            
            task = SimpleTask(user_input)
            response = health_assistant.execute_task(task)
        except Exception as e:
            # Fallback response if assistant execution fails
            response = f"I apologize, but I encountered an error processing your request: {str(e)}. Please try again later or contact support."
        
        st.session_state['conversation'].append({"role": "Assistant", "content": response})
        try:
            st.experimental_rerun()
        except AttributeError:
            pass
