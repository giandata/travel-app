import streamlit as st
from lists import price_ranges


def traveler_type():
    traveler_type = st.radio(
        label="Traveler type:",
        options=[
            "Solo Traveler",
            "Couple",
            "Family travel",
            "Group of friends",
        ],
        index=None,
        help="Optional",
        key="traveler_type",
    )

    return traveler_type


def accomodation():
    accomodation = st.radio(
        label="Preferred accomodation",
        options=["Hotel", "Vacation Rental", "Hostels", "Camping"],
        index=None,
        help="Optional",
        key="accomodation",
    )
    return accomodation


def preferred_transport():
    transportation = st.multiselect(
        label="Select the transportation preferences",
        options=["Flights", "Train", "Car rental", "Public Transport", "Ferry"],
        help="Optional",
        key="transportation",
    )
    return transportation


def night_transfers():
    overnight_transfers = st.checkbox(
        label="Look for overnight transfers",
        help="Optional",
        key="night_transfers",
    )
    return overnight_transfers


def budget():
    st.write("Budget Settings")
    price_range = st.select_slider(
        label="Provide an indicative price range (€)",
        options=price_ranges,
        help="Specify the travel budget to organize a travel that best suits you",
        key="budget",
    )
    return price_range
