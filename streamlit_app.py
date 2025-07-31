import streamlit as st
import requests
import json
import uuid
from datetime import datetime
import time
import os

# Configure Streamlit page
st.set_page_config(
    page_title="AI Agent Workshop",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def call_agent_api(message: str, session_id: str = None):
    """Call the FastAPI agent endpoint"""
    try:
        # Debug info
        st.write(f"🔄 Calling API with message: {message[:50]}...")
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={
                "message": message,
                "session_id": session_id
            },
            timeout=30
        )
        # Debug info
        st.write(f"📡 API Response Status: {response.status_code}")
        response.raise_for_status()
        result = response.json()
        # Debug info
        st.write(f"✅ API Response received: {result.get('reply', '')[:50]}...")
        return result
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error calling API: {e}")
        return None


def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def display_message(role: str, content: str, timestamp: str = None):
    """Display a chat message with styling"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M:%S")

    if role == "user":
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col2:
                st.markdown(f"""
                <div style="background-color: #f0f2f6; border-left: 4px solid #1f77b4; padding: 12px; border-radius: 8px; margin: 8px 0; color: #262730;">
                    <strong style="color: #1f77b4;">🧑 You</strong> 
                    <small style="color: #888; float: right;">({timestamp})</small><br>
                    <div style="margin-top: 6px; color: #262730;">{content}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div style="background-color: #ffffff; border-left: 4px solid #28a745; padding: 12px; border-radius: 8px; margin: 8px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <strong style="color: #28a745;">🤖 Agent</strong> 
                    <small style="color: #888; float: right;">({timestamp})</small><br>
                    <div style="margin-top: 6px; color: #262730;">{content}</div>
                </div>
                """, unsafe_allow_html=True)


def main():
    # Header
    st.title("🤖 AI Agent Workshop")
    st.markdown("**Interactive Frontend for Testing Your ReAct Agent**")

    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")

        # API Health Check
        health_status = check_api_health()
        if health_status:
            st.success("✅ API is running")
        else:
            st.error("❌ API is not running")
            st.markdown("Please start the API with: `make serve`")
            return

        st.divider()

        # Session Management
        st.subheader("💬 Session")
        if st.button("🔄 New Conversation"):
            st.session_state.clear()
            st.rerun()

        # Show current session ID
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

        st.text_input(
            "Session ID:",
            value=st.session_state.session_id[:8] + "...",
            disabled=True,
            help="Unique identifier for this conversation"
        )

        # Debug info
        if st.checkbox("Show Debug Info"):
            st.session_state.debug_mode = True
        else:
            st.session_state.debug_mode = False

        st.divider()

        # Agent Information
        st.subheader("🧠 Agent Info")
        st.markdown("""
        **Model:** qwen/qwen3-coder:free  
        **Tools Available:**
        - 🔍 Exa Search
        - ➕ Add Function
        - 💾 Memory (MemorySaver)
        """)

        st.divider()

        # Example Queries
        st.subheader("💡 Try These Examples")
        example_queries = [
            "Hello, how are you?",
            "Search for information about AI agents",
            "Add 15 to get the result",
            "What did we talk about earlier?",
            "Search for LangGraph documentation"
        ]

        for query in example_queries:
            if st.button(f"📝 {query}", key=f"example_{hash(query)}"):
                st.session_state.example_query = query

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Debug information
    if st.session_state.get('debug_mode', False):
        st.write(
            f"🐛 Debug: {len(st.session_state.messages)} messages in history")
        st.write(f"🐛 Session ID: {st.session_state.session_id}")

    # Chat Interface
    st.subheader("💬 Chat with Your Agent")

    # Display conversation history
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 20px;">
            👋 Welcome! Start a conversation with your AI agent.<br>
            Your agent has access to search tools and can remember our conversation.
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            display_message(
                message["role"],
                message["content"],
                message.get("timestamp", "")
            )

    # Input form
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])

        with col1:
            # Use example query if available
            default_value = st.session_state.get('example_query', '')
            user_input = st.text_input(
                "Message:",
                placeholder="Ask your agent anything...",
                value=default_value
            )

        with col2:
            submitted = st.form_submit_button(
                "Send 🚀", use_container_width=True)

    # Process user input
    if submitted:
        # Check for example query first, then user input
        message_to_send = user_input.strip()
        if not message_to_send and 'example_query' in st.session_state:
            message_to_send = st.session_state.example_query.strip()

        # Clear the example query after using it
        if 'example_query' in st.session_state:
            del st.session_state.example_query

        if message_to_send:
            st.write("🔄 Processing your message...")  # Debug feedback

            # Add user message
            timestamp = datetime.now().strftime("%H:%M:%S")
            user_message = {
                "role": "user",
                "content": message_to_send,
                "timestamp": timestamp
            }
            st.session_state.messages.append(user_message)

            # Show typing indicator and call API
            with st.spinner("🤖 Agent is thinking..."):
                response_data = call_agent_api(
                    message_to_send, st.session_state.session_id)

            if response_data:
                # Add agent response
                agent_response = response_data.get(
                    "reply", "Sorry, I couldn't process that.")
                agent_timestamp = datetime.now().strftime("%H:%M:%S")

                agent_message = {
                    "role": "agent",
                    "content": agent_response,
                    "timestamp": agent_timestamp
                }
                st.session_state.messages.append(agent_message)

                # Update session ID if it changed
                if "session_id" in response_data:
                    st.session_state.session_id = response_data["session_id"]

                st.success("✅ Response received! Refreshing chat...")
                time.sleep(1)  # Brief pause before refresh
                st.rerun()
            else:
                st.error("❌ Failed to get response from agent. Please try again.")

    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🔧 Backend:** FastAPI + LangGraph")
    with col2:
        st.markdown("**🧠 Model:** Qwen3-Coder")
    with col3:
        if st.button("📊 View API Docs"):
            st.markdown(f"[Open API Documentation]({API_BASE_URL}/docs)")


if __name__ == "__main__":
    main()
