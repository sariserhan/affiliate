import logging
import random

import streamlit as st
from streamlit_extras.mention import mention

from backend.data.item import Item
from frontend.ask_ai import ask_ai_page
from frontend.utils.utils import get_image, open_page


def all_and_best_items(is_best_pick: bool = False, is_most_viewed: bool = False):
    _, col2, _ = st.columns([1, 2.5, 1])
    items = Item().fetch_records()
    if not is_most_viewed:
        if is_best_pick:
            temp_catalog_list = []
        else:
            random.shuffle(items)

        for item in items:
            logging.info(" -------> %s is processing...", item['name'])
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
                    st.write(
                        f"<h2 class='element'><a href={url}>{name}<br>({item['catalog']})</a></h2>", unsafe_allow_html=True)
                    st.write('---')

                    # --- ADD mentions to the text
                    inline_mention = mention(
                        label=f"**_Visit Site:_ :green[{name}]** :pushpin:",
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
                    counter_text.markdown(
                        f'**:green[{viewed}]** times visited :eyes:', unsafe_allow_html=True)
                    if is_best_pick:
                        ask_ai_page(name=name)
                    if st.form_submit_button(label=':heavy_dollar_sign: Check Price', on_click=open_page, args=(url,)):
                        Item().update_record(key=item_key,
                                             updates={'clicked': clicked+1})

                        # Update the counter text on the page
                        counter_text.markdown(
                            f"**:red[{viewed+1}]** times visited :white_check_mark:")
                        logging.info(
                            "%s is clicked by %s --> %s", name, st.experimental_user.email, url)
    else:
        items_category_dict = {}
        for item in items:
            viewed = item['clicked'] + item['f_clicked']
            if item['catalog'] not in items_category_dict:
                items_category_dict[item['catalog']] = [item['name'], viewed]
            elif viewed > items_category_dict[item['catalog']][1]:
                items_category_dict[item['catalog']] = [item['name'], viewed]

        most_viewed_items_name = [value[0]
                                  for _, value in items_category_dict.items()]

        for item in items:
            if item['name'] in most_viewed_items_name:
                form_name = item['name'] + '_most_viewed'

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
                        st.write(
                            f"<h2 class='element'><a href={url}>{name}<br>({item['catalog']})</a></h2>", unsafe_allow_html=True)
                        st.write('---')

                        # --- ADD mentions to the text
                        inline_mention = mention(
                            label=f"**_Visit Site:_ :green[{name}]** :pushpin:",
                            icon=":arrow_right:",
                            url=url,
                            write=False
                        )
                        st.image(image=image, caption=name,
                                 use_column_width=True)
                        st.markdown(description)

                        # --- URL AND KEYBOARD TO URL
                        st.write(
                            inline_mention, unsafe_allow_html=True
                        )
                        # CHECK PRICE BUTTON
                        counter_text = st.empty()
                        counter_text.markdown(
                            f'**:green[{viewed}]** times visited :fire:', unsafe_allow_html=True)
                        ask_ai_page(name=name)
                        if st.form_submit_button(label=':heavy_dollar_sign: Check Price', on_click=open_page, args=(url,)):
                            Item().update_record(key=item_key,
                                                 updates={'clicked': clicked+1})

                            # Update the counter text on the page
                            counter_text.markdown(
                                f"**:red[{viewed+1}]** times visited :white_check_mark:")
                            logging.info(
                                "%s is clicked by %s --> %s", name, st.experimental_user.email, url)
