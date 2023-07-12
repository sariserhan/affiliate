import streamlit as st
import webbrowser

from io import BytesIO
from PIL import Image

from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.keyboard_url import keyboard_to_url
from streamlit_extras.keyboard_text import key
from streamlit_extras.mention import mention
from streamlit_lottie import st_lottie
from streamlit_card import card
from st_pages import Page, hide_pages, show_pages

from frontend.footer import footer
from frontend.sidebar import sidebar
from frontend.subscription import subscription
from backend.data.item import Item


# --- NAVIGATION BAR
st.set_page_config(
    layout='wide',
    page_title="Affiliate App",
    page_icon=":books:"
)

show_pages(
    [
        Page("streamlit_app.py", "home"),
        Page("pages/admin.py", "admin")
    ]
)
hide_pages(["admin", "home"])



st.title('BestBuybyAI')

# --- CATALOG SIDE BAR
selected = sidebar()

# --- POST LIST
col1, col2 = st.columns([0.7,0.3], gap="small")

mentions_list = []

with col1:
        st.header(selected)

        # keyboard_key = []
        
        # --- ITEM LIST
        items = Item().get_record_by_catalog(catalog=selected)
        for item_index, item in enumerate(items, start=1):
            name = item["name"]
            url = item['affiliate_link']
            description = item['description']
            image_name = item['image_name']
            
            with st.form(f'{name}_form'):
                # ADD mentions to the text         
                mentions_list.append(mention(
                    label=name,
                    icon="streamlit",  # Some icons are available... like Streamlit!
                    url=item['affiliate_link'],
                ))
                # card(
                #     title="Hello Geeks!",
                #     text="Click this card to redirect to GeeksforGeeks",
                #     image="https://media.geeksforgeeks.org/wp-content/cdn-uploads/20190710102234/download3.png",
                #     url="https://www.geeksforgeeks.org/",
                # )
                st.subheader(name)      
            
                # IMAGE
                image_data = Item().get_image_data(name=image_name, catalog=selected)
                image = Image.open(BytesIO(image_data))
                st.image(image=image, caption=item['name'], width=400)
                
                # Item Description
                st.markdown(description)
                
                # --- ADD keyboard to URL
                print(item_index)
                keyboard_to_url(key=str(item_index), url=url)
                st.write(
                    f"""check out this [link]({url}) or hit {key(str(item_index), False)} on your keyboard...!""",
                    unsafe_allow_html=True,
                )
                
                # COUNTER
                if 'click_count' not in st.session_state:                    
                    st.session_state.click_count = item['clicked'] + item['f_clicked']
                                
                # FORM SUBMIT BUTTON
                if 'button_label' not in st.session_state:
                    st.session_state.click_count += 1
                    st.session_state.button_label = f"Clicked2 {st.session_state.click_count} times"
                    webbrowser.open_new_tab(url)
                    
                    
                def submit_form():
                    st.session_state.button_label = f"Clicked {st.session_state.click_count} times"
                form_button = st.form_submit_button(label=f"{st.session_state.button_label}", on_click=submit_form)
                if form_button:
                    st.session_state.click_count += 1
                    webbrowser.open_new_tab(url)
                    
                print(st.session_state.click_count)
            
    
# --- EMAIL SUBSCRIPTION
        subscription()
        
    
# --- ADVERTISEMENT
with col2:
    st.header('Links')
    st_lottie("https://lottie.host/8a1ba2d6-ce90-4731-a8df-39aa09d15db2/3bgWuyOp4z.json")
    

# --- BUY ME A COFFEE
    button(username="serhansari", floating=True, width=221)
    
# --- FOOTER 
    footer()