"""
SREnity - Enterprise SRE Agent
Streamlit Chat Interface

A production-ready SRE incident response agent powered by LangGraph ReAct pattern
with BM25 + Reranker retrieval and web search capabilities.
"""

import streamlit as st
import sys
from pathlib import Path
from dotenv import load_dotenv
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

# Import our agent
from src.agents.sre_agent import SREAgent

# Page configuration
st.set_page_config(
    page_title="SREnity - SRE Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-response {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        color: #212529;
    }
    .agent-response h1, .agent-response h2, .agent-response h3 {
        color: #1f77b4;
    }
    .agent-response code {
        background-color: #e9ecef;
        color: #d63384;
        padding: 0.2rem 0.4rem;
        border-radius: 0.25rem;
        font-family: 'Courier New', monospace;
    }
    .agent-response pre {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.25rem;
        padding: 1rem;
        overflow-x: auto;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff7f0e;
        margin: 1rem 0;
        color: #1565c0;
    }
    .tool-usage {
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.9rem;
        color: #6c757d;
        margin: 0.5rem 0;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
    /* Fix Streamlit chat input styling */
    .stChatInput > div > div > input {
        background-color: white;
        color: #212529;
    }
    .stChatInput > div > div > input::placeholder {
        color: #6c757d;
    }
    
    /* Chat bubble styles */
    .chat-container {
        display: flex;
        margin: 1rem 0;
    }
    .chat-bubble {
        max-width: 70%;
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        word-wrap: break-word;
        position: relative;
    }
    .user-bubble {
        background-color: transparent;
        color: white;
        border: 1px solid #6c757d;
        margin-left: auto;
        border-bottom-right-radius: 0.25rem;
    }
    .agent-bubble {
        background-color: transparent;
        color: #212529;
        border: none;
        margin-right: auto;
        padding: 0;
    }
    .chat-label {
        font-size: 0.8rem;
        font-weight: bold;
        margin-bottom: 0.25rem;
        color: #6c757d;
    }
    .user-label {
        text-align: right;
    }
    .agent-label {
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "agent_initialized" not in st.session_state:
    st.session_state.agent_initialized = False

def initialize_agent():
    """Initialize the SRE agent"""
    if not st.session_state.agent_initialized:
        with st.spinner("🤖 Initializing SRE Agent (loading documents and building index - this may take 30-60 seconds)..."):
            try:
                st.session_state.agent = SREAgent()
                st.session_state.agent_initialized = True
                st.success("✅ Agent initialized successfully! Ready for queries.")
                st.rerun()  # Force sidebar to update
                return True
            except Exception as e:
                st.error(f"❌ Failed to initialize agent: {str(e)}")
                return False
    return True

def display_message(message, is_user=False):
    """Display a message in the chat with bubble styling for user only"""
    if is_user:
        st.markdown(f"""
        <div class="chat-container">
            <div style="flex: 1; text-align: right;">
                <div class="chat-label user-label">👤 You</div>
                <div class="chat-bubble user-bubble">{message}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-container">
            <div style="flex: 1; text-align: left;">
                <div class="chat-label agent-label">🤖 SREnity</div>
                <div>{message}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 SREnity - Enterprise SRE Agent</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 About SREnity")
        st.markdown("""
        **SREnity** is an enterprise SRE incident response agent that:
        
        - 🔍 **Searches GitLab runbooks** using BM25 + Reranker
        - 🌐 **Web search** for latest updates and CVEs
        - 🧠 **Agentic reasoning** with LangGraph ReAct pattern
        - 🛡️ **Guardrails** to stay focused on SRE topics
        
        **Try asking about:**
        - Redis memory monitoring
        - PostgreSQL connection issues
        - Elasticsearch cluster health
        - GitLab CI/CD problems
        - Kubernetes troubleshooting
        """)
        
        st.header("🔧 Agent Status")
        if st.session_state.agent_initialized:
            st.success("✅ Agent Ready")
        else:
            st.warning("⏳ Initializing...")
        
        st.header("📊 Capabilities")
        st.markdown("""
        - **Runbook Search**: BM25 + Cohere Reranker
        - **Web Search**: Tavily for latest info
        - **Coverage**: Redis-focused GitLab runbooks
        """)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    st.header("💬 Chat with SREnity")
    
    # Initialize agent
    if not initialize_agent():
        st.stop()
    
    # Display chat messages
    for message in st.session_state.messages:
        display_message(message["content"], message["is_user"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about SRE procedures, troubleshooting, or incident response..."):
        # Add user message to chat
        st.session_state.messages.append({"content": prompt, "is_user": True})
        display_message(prompt, is_user=True)
        
        # Get agent response
        with st.spinner("🤔 Thinking (searching runbooks and generating response)..."):
            try:
                # Create a placeholder for the response
                response_placeholder = st.empty()
                
                # Get response from agent
                response = st.session_state.agent.invoke(prompt, verbose=False)
                
                # Display response
                with response_placeholder.container():
                    st.markdown("**🤖 SREnity:**")
                    st.markdown(response)
                
                # Add to messages
                st.session_state.messages.append({"content": response, "is_user": False})
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                response_placeholder.error(error_msg)
                st.session_state.messages.append({"content": error_msg, "is_user": False})
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
        <strong>SREnity</strong> - Enterprise SRE Agent | Powered by LangGraph ReAct + BM25 + Reranker
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
