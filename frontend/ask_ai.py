import logging
import os
import time

import openai
import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.keyboard_text import key
from streamlit_extras.keyboard_url import keyboard_to_url
from streamlit_extras.mention import mention
from streamlit_extras.no_default_selectbox import selectbox

from backend.data.item import Item
from frontend.utils.utils import ask_ai, get_image, get_progress_bar, open_page

logging.basicConfig(level=logging.DEBUG)

openai.organization = "org-KAv10qRlhbdtXmwkdkuET5TP"
openai.api_key = os.getenv("OPENAI_API_KEY")
models = openai.Model.list()

load_dotenv()


def ask_ai_page(name: str = None):
    if name:
        if st.form_submit_button('Not Sure :question: Ask AI :speech_balloon:'):
            logging.info(models.data[0].id)
            my_bar = st.empty()
            progress_text = "Searching... Please wait..."
            my_bar.progress(0, text=progress_text)

            answer = ask_ai(message_to_ask=os.getenv(
                'AI_ASK').format(name)).split('\n')
            get_progress_bar(my_bar, progress_text)

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
        items_name_list = [val for item in all_items for key,
                           val in item.items() if key == 'name']  # ✅
        if selected_item := selectbox(
            label='Choose Item from the drop-down menu to know more about with AI',
            options=items_name_list,
            key='items',
        ):
            key_right = selected_item.replace(' ', '_')
            item = Item().get_record(key_right)
            item_image = get_image(item['image_name'], item['catalog'])
            with st.form('ai'):
                # --- ADD keyboard to URL
                keyboard_to_url(key=str(1), url=item['affiliate_link'])

                inline_mention_right = mention(
                    label=f"**_Visit Site:_ :green[{item['name']}]** :pushpin:",
                    icon=":arrow_right:",
                    url=item['affiliate_link'],
                    write=False
                )

                st.markdown(
                    f"<h2 class='element'><a href={item['affiliate_link']}>{item['name']}</a></h2>", unsafe_allow_html=True)
                st.write('---')
                st.image(item_image, use_column_width=True,
                         caption=item['description'])

                # --- URL AND KEYBOARD TO URL
                st.write(
                    f'{inline_mention_right} or hit {key(":one:", False)} on your keyboard :keyboard:', unsafe_allow_html=True
                )

                st.write('---')

                # CHECK PRICE BUTTON
                counter_text = st.empty()
                counter_text.markdown(
                    f'**:green[{item["clicked"]+item["f_clicked"]}]** times visited :boom:', unsafe_allow_html=True)

                if check_price_button := st.form_submit_button(
                    ":heavy_dollar_sign: Check Price",
                    on_click=open_page,
                    args=(item['affiliate_link'],),
                ):
                    Item().update_record(key=item['key'], updates={
                        'clicked': item['clicked']+1})

                    # Update the counter text on the page
                    counter_text.markdown(
                        f'**:red[{item["clicked"]+item["f_clicked"]+1}]** times visited :white_check_mark:')
                    logging.info(
                        f"{item['name']} is clicked by {st.experimental_user.email} --> {item['affiliate_link']}")

                questions_list = [
                    f'Should I buy this product:{selected_item}',
                    f'Should I not this buy product:{selected_item}',
                    f'What are the main features and specifications of this product:{selected_item}?',
                    f'What are my alternatives rather than this product:{selected_item}',
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
                selected_question = selectbox(
                    "Choose pre-selected question from the drop-down menu to ask AI", options=questions_list)

                if st.form_submit_button("Ask AI :speech_balloon:") and selected_question:
                    # AI
                    logging.info(models.data[0].id)
                    my_bar = st.empty()
                    progress_text = "Searching with AI... Please wait..."
                    my_bar.progress(0, text=progress_text)

                    answer = ask_ai(message_to_ask=selected_question)
                    get_progress_bar(my_bar, progress_text)
                    logging.info(f'--------> AI ANSWER:{answer}')
                    st.write(answer)
