import streamlit as st
import anthropic
from claude import ClaudeLlm
import os
import base64

# Get API key from the environment variable
api_key = os.environ.get("ANTHROPIC_API_KEY")

# If the API key is not provided, display an error message and exit
if not api_key:
    st.error("API key is not set in the environment variable. Please set it and try again.")
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

# Initialize user chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit app title and layout
st.set_page_config(page_title="Claude3-Streamlit", layout="wide")

# Mode selection
mode = st.sidebar.radio("Please choose a mode", ('Text', 'Vision'), key="mode")

# Streamlit app content
if mode == 'Text':
    st.title("Claude3-Streamlit - Text Mode")

    # Receive user input
    user_input = st.text_area("Please enter text", placeholder="What is the second highest mountain in Japan? Please just tell me the name", height=200, key="text_input")

    # Processing when the send button is pressed
    if st.button("Send", key="send_text"):
        # Create an instance of ClaudeLlm class
        claude = ClaudeLlm(client, user_input)
        st.write("Opus response:")
        opus_response = claude.generate_responses("claude-3-opus-20240229")
        st.success(opus_response)

        # Append user input and Opus response to chat history
        st.session_state.chat_history.append({"user": user_input, "assistant": opus_response})

    # Display chat history
    st.subheader("Chat History")
    for chat in st.session_state.chat_history:
        st.markdown(f"**User:** {chat['user']}")
        st.markdown(f"**Assistant:** {chat['assistant']}")

elif mode == 'Vision':
    st.title("Claude3-Streamlit - Vision Mode")

    # File uploader
    uploaded_file = st.file_uploader("Please select an image file", type=["jpg", "jpeg", "png", "gif"], key="file_uploader")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded image", use_column_width=True)

        # Get file extension
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        # Set media type based on extension
        if file_extension in [".jpg", ".jpeg"]:
            image_media_type = "image/jpeg"
        elif file_extension == ".png":
            image_media_type = "image/png"
        elif file_extension == ".gif":
            image_media_type = "image/gif"
        else:
            st.error("Unsupported file format.")
            st.stop()

        image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")

        # Prompt settings
        prompt = st.text_area("Please enter text", placeholder="Describe the image.", height=200, key="image_prompt")

        user_input = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": image_media_type,
                    "data": image_data,
                },
            },
            {
                "type": "text",
                "text": prompt
            }
        ]

        if st.button("Send", key="send_image"):
            # Create an instance of ClaudeLlm class
            claude = ClaudeLlm(client, user_input)
            st.write("Opus response:")
            opus_response = claude.generate_responses("claude-3-opus-20240229")
            st.success(opus_response)

            # Append user input and Opus response to chat history
            st.session_state.chat_history.append({"user": f"Image: {prompt}", "assistant": opus_response})

    # Display chat history
    st.subheader("Chat History")
    for chat in st.session_state.chat_history:
        st.markdown(f"**User:** {chat['user']}")
        st.markdown(f"**Assistant:** {chat['assistant']}")
