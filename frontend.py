import requests
import json
import tempfile
import os
import streamlit as st
import time

BACKEND_URL = "https://psychic-adventure-p4w6pqpgxw9c6gp6-8000.app.github.dev"

def chat(user_input, data, session_id=None):
    """
    Sends a user input to a chat API and returns the response.

    Args:
        user_input (str): The user's input.
        data (str): The data source.
        session_id (str, optional): Session identifier. Defaults to None.

    Returns:
        tuple: A tuple containing the response answer and the updated session_id.
    """
    try:
        url = BACKEND_URL + "/chat"
        payload = {"user_input": user_input, "data_source": data}
        if session_id:
            payload["session_id"] = session_id

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        return response_data["response"]["answer"], response_data.get("session_id")
    except requests.RequestException as e:
        st.error(f"Chat request failed: {e}")
        return "Sorry, something went wrong.", session_id

def upload_file(file_path):
    """
    Uploads a file to a specified API endpoint.

    Args:
        file_path (str): The path to the file to be uploaded.

    Returns:
        str: The file path returned by the API or None if failed.
    """
    try:
        filename = os.path.basename(file_path)
        url = BACKEND_URL + "/uploadFile"
        files = [("data_file", (filename, open(file_path, "rb"), "application/pdf"))]
        headers = {"accept": "application/json"}
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()
        return response.json().get("file_path")
    except requests.RequestException as e:
        st.error(f"File upload failed: {e}")
        return None

# Set page configuration for the Streamlit app
st.set_page_config(page_title="Document Chat", page_icon="📕", layout="wide")

# Initialize chat history and session variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "sessionid" not in st.session_state:
    st.session_state.sessionid = None

# Allow user to upload a file (PDF or DOCX)
data_file = st.file_uploader(label="Input file", accept_multiple_files=False, type=["pdf", "docx"])
st.divider()

# Process the uploaded file if available
if data_file is not None:
    # Save the file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf" if data_file.type == "application/pdf" else ".docx") as temp_file:
        temp_file.write(data_file.getbuffer())
        temp_file_path = temp_file.name

    # Upload the file to a specified API endpoint
    s3_upload_url = upload_file(file_path=temp_file_path)
    
    # Remove the temporary file
    os.remove(temp_file_path)
    
    if s3_upload_url is None:
        st.error("Failed to upload file.")
    else:
        s3_upload_url = s3_upload_url.split("/")[-1]

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("You can ask any question"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                if st.session_state.sessionid is None:
                    # If no existing session ID, start a new session
                    assistant_response, session_id = chat(prompt, data=s3_upload_url, session_id=None)
                    st.session_state.sessionid = session_id
                else:
                    # If existing session ID, continue the session
                    assistant_response, session_id = chat(prompt, session_id=st.session_state.sessionid, data=s3_upload_url)

                message_placeholder = st.empty()
                full_response = ""

                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.05)  # Adjust the delay as needed

                message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
