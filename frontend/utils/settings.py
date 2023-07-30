import streamlit as st

from pathlib import Path

theme_switch = None
def enable_theme_selection_for_user():
    global theme_switch    
    if st.checkbox("Enable Theme Switch"):
        theme_switch = True
        return theme_switch
    theme_switch = False
    return theme_switch


def set_default_theme():
    current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    config_toml_file = current_dir / '.streamlit' / 'config.toml'
    
    if st.checkbox("Default Dark Theme", key="dark_theme"):
        config_toml = open(config_toml_file, 'w')
        config_toml.write('[theme]\nbase="dark"')
        config_toml.close()
    else:
        config_toml = open(config_toml_file, 'w')
        config_toml.write('[theme]\nbase="light"')
        config_toml.close()
        
