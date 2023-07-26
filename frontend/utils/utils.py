
import base64
import streamlit as st

from io import BytesIO
from PIL import Image

from backend.data.item import Item
from streamlit.components.v1 import html


@st.cache_data(show_spinner=False)
def get_image(image_name, selected_catalog, resize = None):
    image_data = Item().get_image_data(name=image_name, catalog=selected_catalog)
    image = Image.open(BytesIO(image_data))
    if resize:
        return image.resize((resize[0], resize[1]), Image.ANTIALIAS)
    return image


# Function to convert image to base64 encoding
def pil_image_to_base64(image):
    img_buffer = BytesIO()
    image.save(img_buffer, format="PNG")  # You can change the format to JPEG if needed
    return base64.b64encode(img_buffer.getvalue()).decode()


# Navigates in the new page
def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script> 
    """ % (url)
    html(open_script, height=0)
    
    
# Navigates in the same page
def nav_to(url): 
    nav_script = """
                    <meta http-equiv="refresh" content="0; url='%s'" target="_blank">                    
                 """ % (url)
    st.write(nav_script, unsafe_allow_html=True)