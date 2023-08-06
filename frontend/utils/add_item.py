import logging
import random
import re
import time

import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox

from backend.data.affiliate_partner import Affiliate_Partner
from frontend.utils.utils import ask_ai, get_progress_bar

logging.basicConfig(level=logging.DEBUG)


# --- ADD ITEM
def add_item(item_obj, catalog_list, category_list):
    f_clicked_toggle = None

    try:
        from streamlit_toggle import st_toggle_switch

        # TOGGLE SWITCH FOR f_clicked
        f_clicked_toggle = st_toggle_switch(
            label="Enable f-clicked?",
            key="switch_1",
            default_value=False,
            label_after=False,
            inactive_color="#D3D3D3",  # optional
            active_color="#11567f",  # optional
            track_color="#29B5E8",  # optional
        )
    except Exception:
        logging.warning('Toggle Switch in not available')

    catalog_list.append("Add New Catalog")
    category_list.append("Add New Category")

    # GET AFFILIATE PARTNER FROM DB
    affiliate_partner_list = []
    affiliate_partners = Affiliate_Partner().fetch_records()
    for affiliate_partner in affiliate_partners:
        affiliate_partner_list.append(affiliate_partner['key'])

    affiliate_partner_list.append("Add New Partner")

    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

    name = st.text_input(label='Item Name', key='item_name',
                         placeholder='Name', label_visibility='collapsed')

    if regex.search(name) != None:
        st.warning(
            f"Special characters are not allowed in the name section: {name}")

    desc_button = False
# ------------------------------------
    desc_button_container = st.empty()
    if name:
        desc_button = desc_button_container.button("Get Description!")
    description = st.text_area(label='Item Description', height=200, key='description',
                               placeholder='Description', label_visibility='collapsed', disabled=False)
    desc_container = st.empty()
    if desc_button and name:
        my_bar_desc = st.progress(0, text="Searching Description...")

        answer = ask_ai(
            message_to_ask=f'Describe this item in one paragraph:{name}')
        get_progress_bar(my_bar_desc, progress_text="Searching Description...")
        desc_container.write(answer)

    pros_button_container = st.empty()
    pros_button = pros_button_container.button("Get Pros!") if name else False
    pros = st.text_area(label='Pros', height=300, key='pros',
                        placeholder='Pros', label_visibility='collapsed', disabled=False)
    pros_container = st.empty()
    if pros_button and name:
        my_bar_pros = st.progress(0, text="Searching Pros...")

        answer = ask_ai(
            message_to_ask=f'What are the pros of this item:{name}')
        get_progress_bar(my_bar_pros, progress_text="Searching Pros...")
        pros_container.write(answer)

    cons_button_container = st.empty()
    cons_button = cons_button_container.button("Get Cons!") if name else False
    cons = st.text_area(label='Cons', height=300, key='cons',
                        placeholder='Cons', label_visibility='collapsed', disabled=False)
    cons_container = st.empty()
    if cons_button and name:
        my_bar_cons = st.progress(0, text="Searching Cons...")

        answer = ask_ai(
            message_to_ask=f'What are the cons of this item:{name}')
        get_progress_bar(my_bar_cons, progress_text="Searching Cons...")
        cons_container.write(answer)
# ------------------------------------
    affiliate_link = st.text_input(label='Item Affiliate Link', key='affiliate_link',
                                   placeholder='Affiliate Link', label_visibility='collapsed')

    selected_categories = st.multiselect(
        label='Choose Category or Add New', options=category_list[:])
    if "Add New Category" in selected_categories:
        selected_categories.append(st.text_input(
            label='Add Category Name', key='categories', placeholder='Category Name', label_visibility='collapsed'))
        selected_categories.remove('Add New Category')

    catalog_name = selectbox(
        label='Choose Catalog or Add New', options=catalog_list[:])
    if catalog_name == "Add New Catalog":
        catalog_name = st.text_input(label='Add Catalog Name', key='catalog_name',
                                     placeholder='Catalog Name', label_visibility='collapsed')

    affiliate_partner = selectbox(
        label='Choose Affiliate Partner or Add New', options=affiliate_partner_list)
    if affiliate_partner == "Add New Partner":
        affiliate_partner = st.text_input(
            label='Add Partner Name', key='partner_name', placeholder='Partner Name', label_visibility='collapsed')

    if f_clicked_toggle:
        random_num = random.randint(1000, 5000)
        f_clicked_val = st.number_input(
            label='Num of f_clicked to start', value=random_num, key='f_clicked')

    uploaded_file = st.file_uploader("Choose a file")
    st.write('---')

    disable_button = True
    add_button_container = st.empty()

    if all([uploaded_file, name, description, affiliate_link, catalog_name, affiliate_partner, pros, cons]):
        image_val = uploaded_file.getvalue()
        image_name = uploaded_file.name
        disable_button = False

        if add_button_container.button(label='Add a New Item', disabled=disable_button):
            progress_text = "Submitting... Please wait..."
            my_bar = st.progress(0, text=progress_text)

            try:
                item_obj.create_item(
                    name=name,
                    description=description,
                    image_path=image_val,
                    image_name=image_name,
                    affiliate_link=affiliate_link,
                    affiliate_partner=affiliate_partner,
                    categories=selected_categories,
                    catalog_names=[catalog_name],
                    pros=pros,
                    cons=cons,
                    f_clicked=int(f_clicked_val) if f_clicked_toggle else 0
                )

                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)

                st.success(f'Item added into DB: {name}')
            except Exception as e:
                st.error("Something went wrong!")
                logging.error(e)
            finally:
                add_button_container.empty()
