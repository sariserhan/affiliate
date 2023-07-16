import os
import re
import logging
import streamlit as st


from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

@st.cache_resource
def google_analytics_setup():
    
    # --- GOOGLE ANALYTICS SETUP
    google_tag_id = os.getenv("GOOGLE_ANALYTICS_TAG_ID")

    beginning = f'<!-- Google Analytics tracking code --><script async src="https://www.googletagmanager.com/gtag/js?id={google_tag_id}"></script>'
    middle = """<script>
                    window.dataLayer = window.dataLayer || [];
                    function gtag(){dataLayer.push(arguments);}
                    gtag('js', new Date());
            """
    end = f"gtag('config', '{google_tag_id}'); </script>"

    google_anayltics_script = beginning + middle + end

    # Insert the script in the head tag of the static template inside your virtual
    a=os.path.dirname(st.__file__)+'/static/index.html'
    with open(a, 'r') as f:
        data=f.read()
        logging.info(f'INDEX.HTML: {a} INDEX-CONTENT: {data}\n')
        if "googletagmanager" not in data:            
            if len(re.findall('UA-', data))==0:
                with open(a, 'w') as ff:
                    newdata=re.sub('<head>','<head>'+google_anayltics_script,data)
                    ff.write(newdata)
                    logging.info("index.html file is updated with Google Analytics tracking code")
                    logging.info(f"NEW-INDEX-CONTENT:{newdata}")
        else:
            logging.warning("Google Analytics is already set")
                    
    return st.markdown(google_anayltics_script, unsafe_allow_html=True)