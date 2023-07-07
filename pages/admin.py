import streamlit as st

from backend.data.item import Item

st.set_page_config(layout='centered')

st.header('Create New Item')

with st.container():
    name = st.text_input(label='Item Name', key='name', placeholder='Name', label_visibility='collapsed')
    description = st.text_area(label='Item Description', height=50, key='description', placeholder='Description',label_visibility='collapsed')
    image_data = st.text_input(label='Item Image Path or Byte', key='image_data', placeholder='Image Path or Byte',label_visibility='collapsed')
    affiliate_link = st.text_input(label='Item Affiliate Link', key='affiliate_link', placeholder='Affiliate Link',label_visibility='collapsed')
    catalog_name = st.text_input(label='Catalog Name', key='catalog_name', placeholder='Catalog Name', label_visibility='collapsed')
    clicked = st.number_input(label='Num of clicked to start', value=0, key='clicked')
    button = st.button(label='Submit')
    
    if button:
        st.write(name)
        item = Item()
        item.create_item(name=name, description=description, image_path_or_byte=image_data, link=affiliate_link, catalog_name=catalog_name, clicked=int(clicked))
