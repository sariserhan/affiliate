from pathlib import Path

import streamlit as st

disable_theme_switch = False


def disable_theme_selection_for_user():
    global disable_theme_switch
    if st.checkbox("Disable Theme Switch"):
        disable_theme_switch = True

    return disable_theme_switch


def set_default_theme():
    current_dir = Path(
        __file__).parent if "__file__" in locals() else Path.cwd()
    config_toml_file = current_dir / '.streamlit' / 'config.toml'

    if st.checkbox("Default Dark Theme", key="dark_theme"):
        config_toml = open(config_toml_file, 'w')
        config_toml.write('[theme]\nbase="dark"')
    else:
        config_toml = open(config_toml_file, 'w')
        config_toml.write('[theme]\nbase="light"')

    config_toml.close()


def get_db_backup():
    if st.checkbox('Backup --> Catalog_DB'):
        from backend.data.catalog import Catalog
        try:
            Catalog().migrate_database('catalog_db_backup')
            st.info('Backup Complete:catalog_db_backup')
        except Exception as e:
            st.error('Error attempting :to backup:catalog_db_backup')

    if st.checkbox('Backup --> Category_DB'):
        from backend.data.category import Category
        try:
            Category().migrate_database('category_db_backup')
            st.info('Backup Complete:category_db_backup')
        except Exception as e:
            st.error('Error attempting :to backup:category_db_backup')

    if st.checkbox('Backup --> Subscription_DB'):
        from backend.data.subscribe import Subscription
        try:
            Subscription().migrate_database('subscription_db_backup')
            st.info('Backup Complete:subscription_db_backup')
        except Exception as e:
            st.error('Error attempting :to backup:subscription_db_backup')

    if st.checkbox('Backup --> Items_DB2'):
        from backend.data.item import Item
        try:
            Item().migrate_database('items_db2_backup')
            st.info('Backup Complete:items_db2_backup')
        except Exception as e:
            st.error('Error attempting :to backup:items_db2_backup')

    if st.checkbox('Backup --> Affiliate_Partner_DB'):
        from backend.data.affiliate_partner import Affiliate_Partner
        try:
            Affiliate_Partner().migrate_database('affiliate_partner_db_backup')
            st.info('Backup Complete:affiliate_partner_db_backup')
        except Exception as e:
            st.error('Error attempting :to backup:affiliate_partner_db_backup')

    if st.checkbox('Backup --> Admin_DB'):
        from backend.data.admin import Admin
        try:
            Admin().migrate_database('admin_db_backup')
            st.info('Backup Complete:admin_db_backup')
        except Exception as e:
            st.error('Error attempting :to backup:admin_db_backup')

    # TODO: Make Backup for Images
    if st.checkbox('Backup --> Images_DB'):
        pass
