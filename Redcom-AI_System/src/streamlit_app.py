import streamlit as st
import requests
import pandas as pd
import time
import os

st.title("Radcom Traffic Classification System")

# Get API URL from environment variables for Docker flexibility
API_URL = os.getenv("INFERENCE_URL", "http://inference:8000")

task_type = st.selectbox("Select Classification Task", ["app", "att"])
uploaded_file = st.file_uploader("Upload Validation CSV", type=["csv"])

if uploaded_file and st.button("Start Analysis"):
    with st.spinner("Uploading and processing..."):
        # Send file to the FastAPI endpoint
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{API_URL}/predict/{task_type}", files=files)
        
        if response.status_code == 200:
            task_id = response.json().get("task_id")
            st.info(f"Task successfully queued. ID: {task_id}")
            
            # Poll for results
            placeholder = st.empty()
            while True:
                res_check = requests.get(f"{API_URL}/result/{task_id}").json()
                if res_check["status"] == "Done":
                    st.success("Analysis Complete!")
                    result_df = pd.read_json(res_check["result"], orient="split")
                    st.dataframe(result_df.head(10))
                    
                    # Provide download link for the tagged validation file [cite: 7]
                    csv_data = result_df.to_csv(index=False)
                    st.download_button("Download Tagged CSV", csv_data, f"{task_type}_predictions.csv")
                    break
                else:
                    placeholder.text("Model is running inference... please wait.")
                time.sleep(2)