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

def number_to_words(number):
    words = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]
    return " ".join(words[int(i)] for i in str(number))

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
                mention_clicked = mention(
                    label=name,
                    icon="streamlit",  # Some icons are available... like Streamlit!
                    url=item['affiliate_link'],
                )
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
                
                # COUNTER
                if name not in st.session_state:                    
                    st.session_state.name = item['clicked'] + item['f_clicked']
                    
                counter_text = st.empty()
                counter_text.write(f"The counter value is: {st.session_state.name}")
                
                # --- ADD keyboard to URL
                number = number_to_words(item_index)
                keyboard_to_url(key=str(item_index), url=url)
                
                def link_callback():
                    st.session_state.name += 1
                    
                link = st.markdown(
                    f"[Visit Site]({url}) or hit {key(number, False)} on your keyboard...!",
                    # f"""[Visit Site]({url}) or hit {key(number, False)} on your keyboard...!""",
                    unsafe_allow_html=True
                )
                

                    
                # CHECK PRICE BUTTON
                form_button = st.form_submit_button(label=f"Check Price")
                
                if form_button:
                    print("YESSSS")
                    st.session_state.name += 1
                    
                    # Update the counter text on the page
                    counter_text.write(f"The counter value is: {st.session_state.name}")
                    webbrowser.open_new_tab(url)
                    

            
    
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