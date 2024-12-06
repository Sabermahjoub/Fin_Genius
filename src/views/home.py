import streamlit as st
import base64
import os

# Print current working directory and list files
#st.write("Current working directory:", os.getcwd())
#st.write("Files in directory:", os.listdir())

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    try:
        bin_str = get_base64(png_file)
        page_bg_img = '''
        <style>
        .stApp {
            background-image: url("data:image/png;base64,%s");
            background-size: cover;
        }
        </style>
        ''' % bin_str
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError as e:
        st.error(f"Error: Could not find {png_file}")
        st.write("Make sure the image is in:", os.getcwd())

# Try using absolute path
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, '../assets/home_bg.jpg')
#st.write("Trying to find image at:", image_path)

set_background(image_path)