import random
import logging
import streamlit as st
import streamlit_authenticator as stauth

from backend.data.admin import Admin
from backend.data.item import Item
from backend.data.catalog import Catalog
from backend.data.affiliate_partner import Affiliate_Partner

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
        tab1, tab2 = st.tabs(["Create", "Delete"])
        with tab1:
            st.header('Create New Item')
            
            f_clicked_toggle = None
            
            try:
                from streamlit_toggle import st_toggle_switch
                # TOGGLE SWITCH FOR f_clicked
                f_clicked_toggle = st_toggle_switch(
                    label="Enable f-clicked?",
                    key="switch_1",
                    default_value=False,
                    label_after=False,
                    inactive_color="#D3D3D3",  # optional
                    active_color="#11567f",  # optional
                    track_color="#29B5E8",  # optional
                )
            except:
                logging.warning('Toggle Switch in not available')
            
            # GET CATALOG FROM DB
            catalog_list = []
            catalogs = Catalog().fetch_records()        
            for catalog in catalogs:
                catalog_list.append(catalog['name'])
                
            catalog_list.append("Add New Catalog")
                
            # GET AFFILIATE PARTNER FROM DB
            affiliate_partner_list = []
            affiliate_partners = Affiliate_Partner().fetch_records()        
            for affiliate_partner in affiliate_partners:
                affiliate_partner_list.append(affiliate_partner['key'])
            
            affiliate_partner_list.append("Add New Partner")
            
            name = st.text_input(label='Item Name', key='item_name', placeholder='Name', label_visibility='collapsed')
            description = st.text_area(label='Item Description', height=50, key='description', placeholder='Description',label_visibility='collapsed')    
            affiliate_link = st.text_input(label='Item Affiliate Link', key='affiliate_link', placeholder='Affiliate Link',label_visibility='collapsed')
            catalog_names = st.multiselect(label="Choose Category", options=catalog_list)
            if "Add New Catalog" in catalog_names:
                new_catalog_name = st.text_input(label='Add Catalog Name', key='catalog_name', placeholder='Catalog Name', label_visibility='collapsed')
                catalog_names.append(new_catalog_name)        
                catalog_names.remove('Add New Catalog')
                
            affiliate_partner = st.selectbox(label="Choose Partner", options=affiliate_partner_list)
            if "Add New Partner" == affiliate_partner:
                affiliate_partner = st.text_input(label='Add Partner Name', key='partner_name', placeholder='Partner Name', label_visibility='collapsed')
                
            if f_clicked_toggle:
                random_num = random.randint(1000, 5000)
                f_clicked_val = st.number_input(label='Num of f_clicked to start', value=random_num, key='f_clicked')
                
            uploaded_file = st.file_uploader("Choose a file")
            button = st.button(label='Create')
            
            if uploaded_file is not None:
                image_val = uploaded_file.getvalue()
                image_name = uploaded_file.name
            
                if button:                
                    try:
                        item = Item()                    
                        item.create_item(
                            name=name, 
                            description=description,
                            image_path=image_val,
                            image_name=image_name,
                            affiliate_link=affiliate_link,
                            affiliate_partner=affiliate_partner,
                            catalog_names=catalog_names,
                            f_clicked=int(f_clicked_val) if f_clicked_toggle else 0
                            )
                        st.success(f'Item added into DB: {name}')
                    except Exception as e:
                        st.error("Something went wrong!")
                        logging.error(e)

        with tab2:
            st.header('Delete an Item')
            
            name = st.text_input(label='Item Name', key='item_name_to_delete', placeholder='Name', label_visibility='collapsed')
            key = name.replace(' ',f'_')
            
            button = st.button(label='Delete')
            if button:
                item_key = Item().get_record(key)['key']
                if key == item_key:
                    if Item().delete_item(key=key, name=name):
                        st.success(f'Item is deleted {name}')
                    else:
                        st.error('Error in deleting item')
            