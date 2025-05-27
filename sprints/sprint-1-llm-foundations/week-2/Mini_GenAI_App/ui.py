import streamlit as st
import requests

st.title("📋 Mini GenAI Summarizer")

st.write("Upload a text file to generate a summary.")

uploaded_file = st.file_uploader("Choose a text file", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    st.write("### Uploaded Text:")
    st.text_area("Uploaded Text", text, height=150)

    if st.button("Summarize"):
        st.write("⏳ Generating Summary...")

        # Make a request to your FastAPI backend
        response = requests.post(
            "http://localhost:8000/summarize",
            files={"file": uploaded_file.getvalue()}
        )

        if response.status_code == 200:
            summary = response.json().get("summary")
            st.success("✅ Summary Generated:")
            st.text_area("Summary", summary, height=150)
        else:
            st.error("❌ Failed to generate summary. Please try again.")
