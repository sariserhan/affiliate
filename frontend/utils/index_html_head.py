import logging
import os
import re

import streamlit as st

logging.basicConfig(level=logging.DEBUG)

def index_html_add_to_head(context: str, add_head: str, add_body: str = ''):
    # Insert the script in the head tag of the static template inside your virtual
    a = f'{os.path.dirname(st.__file__)}/static/index.html'
    with open(a, 'r') as f:
        data=f.read()
        if context == "adsense":
            if "googlesyndication" not in data and len(re.findall('UA-', data))==0:
                with open(a, 'w') as ff:
                    newdata_head = re.sub('<head>', f'<head>{add_head}', data)
                    ff.write(newdata_head)
                    if add_body:
                        newdata_body = re.sub('<body>', f'<body>{add_body}', data)
                        ff.write(newdata_body)
                    logging.info(f"{a} is updated with Google Adsense tracking code")
        elif context == "analytics":
            if "googletagmanager" in data:
                logging.warning("Google Analytics is already set")
            elif len(re.findall('UA-', data))==0:
                with open(a, 'w') as ff:
                    newdata = re.sub('<head>', f'<head>{add_head}', data)
                    ff.write(newdata)
                    logging.info(f"{a} is updated with Google Analytics tracking code")
        elif context == "impact":
            if "ir-site-verification-token" in data:
                logging.warning("Google Adsense is already set")
            elif len(re.findall('UA-', data))==0:
                with open(a, 'w') as ff:
                    newdata_head = re.sub('<head>', f'<head>{add_head}', data)
                    ff.write(newdata_head)
                    logging.info(f"{a} is updated with Impact Id")
    return