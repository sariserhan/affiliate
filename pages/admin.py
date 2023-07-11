import streamlit as st
import streamlit_authenticator as stauth

from backend.data.admin import Admin
from backend.data.item import Item

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
        name = st.text_input(label='Item Name', key='item_name', placeholder='Name', label_visibility='collapsed')
        description = st.text_area(label='Item Description', height=50, key='description', placeholder='Description',label_visibility='collapsed')    
        affiliate_link = st.text_input(label='Item Affiliate Link', key='affiliate_link', placeholder='Affiliate Link',label_visibility='collapsed')
        catalog_name = st.text_input(label='Catalog Name', key='catalog_name', placeholder='Catalog Name', label_visibility='collapsed')
        clicked = st.number_input(label='Num of clicked to start', value=0, key='clicked')
        uploaded_file = st.file_uploader("Choose a file")
        button = st.button(label='Submit')
        
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
        
            if button:
                st.write(name)
                item = Item(name=name)
                item.create_item(name=name, description=description, image_path_or_byte=bytes_data, affiliate_link=affiliate_link, catalog_name=catalog_name, clicked=int(clicked))
