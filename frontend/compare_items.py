import os
import time
import openai

import logging
import streamlit as st

from dotenv import load_dotenv

from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.mention import mention
from streamlit_extras.keyboard_url import keyboard_to_url
from streamlit_extras.keyboard_text import key

from backend.data.catalog import Catalog
from backend.data.item import Item
from frontend.column_setup import get_image, open_page

logging.basicConfig(level=logging.DEBUG)

openai.organization = "org-KAv10qRlhbdtXmwkdkuET5TP"
openai.api_key = os.getenv("OPENAI_API_KEY")
models = openai.Model.list()

load_dotenv()
        
def compare_items(compare: bool = False):    
    catalog_list = [catalog['name'] for catalog in Catalog().fetch_records()]
    selected_catalog = selectbox(label="Choose Category", options=catalog_list)
    items_list = [item['name'] for item in Item().get_record_by_catalog(selected_catalog)]
    
    col1, col2 = st.columns(2)
    
    if selected_catalog:
        with col1:
            selected_item_left = selectbox(label='item left', options=items_list, key='item_left', label_visibility='collapsed')
            if selected_item_left:
                with st.form('left'):
                    key_left = selected_item_left.replace(' ','_')                                      
                    item_left = Item().get_record(key_left)                                                                    
                    item_left_image = get_image(item_left['image_name'], selected_catalog)
                    
                    # --- ADD keyboard to URL
                    keyboard_to_url(key=str(1), url=item_left['affiliate_link'])
                    
                    inline_mention_left = mention(
                        label=f"**_Visit Site:_ :green[{item_left['name']}]**",
                        icon=":arrow_right:",
                        url=item_left['affiliate_link'],
                        write=False
                    )
                    
                    st.markdown(f"<h2 class='element'><a href={item_left['affiliate_link']}>{item_left['name']}</a></h2>", unsafe_allow_html=True)
                    st.write('---')
                    st.image(item_left_image, use_column_width=True, caption=item_left['description'])
                    
                    # --- URL AND KEYBOARD TO URL            
                    st.write(
                        f'{inline_mention_left} or hit {key(":one:", False)} on your keyboard :exclamation:', unsafe_allow_html=True
                    )                        
                    
                    if not compare:
                        st.write('---')
                            
                        pros_left = item_left['pros'].split('.\n')
                        cons_left = item_left['cons'].split('.\n')
                        
                        for pros in pros_left:
                            if pros != '':
                                st.write(f':white_check_mark: {pros}')
                            
                        st.write('---')                                                        
                        for cons in cons_left:
                            if cons != '':
                                st.write(f':x: {cons}')                                                                                                 
                    
                    st.write('---')
                    button_row_1, _, button_row_3, _, _ = st.columns([1,0.1,1,0.1,0.1])
                    with button_row_3:
                        button = st.form_submit_button("Check Price", on_click=open_page, args=(item_left['affiliate_link'],))
                    with button_row_1:
                        counter_text = st.empty()
                        counter_text.markdown(f'**:green[{item_left["clicked"]+item_left["f_clicked"]}]** times visited :exclamation:', unsafe_allow_html=True)                                    
                    
                        if button:
                            Item().update_record(key=item_left['key'], updates={'clicked':item_left['clicked']+1})
                                
                            # Update the counter text on the page
                            counter_text.markdown(f'**:red[{item_left["clicked"]+item_left["f_clicked"]+1}]** times visited :white_check_mark:')                
                            logging.info(f"{item_left['name']} is clicked by {st.experimental_user.email} --> {item_left['affiliate_link']}")
                
        with col2:                
            selected_item_right = selectbox(label='item right', options=items_list, key='item_right', label_visibility='collapsed')
            if selected_item_right:
                with st.form('right'):
                    key_right = selected_item_right.replace(' ','_')                        
                    item_right= Item().get_record(key_right)
                    item_right_image = get_image(item_right['image_name'], selected_catalog)
                    
                    # --- ADD keyboard to URL
                    keyboard_to_url(key=str(2), url=item_left['affiliate_link'])
                    
                    inline_mention_right = mention(
                        label=f"**_Visit Site:_ :green[{item_right['name']}]**",
                        icon=":arrow_right:",
                        url=item_right['affiliate_link'],
                        write=False
                    )
                    
                    st.markdown(f"<h2 class='element'><a href={item_right['affiliate_link']}>{item_right['name']}</a></h2>", unsafe_allow_html=True)
                    st.write('---')
                    st.image(item_right_image, use_column_width=True, caption=item_right['description'])
                    
                    # --- URL AND KEYBOARD TO URL            
                    st.write(
                        f'{inline_mention_right} or hit {key(":two:", False)} on your keyboard :exclamation:', unsafe_allow_html=True
                    )
                    
                    if not compare:
                        st.write('---')                            
                        pros_right = item_right['pros'].split('.\n')
                        cons_right = item_right['cons'].split('.\n')
                        
                        for pros in pros_right:
                            if pros != '':
                                st.write(f':white_check_mark: {pros}')
                            
                        st.write('---')                                                        
                        for cons in cons_right:
                            if cons != '':
                                st.write(f':x: {cons}')                                            
                        
                    st.write('---')
                    button_row_1, _, button_row_3, _, _ = st.columns([1,0.1,1,0.1,0.1])
                    with button_row_3:
                        button = st.form_submit_button("Check Price", on_click=open_page, args=(item_right['affiliate_link'],))                        
                    
                    with button_row_1:
                        counter_text = st.empty()
                        counter_text.markdown(f'**:green[{item_right["clicked"]+item_right["f_clicked"]}]** times visited :exclamation:', unsafe_allow_html=True)                                    
                    
                        if button:
                            Item().update_record(key=item_right['key'], updates={'clicked':item_right['clicked']+1})
                                
                            # Update the counter text on the page
                            counter_text.markdown(f'**:red[{item_right["clicked"]+item_right["f_clicked"]+1}]** times visited :white_check_mark:')                
                            logging.info(f"{item_right['name']} is clicked by {st.experimental_user.email} --> {item_right['affiliate_link']}")
        
        if compare:
            with st.form("Compare_with_AI"):
                if st.form_submit_button("Compare items with AI"):
                    if selected_item_left and selected_item_right:
                        if selected_item_right == selected_item_left:
                            st.warning("Please select different items to compare with AI")
                        else:
                            logging.info(models.data[0].id)
                            progress_text = "Searching... Please wait..."
                            my_bar = st.empty()
                            my_bar.progress(0, text=progress_text)
                            
                            # create a chat completion
                            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                                                        messages=[{"role": "user", 
                                                                                    "content": os.getenv("AI_COMPARE").format(item_left['name'], item_right['name'])
                                                                                    }])

                            for percent_complete in range(100):
                                time.sleep(0.01)
                                my_bar.progress(percent_complete + 1, text=progress_text)
                            my_bar.progress(100, text='Completed')
                            time.sleep(1)
                            my_bar.empty()
                            answer = chat_completion.choices[0].message.content
                            logging.info(f'--------> AI ANSWER:{answer}')
                            st.write(answer)
 
                
def item_pick_ask_ai():
    all_items = Item().fetch_records()
    items_name_list = [val for item in all_items for key,val in item.items() if key == 'name'] # ✅
    selected_item = selectbox(label='Choose Item to ask AI', options=items_name_list, key='items')
    if selected_item:
        key_right = selected_item.replace(' ','_')                        
        item= Item().get_record(key_right)
        item_image = get_image(item['image_name'], item['catalog'])
        with st.form('ai'):
            # --- ADD keyboard to URL
            keyboard_to_url(key=str(1), url=item['affiliate_link'])
            
            inline_mention_right = mention(
                label=f"**_Visit Site:_ :green[{item['name']}]**",
                icon=":arrow_right:",
                url=item['affiliate_link'],
                write=False
            )
            
            st.markdown(f"<h2 class='element'><a href={item['affiliate_link']}>{item['name']}</a></h2>", unsafe_allow_html=True)
            st.write('---')
            st.image(item_image, use_column_width=True, caption=item['description'])
            
            # --- URL AND KEYBOARD TO URL            
            st.write(
                f'{inline_mention_right} or hit {key(":one:", False)} on your keyboard :exclamation:', unsafe_allow_html=True
            )
            
            st.write('---')                         

            # CHECK PRICE BUTTON
            counter_text = st.empty()
            counter_text.markdown(f'**:green[{item["clicked"]+item["f_clicked"]}]** times visited :exclamation:', unsafe_allow_html=True) 
            
            buy_button = st.form_submit_button("Check Price", on_click=open_page, args=(item['affiliate_link'],))   
            
            # AI 
            logging.info(models.data[0].id)
            my_bar = st.empty()
            progress_text = "Searching with AI... Please wait..."
            my_bar.progress(0, text=progress_text)
            
            # create a chat completion
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                                        messages=[{"role": "user", 
                                                                    "content": os.getenv('AI_ASK').format(item['name'])
                                                                    }])

            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            my_bar.progress(100, text='Completed')
            time.sleep(1)
            my_bar.empty()
            
            answer = chat_completion.choices[0].message.content.split('\n')
            
            logging.info(f'--------> AI ANSWER:{answer}')
            
            buy_paragraph, dont_buy_paragraph = answer[0], answer[2]
            
            logging.info(f'--------> AI ANSWER BUY:{buy_paragraph}')
            logging.info(f'--------> AI ANSWER DONT BUY:{dont_buy_paragraph}')
            
            st.subheader("You should consider because ✅")
            st.write(buy_paragraph)
            st.write('---')
            st.subheader("You shouldn't because ❌")
            st.write(dont_buy_paragraph)
            
            if buy_button:
                Item().update_record(key=item['key'], updates={'clicked':item['clicked']+1})
                    
                # Update the counter text on the page
                counter_text.markdown(f'**:red[{item["clicked"]+item["f_clicked"]+1}]** times visited :white_check_mark:')                
                logging.info(f"{item['name']} is clicked by {st.experimental_user.email} --> {item['affiliate_link']}")
                