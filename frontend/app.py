import streamlit as st
import requests
import yaml
import os
import time

# Get project root (one level above frontend folder)
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(PROJECT_DIR, "config.yml")

# Load config
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

backend = config["backend"]
BASE_URL = f"http://{backend['host']}:{backend['port']}"
print("Backend URL:", BASE_URL)

st.title("Streamlit + FastAPI with YAML Config")

# Greet API
name = st.text_input("Enter your name")
if st.button("Greet Me"):
    response = requests.get(f"{BASE_URL}/api/greet", params={"name": name})
    st.success(response.json()["message"])

# Square API
number = st.number_input("Enter a number", value=1)
if st.button("Calculate Square"):
    response = requests.get(f"{BASE_URL}/api/square", params={"number": number})
    st.info(f"Square: {response.json()['result']}")


# --- Images at the bottom ---
IMAGE_DIR = os.path.join(PROJECT_DIR, "images")

# Get all images in folder
image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

if image_files:
    st.write("---")  # horizontal separator
    st.subheader("Gallery")
    cols = st.columns(len(image_files))
    for col, img_file in zip(cols, image_files):
        img_path = os.path.join(IMAGE_DIR, img_file)
        col.image(img_path, use_container_width=True)
else:
    st.write("No images found in the images/ folder.")


# # --- Rotating slideshow ---
# if image_files:
#     st.write("---")
#     st.subheader("Rotating Images")
#     slideshow_placeholder = st.empty()
    
#     while True:
#         for img_file in image_files:
#             img_path = os.path.join(IMAGE_DIR, img_file)
#             slideshow_placeholder.image(img_path, use_container_width=True)
#             time.sleep(2)  # Change image every 2 seconds



st.write("---")
st.subheader("IMDb Link")

# Option 1: Simple clickable link
st.markdown("[Go to IMDb](https://www.imdb.com/)")

# Option 2: Button that opens IMDb in a new tab
if st.button("Visit IMDb"):
    st.markdown(
        """
        <script>
        window.open('https://www.imdb.com/', '_blank')
        </script>
        """,
        unsafe_allow_html=True
    )

