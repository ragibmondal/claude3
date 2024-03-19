import streamlit as st
import anthropic
from claude import ClaudeLlm  # claude.py から ClaudeLlm クラスをインポート
import os
import base64

# Receive input from sidebar instead of getting API key from environment variable
api_key = st.sidebar.text_input("Enter your API key", type="password", help="Enter your API key here.")

# If the API key is not entered, display a warning and abort the process
if not api_key:
     st.error("API key required. Please enter it from the sidebar.")
else:
     client = anthropic.Anthropic(api_key=api_key)
    
# Mode selection
mode = st.sidebar.radio("Please choose a mode", ('Text', 'Vision'))

if mode == 'Text':
     # Streamlit app title
     st.title("Claude3-Streamlit")
     # receive user input
     user_input = st.text_area("Please enter text", placeholder="What is the second highest mountain in Japan? Please just tell me the name", height=200)
     # Processing when the send button is pressed
     if st.button("Send"):
         # Create an instance of ClaudeLlm class
         claude = ClaudeLlm(client, user_input)
        
         col1, col2 = st.columns(2) # Split the screen into two columns
         with col1:
             st.write("Opus response:")
             st.write_stream(claude.generate_responses("claude-3-opus-20240229"))
         with col2:
             st.write("Sonnet response:")
             st.write_stream(claude.generate_responses("claude-3-sonnet-20240229"))
         # Display cost calculation results
         st.table(claude.cost_df)
         _, jpy_rate = claude.convert_usd_to_jpy(1) # dummy call to get the exchange rate of 1USD
         st.write(jpy_rate)

elif mode == 'Vision':
     st.title("Claude3-Streamlit-vision")
     uploaded_file = st.file_uploader("Please select an image file", type=["jpg", "jpeg", "png", "gif"])

     if uploaded_file is not None:
         st.image(uploaded_file, caption="Uploaded image", use_column_width=True)
         # get file extension
         prompt = st.text_area("Please enter text", placeholder="Describe the image.", height=200)
         file_extension = os.path.splitext(uploaded_file.name)[1].lower()

         # set media type based on extension
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

         # prompt settings

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
         if st.button("Send"):
             # Create an instance of ClaudeLlm class
             claude = ClaudeLlm(client, user_input)
             col1, col2 = st.columns(2) # Split the screen into two columns
             with col1:
                 st.write("Opus response:")
                 st.write_stream(claude.generate_responses("claude-3-opus-20240229"))
             with col2:
                 st.write("Sonnet response:")
                 st.write_stream(claude.generate_responses("claude-3-sonnet-20240229"))
             # Display cost calculation results
             st.table(claude.cost_df)
             _, jpy_rate = claude.convert_usd_to_jpy(1) # dummy call to get the exchange rate of 1USD
             st.write(jpy_rate)
