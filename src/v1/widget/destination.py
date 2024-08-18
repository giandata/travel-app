import streamlit as st
from lists import countries


def country_selection():
    if "selected_countries" not in st.session_state:
        st.session_state["selected_countries"] = None

    selected_countries = st.multiselect(
        label="Countries to visit",
        options=countries,
        key="steps",
        max_selections=5,
        placeholder="Choose at least 1 country",
        label_visibility="visible",
        help="Required",
    )
    return selected_countries
