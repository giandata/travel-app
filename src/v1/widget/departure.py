import streamlit as st
from datetime import datetime, timedelta


def departure_date():
    now = datetime.now()
    date = st.date_input(
        label="Date of departure",
        value=now,
        min_value=now,
        max_value=now + timedelta(days=365),
        key="date",
        help="Select date of departure",
        format="YYYY/MM/DD",
        label_visibility="visible",
    )
    return date


def travel_duration():
    duration = st.slider(
        label="How many days you want to travel?",
        min_value=1,
        max_value=10,
        step=1,
        key="duration",
        help="Select how many days you want to travel",
        label_visibility="visible",
    )
    return duration
