import random
import logging
import streamlit as st
import streamlit_authenticator as stauth

from functools import partial

from backend.data.admin import Admin
from backend.data.item import Item
from backend.data.catalog import Catalog
from backend.data.affiliate_partner import Affiliate_Partner
from backend.email.send_email import EmailService

from frontend.column_setup import get_image

logging.basicConfig(level=logging.DEBUG)

st.set_page_config(layout='centered')

if "state_dict" not in st.session_state:
    st.session_state.state_dict = {}

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

    with st.container():
        tab1, tab2, tab3 = st.tabs(["Add New Item", "Delete Item", "Send Email"])
        
        # --- SHARED AREA
        catalog_list = []
        catalogs = Catalog().fetch_records()
        for catalog in catalogs:
            catalog_list.append(catalog['name'])
            
        item_obj = Item()
        
        # --- ADD ITEM
        with tab1:
            # with st.form(key="create-form", clear_on_submit=True):
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
            
            catalog_names = st.multiselect(label="Choose Category or Add New", options=catalog_list[::-1])
            if "Add New Catalog" in catalog_names:
                new_catalog_name = st.text_input(label='Add Catalog Name', key='catalog_name', placeholder='Catalog Name', label_visibility='collapsed')
                catalog_names.append(new_catalog_name)        
                catalog_names.remove('Add New Catalog')
                
            affiliate_partner = st.selectbox(label="Choose Affiliate Partner or Add New", options=affiliate_partner_list)
            if "Add New Partner" == affiliate_partner:
                affiliate_partner = st.text_input(label='Add Partner Name', key='partner_name', placeholder='Partner Name', label_visibility='collapsed')
                
            if f_clicked_toggle:
                random_num = random.randint(1000, 5000)
                f_clicked_val = st.number_input(label='Num of f_clicked to start', value=random_num, key='f_clicked')
                
            uploaded_file = st.file_uploader("Choose a file")
            st.write('---')
            button = st.button(label='Create')
            
            if uploaded_file is not None:
                image_val = uploaded_file.getvalue()
                image_name = uploaded_file.name
            
                if button:                
                    try:
                        item_obj.create_item(
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
                        
        # --- DELETE ITEM
        with tab2:
            # with st.form(key="delete-form", clear_on_submit=True):
            st.header('Delete an Item')
            
            name = st.text_input(label='Item Name', key='item_name_to_delete', placeholder='Item Name to Delete', label_visibility='collapsed')
            key = name.replace(' ',f'_')
            st.write('---')
            
            button = st.button(label='Delete')
            if button:
                item_key = item_obj.get_record(key)['key']
                if key == item_key:
                    if item_obj.delete_item(key=key, name=name):
                        st.success(f'Item is deleted {name}')
                    else:
                        st.error('Error in deleting item')
                        
        # --- SEND EMAIL
        with tab3:
            item_list = []
            image_list= []
            image_name = None
            
            def on_selectbox_change(selected_catalog):
                pass
            catalog_list.remove('Add New Catalog')
            selected_catalog = st.selectbox(label="Choose Category", options=catalog_list)
            if selected_catalog:
                for item in item_obj.fetch_records():
                    if item['catalog'] == selected_catalog and not item['email_sent']:
                        item_list.append(item['name'])
                        image_list.append(item['image_name'])
                        
            selected_item = st.selectbox(label="Choose Item to Send", 
                                         options=item_list, 
                                         on_change=on_selectbox_change, args=(selected_catalog, )
                                         )
            for image_name_in_list in image_list:
                if selected_item in image_name_in_list:
                    image_name = image_name_in_list
                    break
            if image_name:
                image = get_image(image_name=image_name, selected_catalog=selected_catalog)
                st.image(image=image, caption=name, use_column_width=True)
            else:
                st.warning("No Product to send in this category")
            st.write('---')
            
            button = st.button(label='Send')
            
            if button:
                email_obj = EmailService()
                emails_to_send = email_obj.get_subscription_list()
                
                item_dict = email_obj.get_item(selected_item)
                for email in emails_to_send:
                    if not item_dict['email_sent']:
                        try:
                            email_obj.send_email(recipient_email=email, item_dict=item_dict)
                            st.success(f'Email sent to {email}')
                            try:
                                item_obj.update_record(key=item_dict['key'], updates={'email_sent': True})
                                logging.info(f"{item_dict['name']} updated in DB")
                            except Exception as e:
                                logging.error(f"Error in updating {item_dict['name']} in DB {e}")
                        except Exception as e:
                            st.error(f'Error sending email --> {e}')                            

