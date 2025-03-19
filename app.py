import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import pandas as pd
import os
from dotenv import load_dotenv
# Import the functions from GenAI.py
from GenAI import process_image
st.title("Image to DataFrame")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    temp_file_path = os.path.abspath("temp_image.png")
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    with st.spinner("Processing image..."): # Add spinner here
        output = process_image(temp_file_path)

    if isinstance(output, pd.DataFrame) and not output.empty:
        st.dataframe(output)
        st.success("DataFrame created successfully!")
    os.remove(temp_file_path)

    