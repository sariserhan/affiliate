import os
import re
import logging
import streamlit as st

logging.basicConfig(level=logging.DEBUG)

def index_html_add_to_head(context: str, add_head: str, add_body: str = ''):
    # Insert the script in the head tag of the static template inside your virtual
    a=os.path.dirname(st.__file__)+'/static/index.html'
    with open(a, 'r') as f:
        data=f.read()
        if context == "analytics":
            if "googletagmanager" not in data:
                if len(re.findall('UA-', data))==0:
                    with open(a, 'w') as ff:
                        newdata=re.sub('<head>','<head>'+add_head,data)
                        ff.write(newdata)
                        logging.info(f"{a} is updated with Google Analytics tracking code")
            else:
                logging.warning("Google Analytics is already set")
        elif context == "adsense":
            if "googlesyndication" not in data:
                if len(re.findall('UA-', data))==0:
                    with open(a, 'w') as ff:
                        newdata_head=re.sub('<head>','<head>'+add_head,data)                        
                        ff.write(newdata_head)
                        if add_body:
                            newdata_body=re.sub('<body>','<body>'+add_body,data)
                            ff.write(newdata_body)
                        logging.info(f"{a} is updated with Google Adsense tracking code")
            else:
                logging.warning("Google Adsense is already set")
        else:
            pass
                    
    return