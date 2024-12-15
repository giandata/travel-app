import streamlit as st
from lists import price_ranges


def traveler_type():
    traveler_type = st.radio(
        label="**Traveler type:**",
        options=[
            "Solo Traveler",
            "Couple",
            "Family travel",
            "Group of friends",
        ],
        index=None,
        help="Optional setting for optimized travel based on traveler type",
        key="traveler_type",
    )

    return traveler_type


def accomodation():
    accomodation = st.pills(
        label="**Preferred accomodation**",
        options=["Hotel", "Vacation Rental", "Hostels", "Camping"],
        selection_mode="multi",
        help="Optional setting for preferred accomodation",
        key="accomodation",
    )
    return accomodation


def preferred_transport():
    transportation = st.pills(
        label="**Select the transportation preferences**",
        options=["Flights", "Train", "Car rental", "Public Transport", "Ferry"],
        selection_mode="multi",
        help="Optional setting for selecting preferred transportation",
        key="transportation",
    )
    return transportation


def night_transfers():
    overnight_transfers = st.checkbox(
        label="Look for overnight transfers",
        help="Optional setting for researching overnight transfers",
        key="night_transfers",
    )
    return overnight_transfers


def budget():
    price_range = st.select_slider(
        label="**Provide an indicative budget range (€)**",
        options=price_ranges,
        help="Optional setting for optimization of the travel plan based on budget preferences",
        key="budget",
    )
    return price_range
