import os
import re
import logging
import in_place
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
        elif context == "impact":
            if "ir-site-verification-token" not in data:
                if len(re.findall('UA-', data))==0:
                    with open(a, 'w') as ff:
                        newdata_head=re.sub('<head>','<head>'+add_head,data)                        
                        ff.write(newdata_head)                    
                        logging.info(f"{a} is updated with Impact Id")
            else:
                logging.warning("Google Adsense is already set")
        else:
            pass
                    
    return

def alter_index_html(old_val: str, new_val: str):
    index_file=os.path.dirname(st.__file__)+'/static/index.html'
    
    with in_place.InPlace(index_file) as file:
        for line in file:
            line = line.replace(old_val, new_val)
            file.write(line)
        file.close()
        