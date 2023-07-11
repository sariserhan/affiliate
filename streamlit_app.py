import streamlit as st

from io import BytesIO
from base64 import b64decode

from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.keyboard_url import keyboard_to_url
from streamlit_extras.mention import mention

from frontend.footer import footer
from frontend.sidebar import sidebar
from frontend.subscription import subscription
from backend.data.item import Item


# --- NAVIGATION BAR
st.set_page_config(
    layout='wide',
    page_title="Multipage App",
    page_icon=":books:"
)

st.title('BestBuybyAI')
# load_key_css()

# --- CATALOG SIDE BAR
selected = sidebar()

# --- POST LIST
col1, col2 = st.columns([0.7,0.3], gap="small")
with col1:
    with st.container():
    
        st.header(selected)

        # --- ITEM LIST
        items = Item().get_record_by_catalog(catalog=selected)
        for item in items:
            st.subheader(item['name'])
            
            # --- ADD keyboard to URL
            key = item['name'][0]
            # keyboard_to_url(key=key, url=item['link'])        
            # st.write(
            #    f"""Now hit {key("S", False)} on your keyboard...!""",
            #     unsafe_allow_html=True
            # )
        
            # IMAGE
            image_data = item['image_data']
            image = BytesIO(b64decode(image_data))
            st.image(image=image, caption=item['name'])
            
            # Item Description
            st.markdown(item['description'])
            
            # ADD mentions to the text         
            mention(
                label=item['name'],
                icon="streamlit",  # Some icons are available... like Streamlit!
                url=item['link'],
            )
            # st.write(f"check out this [link]({item['link']})")
            
            st.divider()
    
    # --- EMAIL SUBSCRIPTION
    subscription()
        
    
# --- ADVERTISEMENT
with col2:
    st.header('Commercial')
    st.markdown('asdasdasdasdasdasdsadasdasdasdasdasdasdsadasdasdasdasdasdasdsadasdasdasdasdasdasdsadasdasdasdasdasdasdsadasdasdasdasdasdasdsadasdasdasdasdasdasdsad')

# --- BUY ME A COFFEE
    button(username="serhansari", floating=True, width=221)
    
# --- FOOTER 
    footer()