import logging

import streamlit as st
from streamlit_extras.keyboard_text import key
from streamlit_extras.keyboard_url import keyboard_to_url
from streamlit_extras.mention import mention

from backend.data.item import Item
from frontend.ask_ai import ask_ai_page
from frontend.utils.utils import get_image, open_page

logging.basicConfig(level=logging.DEBUG)


def number_to_words(number):
    words = [":one:", ":two:", ":three:", ":four:", ":five:",
             ":six:", ":seven:", ":eight:", ":nine:", ":zero:"]
    return " ".join(words[int(i)] for i in str(number))


def set_form(items: dict, col_name: str, selected_catalog: str):
    for item_index, item in enumerate(items):
        item_key = item["key"]
        name = item["name"]
        url = item['affiliate_link']
        description = item['description']
        image_name = item['image_name']
        clicked = item["clicked"]
        f_clicked = item["f_clicked"]
        viewed = clicked + f_clicked

        with st.form(f'{name}_{col_name}', clear_on_submit=False):

            # --- SUB-HEADER
            st.markdown(
                f"<h2 class='element'><a href={url}>{name}</a></h2>", unsafe_allow_html=True)
            st.write('---')

            # --- ADD keyboard to URL
            number = number_to_words(item_index)
            keyboard_to_url(key=str(item_index+1), url=url)

            # --- ADD mentions to the text
            inline_mention = mention(
                label=f"**_Visit Site:_ :green[{name}]** :pushpin:",
                icon=":arrow_right:",
                url=url,
                write=False
            )

            # -------------------------------------
            # THIS IS FOR AD
            # --- ADD mentions to the text for ad..
            # inline_ad_mention = mention(
            #     label="but don't click :red[THIS]",
            #     icon=':exclamation:',
            #     url="https://www.google.com",
            #     write=False
            # )
            # NOTE: Add ad link here
            # keyboard_to_url(key="a", url="https://www.google.com")
            # st.write(
            #     f'{inline_mention} or hit {key(number, False)} on your keyboard {inline_ad_mention} nor hit {key(":a:", False)} :exclamation:',
            #     unsafe_allow_html=True,
            # )
            # -------------------------------------

            # --- IMAGE
            try:
                image = get_image(image_name, selected_catalog)
                st.image(image=image, caption=name, use_column_width=True)
            except Exception as e:
                logging.error(f'Error for item: {name} ---> {e}')

            # --- DESCRIPTION
            st.markdown(description)

            # --- URL AND KEYBOARD TO URL
            st.write(
                f'{inline_mention} or hit {key(number, False)} on your keyboard :keyboard:', unsafe_allow_html=True
            )

            # CHECK PRICE BUTTON
            counter_text = st.empty()
            counter_text.markdown(
                f'**:green[{viewed}]** times visited :eyes:', unsafe_allow_html=True)
            ask_ai_page(name=name)

            if st.form_submit_button(label=':heavy_dollar_sign: Check Price', on_click=open_page, args=(url,)):
                Item().update_record(key=item_key,
                                     updates={'clicked': clicked+1})

                # Update the counter text on the page
                counter_text.markdown(
                    f"**:red[{viewed+1}]** times visited :white_check_mark:")
                logging.info(
                    f"{name} is clicked by {st.experimental_user.email} --> {url}")
