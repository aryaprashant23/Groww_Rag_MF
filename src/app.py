import streamlit as st
import sys
import os

# Ensure we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from guardrails import GuardrailManager
from rag_pipeline import RAGPipeline

# Initialize backend components and cache them to avoid reloading the models
@st.cache_resource
def get_backend():
    guardrails = GuardrailManager()
    pipeline = RAGPipeline()
    return guardrails, pipeline

# Page configuration
st.set_page_config(
    page_title="Mutual Fund FAQ Assistant",
    page_icon="📈",
    layout="centered"
)

# Header and Disclaimer
st.title("Mutual Fund FAQ Assistant 📈")
st.error("**Facts-only. No investment advice.**")
st.markdown("Welcome! I can answer factual questions about Nippon India mutual funds based solely on official documentation.")

# Load backend
with st.spinner("Initializing models... (This might take a moment on first run)"):
    guardrails, pipeline = get_backend()

# Interactive Examples
st.markdown("### Example Queries")
col1, col2, col3 = st.columns(3)

if "user_query" not in st.session_state:
    st.session_state.user_query = None

if col1.button("Exit Load"):
    st.session_state.user_query = "What is the exit load for the Nippon India Small Cap fund?"
if col2.button("Check NAV"):
    st.session_state.user_query = "What is the NAV of Nippon India small cap?"
if col3.button("Subjective Query (Blocked)"):
    st.session_state.user_query = "Is the Nippon India small cap a good fund to buy right now?"

# Chat History initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture user input via chat input OR example button click
prompt = st.chat_input("Ask a factual question about Nippon India funds...")

# Process the query
query_to_process = None
if prompt:
    query_to_process = prompt
    st.session_state.user_query = None # clear any button press
elif st.session_state.user_query:
    query_to_process = st.session_state.user_query
    st.session_state.user_query = None # process it exactly once

if query_to_process:
    # Display the user's message
    with st.chat_message("user"):
        st.markdown(query_to_process)
    st.session_state.messages.append({"role": "user", "content": query_to_process})
    
    # Generate and display the assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Fetching factual information..."):
            # Step 1: Guardrails Verification
            is_valid, refusal_msg = guardrails.validate_query(query_to_process)
            
            if not is_valid:
                # Caught by PII or Intent filter
                response = refusal_msg
            else:
                # Step 2: RAG Pipeline Generation
                result = pipeline.get_answer(query_to_process)
                response = result["answer"]
                
            st.markdown(response)
            
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
