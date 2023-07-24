import random
import logging
import streamlit as st

from streamlit_extras.mention import mention
from backend.data.item import Item
from frontend.column_setup import get_image, open_page

logging.basicConfig(level=logging.DEBUG)

def all_and_best_items(is_best_pick: bool = False):
    col1, col2, col3 = st.columns([1,2.5,1])
    items = Item().fetch_records()
    
    if not is_best_pick:
        random.shuffle(items)
    else:
        temp_catalog_list = []
        
    for item in items:
        logging.info(f"{item['name']} is processing...")
        if is_best_pick:
            form_name = item['name']
            if item['catalog'] in temp_catalog_list:
                continue
            temp_catalog_list.append(item['catalog'])
        else:
            form_name = item['name'] + '_best_pick'
                
        image = get_image(item['image_name'], item['catalog'])
        item_key = item["key"]
        name = item["name"]
        url = item['affiliate_link']
        description = item['description']
        clicked = item["clicked"]
        f_clicked = item["f_clicked"]
        viewed = clicked + f_clicked
        
        with col2:
            with st.form(form_name):
                st.write(f"<h2 class='element'><a href={url}>{name}<br>({item['catalog']})</a></h2>", unsafe_allow_html=True)
                st.write('---')
                
                # --- ADD mentions to the text         
                inline_mention = mention(
                    label=f"**_Visit Site:_ :green[{name}]**",
                    icon=":arrow_right:",
                    url=url,
                    write=False
                )
                st.image(image=image, caption=name, use_column_width=True)
                st.markdown(description)
                
                # --- URL AND KEYBOARD TO URL            
                st.write(
                    inline_mention, unsafe_allow_html=True
                )
                # CHECK PRICE BUTTON
                counter_text = st.empty()
                
                form_button = st.form_submit_button(label='Check Price', on_click=open_page, args=(url,))
                
                counter_text.markdown(f'**:green[{viewed}]** times visited :exclamation:', unsafe_allow_html=True)
                
                if form_button:
                    Item().update_record(key=item_key, updates={'clicked':clicked+1})
                                    
                    # Update the counter text on the page
                    counter_text.markdown(f"**:red[{viewed+1}]** times visited :white_check_mark:")
                    logging.info(f"{name} is clicked by {st.experimental_user.email} --> {url}")