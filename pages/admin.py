import random
import logging
import streamlit as st
import streamlit_authenticator as stauth

from streamlit_toggle import st_toggle_switch
from backend.data.admin import Admin
from backend.data.item import Item
from backend.data.catalog import Catalog

logging.basicConfig(level=logging.DEBUG)

st.set_page_config(layout='centered')

# --- ADMIN AUTHENTICATION

creds = Admin().fetch_records()

names=[]
usernames = []
passwords = []

for cred in creds:
    names.append(cred['name'])
    usernames.append(cred['key'])
    passwords.append(cred['password'])

hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {}
for i in range(len(usernames)):
    credentials["usernames"] = {
                usernames[i]:
                    {
                        "name":names[i],
                        "password":hashed_passwords[i]
                    }
                }

authenticator = stauth.Authenticate(credentials, 'admin_page', 'auth', cookie_expiry_days=1)

user_name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error("Username/password combination incorrect. Please try again.")
if authentication_status == None:
    st.warning("Please enter username and password to login.")
if authentication_status:
    authenticator.login("Logout", "sidebar")
    st.sidebar.title('Welcome *%s*' % (user_name))

# --- CREATE ITEM
    with st.container():
        st.header('Create New Item')
        
        f_clicked_toggle = st_toggle_switch(
            label="Enable f-clicked?",
            key="switch_1",
            default_value=False,
            label_after=False,
            inactive_color="#D3D3D3",  # optional
            active_color="#11567f",  # optional
            track_color="#29B5E8",  # optional
        )
        catalog_list = []
        catalogs = Catalog().fetch_records()        
        for catalog in catalogs:
            catalog_list.append(catalog['name'])
        
        catalog_list.append("Create New Catalog")
        
        name = st.text_input(label='Item Name', key='item_name', placeholder='Name', label_visibility='collapsed')
        description = st.text_area(label='Item Description', height=50, key='description', placeholder='Description',label_visibility='collapsed')    
        affiliate_link = st.text_input(label='Item Affiliate Link', key='affiliate_link', placeholder='Affiliate Link',label_visibility='collapsed')
        catalog_name = st.selectbox(label="Choose Category or Create New", options=catalog_list)
        if catalog_name == "Create New Catalog":
            catalog_name = st.text_input(label='Catalog Name', key='catalog_name', placeholder='Catalog Name', label_visibility='collapsed')
        clicked = st.number_input(label='Num of clicked to start', value=0, key='clicked')
        if f_clicked_toggle:
            random_num = random.randint(1000, 5000)
            f_clicked = st.number_input(label='Num of f_clicked to start', value=random_num, key='f_clicked')
            
        uploaded_file = st.file_uploader("Choose a file")
        button = st.button(label='Submit')
        
        if uploaded_file is not None:
            image_val = uploaded_file.getvalue()
            image_name = uploaded_file.name
            print(image_name)
        
            if button:                
                try:
                    item = Item()
                    if f_clicked_toggle:
                        item.create_item(name=name, description=description, image_path=image_val, image_name=image_name ,affiliate_link=affiliate_link, catalog_name=catalog_name, clicked=int(clicked), f_clicked=int(f_clicked))
                    else:
                        item.create_item(name=name, description=description, image_path=image_val, image_name=image_name, affiliate_link=affiliate_link, catalog_name=catalog_name, clicked=int(clicked))
                    st.success(name)
                except Exception as e:
                    st.error("Something went wrong!")
                    logging.error(e)
                    
                    
                
