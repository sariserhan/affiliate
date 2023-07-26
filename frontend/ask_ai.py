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

from backend.data.item import Item
from frontend.utils.utils import get_image, open_page

logging.basicConfig(level=logging.DEBUG)

openai.organization = "org-KAv10qRlhbdtXmwkdkuET5TP"
openai.api_key = os.getenv("OPENAI_API_KEY")
models = openai.Model.list()

load_dotenv()

def ask_ai(name: str = None):
    if name:
        ask_ai_button = st.form_submit_button('Not Sure? Ask AI')
                
        if ask_ai_button:
            logging.info(models.data[0].id)
            my_bar = st.empty()
            progress_text = "Searching... Please wait..."
            my_bar.progress(0, text=progress_text)
            # create a chat completion
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                                        messages=[{"role": "user", 
                                                                    "content": os.getenv('AI_ASK').format(name)
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
        
        
    else:
        all_items = Item().fetch_records()
        items_name_list = [val for item in all_items for key,val in item.items() if key == 'name'] # ✅
        selected_item = selectbox(label='Choose Item from the drop-down menu to know more about with AI', options=items_name_list, key='items')
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
                questions_list = [
                    f'Should I buy this product:{selected_item}',
                    f'Should I not this buy product:{selected_item}',
                    f'What are the main features and specifications of this product:{selected_item}?',
                    f'What are my alternatives rather than this product:{selected_item}',
                    f'What is the customer ratings for this product:{selected_item}',
                    f'Show me the customer reviews for this product:{selected_item}',
                    f'What is the warranty or guarantee period of this product:{selected_item}?',
                    f'Would you buy this product:{selected_item} or pass if you were me?',
                    f'Tell me the best part of this product:{selected_item}',
                    f'Tell me the worst part of this product:{selected_item}',
                    f'Tell me everything about this product:{selected_item}',
                    f'What problems I might have after I purchase this product:{selected_item}',
                    f'Do you think is this product:{selected_item} a good gift?',
                    f'Are there any compatibility issues with other devices or systems for this product:{selected_item}?',            
                    f'If you were a salesman, tell me something about this product:{selected_item} that I should not know'
                ]
                selected_question = selectbox("Choose pre-selected question from the drop-down menu to ask AI", options=questions_list)
                
                if st.form_submit_button("Ask AI"):
                    if selected_question:
                        # AI 
                        logging.info(models.data[0].id)
                        my_bar = st.empty()
                        progress_text = "Searching with AI... Please wait..."
                        my_bar.progress(0, text=progress_text)
                        
                        # create a chat completion
                        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                                                    messages=[{"role": "user", "content": selected_question}])

                        for percent_complete in range(100):
                            time.sleep(0.01)
                            my_bar.progress(percent_complete + 1, text=progress_text)
                        my_bar.progress(100, text='Completed')
                        time.sleep(1)
                        my_bar.empty()
                        
                        answer = chat_completion.choices[0].message.content
                        logging.info(f'--------> AI ANSWER:{answer}')
                        st.write(answer)        
                        
                        if buy_button:
                            Item().update_record(key=item['key'], updates={'clicked':item['clicked']+1})
                                
                            # Update the counter text on the page
                            counter_text.markdown(f'**:red[{item["clicked"]+item["f_clicked"]+1}]** times visited :white_check_mark:')                
                            logging.info(f"{item['name']} is clicked by {st.experimental_user.email} --> {item['affiliate_link']}")
                            