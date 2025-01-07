import streamlit as st
from lists import countries, european_cities


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
    default = st.session_state.get("selected_countries", [])
    st.session_state["selected_countries"] = selected_countries
    return st.session_state.selected_countries


def city_selection():
    selected_countries = st.session_state.get("selected_countries", [])
    if selected_countries:
        # Combine cities from selected countries
        available_cities = [
            city
            for country in selected_countries
            for city in european_cities.get(country, [])
        ]
        starting_city = st.pills(
            label="**Cities to include in your itinerary**",
            options=available_cities,
            key="cities",
            selection_mode="single",
            label_visibility="visible",
            help="Optional selection",
            default=None,
        )
        st.session_state["starting_city"] = starting_city
        return starting_city
    else:
        st.session_state["starting_city"] = []
        return []
