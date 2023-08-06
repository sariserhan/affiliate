import logging
import os

import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.keyboard_text import key
from streamlit_extras.keyboard_url import keyboard_to_url
from streamlit_extras.mention import mention
from streamlit_extras.no_default_selectbox import selectbox

from backend.data.catalog import Catalog
from backend.data.item import Item
from frontend.utils.utils import ask_ai, get_image, get_progress_bar, open_page

logging.basicConfig(level=logging.DEBUG)

load_dotenv()


def compare_items(compare: bool = False):
    catalog_list = [catalog['name'] for catalog in Catalog().fetch_records()]
    selected_catalog = selectbox(label="Choose Category", options=catalog_list)
    items_list = [item['name']
                  for item in Item().get_record_by_catalog(selected_catalog)]
    compare_form_container = st.empty()
    col1, col2 = st.columns(2)

    if selected_catalog:
        with col1:
            selected_item_left = selectbox(
                label='item left', options=items_list, key='item_left', label_visibility='collapsed')
            if selected_item_left:
                with st.form('left'):
                    key_left = selected_item_left.replace(' ', '_')
                    item_left = Item().get_record(key_left)
                    item_left_image = get_image(
                        item_left['image_name'], selected_catalog)

                    # --- ADD keyboard to URL
                    keyboard_to_url(
                        key=str(1), url=item_left['affiliate_link'])

                    inline_mention_left = mention(
                        label=f"**_Visit Site:_ :green[{item_left['name']}]** :pushpin:",
                        icon=":arrow_right:",
                        url=item_left['affiliate_link'],
                        write=False
                    )

                    st.markdown(
                        f"<h2 class='element'><a href={item_left['affiliate_link']}>{item_left['name']}</a></h2>", unsafe_allow_html=True)
                    st.write('---')
                    st.image(item_left_image, use_column_width=True,
                             caption=item_left['description'])

                    # --- URL AND KEYBOARD TO URL
                    st.write(
                        f'{inline_mention_left} or hit {key(":one:", False)} on your keyboard :keyboard:', unsafe_allow_html=True
                    )

                    if not compare:
                        st.write('---')

                        if '\n\n' in item_left['pros']:
                            pros_left = item_left['pros'].replace(
                                '\n\n', '\n').split('\n')
                        else:
                            pros_left = item_left['pros'].split('. ')

                        if '\n\n' in item_left['cons']:
                            cons_left = item_left['cons'].replace(
                                '\n\n', '\n').split('\n')
                        else:
                            cons_left = item_left['cons'].split('. ')

                        for pros in pros_left:
                            if pros != '':
                                st.write(
                                    f':ballot_box_with_check: :blue[{pros[:pros.find(":") + 1]}]{pros[pros.find(":") + 1:]}'
                                )

                        st.write('---')
                        for cons in cons_left:
                            if cons != '':
                                st.write(
                                    f':warning: :orange[{cons[:cons.find(":") + 1]}]{cons[cons.find(":") + 1:]}'
                                )

                    st.write('---')
                    button_row_1, _, button_row_3, _, _ = st.columns(
                        [1, 0.1, 1, 0.1, 0.1])
                    with button_row_3:
                        button = st.form_submit_button(
                            ":heavy_dollar_sign: Check Price", on_click=open_page, args=(item_left['affiliate_link'],))
                    with button_row_1:
                        counter_text = st.empty()
                        counter_text.markdown(
                            f'**:green[{item_left["clicked"]+item_left["f_clicked"]}]** times visited :eyes:', unsafe_allow_html=True)

                        if button:
                            Item().update_record(key=item_left['key'], updates={
                                'clicked': item_left['clicked']+1})

                            # Update the counter text on the page
                            counter_text.markdown(
                                f'**:red[{item_left["clicked"]+item_left["f_clicked"]+1}]** times visited :white_check_mark:')
                            logging.info(
                                f"{item_left['name']} is clicked by {st.experimental_user.email} --> {item_left['affiliate_link']}")

        with col2:
            selected_item_right = selectbox(
                label='item right', options=items_list, key='item_right', label_visibility='collapsed')
            if selected_item_right:
                with st.form('right'):
                    key_right = selected_item_right.replace(' ', '_')
                    item_right = Item().get_record(key_right)
                    item_right_image = get_image(
                        item_right['image_name'], selected_catalog)

                    # --- ADD keyboard to URL
                    keyboard_to_url(
                        key=str(2), url=item_right['affiliate_link'])

                    inline_mention_right = mention(
                        label=f"**_Visit Site:_ :green[{item_right['name']}]** :pushpin:",
                        icon=":arrow_right:",
                        url=item_right['affiliate_link'],
                        write=False
                    )

                    st.markdown(
                        f"<h2 class='element'><a href={item_right['affiliate_link']}>{item_right['name']}</a></h2>", unsafe_allow_html=True)
                    st.write('---')
                    st.image(item_right_image, use_column_width=True,
                             caption=item_right['description'])

                    # --- URL AND KEYBOARD TO URL
                    st.write(
                        f'{inline_mention_right} or hit {key(":two:", False)} on your keyboard :keyboard:', unsafe_allow_html=True
                    )

                    if not compare:
                        st.divider()

                        if '\n\n' in item_right['pros']:
                            pros_right = item_right['pros'].replace(
                                '\n\n', '\n').split('\n')
                        else:
                            pros_right = item_right['pros'].split('. ')

                        if '\n\n' in item_right['cons']:
                            cons_right = item_right['cons'].replace(
                                '\n\n', '\n').split('\n')
                        else:
                            cons_right = item_right['cons'].split('. ')

                        for pros in pros_right:
                            if pros != '':
                                st.write(
                                    f':white_check_mark: :green[{pros[:pros.find(":") + 1]}]{pros[pros.find(":") + 1:]}'
                                )

                        st.divider()
                        for cons in cons_right:
                            if cons != '':
                                st.write(
                                    f':lightning: :red[{cons[:cons.find(":") + 1]}]{cons[cons.find(":") + 1:]}'
                                )

                    st.divider()
                    button_row_1, _, button_row_3, _, _ = st.columns(
                        [1, 0.1, 1, 0.1, 0.1])
                    with button_row_3:
                        button = st.form_submit_button(
                            ":heavy_dollar_sign: Check Price", on_click=open_page, args=(item_right['affiliate_link'],))

                    with button_row_1:
                        counter_text = st.empty()
                        counter_text.markdown(
                            f'**:green[{item_right["clicked"]+item_right["f_clicked"]}]** times visited :eyes:', unsafe_allow_html=True)

                        if button:
                            Item().update_record(key=item_right['key'], updates={
                                'clicked': item_right['clicked']+1})

                            # Update the counter text on the page
                            counter_text.markdown(
                                f'**:red[{item_right["clicked"]+item_right["f_clicked"]+1}]** times visited :white_check_mark:')
                            logging.info(
                                f"{item_right['name']} is clicked by {st.experimental_user.email} --> {item_right['affiliate_link']}")

        if compare and (selected_item_left and selected_item_right):
            with compare_form_container.form("Compare_with_AI"):
                if st.form_submit_button("Compare items with AI"):
                    if selected_item_right == selected_item_left:
                        st.warning(
                            "Please select different items to compare :exclamation:")
                    else:
                        progress_text = "Searching... Please wait..."
                        my_bar = st.empty()
                        my_bar.progress(0, text=progress_text)

                        answer = ask_ai(message_to_ask=os.getenv("AI_COMPARE").format(
                            item_left['name'], item_right['name']))
                        get_progress_bar(my_bar, progress_text)
                        logging.info(f'--------> AI ANSWER:{answer}')
                        st.write(answer)
