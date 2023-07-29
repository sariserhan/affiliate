import os
import time
import openai
import base64
import streamlit as st

from io import BytesIO
from PIL import Image

from backend.data.item import Item
from streamlit.components.v1 import html

openai.organization = "org-KAv10qRlhbdtXmwkdkuET5TP"
openai.api_key = os.getenv("OPENAI_API_KEY")
models = openai.Model.list()


def ask_ai(message_to_ask: str):
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f'{message_to_ask}'}])
    return chat_completion.choices[0].message.content


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
    
    
def get_progress_bar(my_bar, progress_text: str):
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.progress(100, text='Completed')
    time.sleep(1)
    my_bar.empty()
    
    
def get_img_with_href(local_img_path, context, target_url = None):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    if target_url:
        html_code = f'''
                        <a href="{target_url}">
                            <img src="data:image/{img_format};base64,{bin_str}" alt="{context}"/>
                        </a>
                    '''
    else:
        html_code = f'<img src="data:image/{img_format};base64,{bin_str}" alt="{context}" height="25" />'        
    return html_code


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        