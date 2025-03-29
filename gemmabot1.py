import streamlit as st
import openai
import re  # Added for cleaning responses

# Load API key from Streamlit secrets
api_key = st.secrets["openrouter_api_key"]

# Initialize OpenAI client for OpenRouter
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

st.title("Google: Gemma 3 27B")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input field for user message
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get response from OpenRouter
    try:
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="google/gemma-3-27b-it:free",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=512,
                stream=True
            )

            # Stream response
            full_response = ""
            response_container = st.empty()
            for chunk in response:
                if chunk.choices:
                    content = chunk.choices[0].delta.content or ""
                    full_response += content

                    # Remove \boxed{} formatting
                    cleaned_response = re.sub(r"\\boxed\{(.*?)\}", r"\1", full_response)

                    response_container.write(cleaned_response)

            # Append assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": cleaned_response})

    except Exception as e:
        st.error(f"Error: {e}")
