import streamlit as st
import requests

st.title("Youtube QnA")

st.header("Youtube Transcript QnA")

youtube_url = st.text_input("Enter Youtube URL")
if youtube_url and st.button("Upload URL"):
    with st.spinner("Uploading and processing the transcript..."):
        response1 = requests.post(
            'http://localhost:8001/upload',
            json={'youtube_url': youtube_url}
        )

    if response1.status_code == 200:
        st.success("Transcript uploaded successfully")
        st.session_state.uploaded = True
    else:
        st.error("something went wrong")

if st.session_state.get('uploaded',False):
    question = st.text_input("Ask question")
    if question and st.button("submit Question"):
        with st.spinner("Fetching answer..."):
            response2 = requests.post(
                'http://localhost:8001/answer',
                data={'question': question}
            )

        if response2.status_code == 200:
            st.write(response2.json()['answer'])