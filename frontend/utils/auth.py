import streamlit as st
import streamlit_authenticator as stauth

from backend.data.admin import Admin


# --- ADMIN AUTHENTICATION
def auth():
    creds = Admin().fetch_records()

    names = []
    usernames = []
    passwords = []

    for cred in creds:
        names.append(cred['name'])
        usernames.append(cred['key'])
        passwords.append(cred['password'])

    hashed_passwords = stauth.Hasher(passwords).generate()

    credentials = {
        "usernames": {
            usernames[i]: {"name": names[i], "password": hashed_passwords[i]}
        }
        for i in range(len(usernames))
    }
    authenticator = stauth.Authenticate(
        credentials, 'admin_page', 'auth', cookie_expiry_days=1)

    user_name, authentication_status, username = authenticator.login(
        'Login', 'main')

    if authentication_status == False:
        st.error("Username/password combination incorrect. Please try again.")
        return False
    if authentication_status is None:
        st.warning("Please enter username and password to login.")
        return False
    if authentication_status:
        authenticator.login("Logout", "sidebar")
        st.sidebar.title(f'Welcome *{user_name}*')
        return True
