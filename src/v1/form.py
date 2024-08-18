import streamlit as st
import os
import sys

# The following line allows using absolute imports relative to "src"
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

# Absolutely importing src requires the workspace root to be set (see project_root)
import src


from src.v1 import widget
from widget import destination, departure, travel_type, travel_preferences

st.sidebar.write(st.session_state)

with st.form(key="input_form", clear_on_submit=True, border=False):
    selected_countries = destination.country_selection()  # required
    date = departure.departure_date()
    duration = departure.travel_duration()
    travel_activities = widget.travel_type.travel_activities()  # required
    travel_pace = widget.travel_type.travel_pace()  # required
    st.divider()
    traveler_type = travel_preferences.traveler_type()
    accomodation = travel_preferences.accomodation()
    transportation = travel_preferences.preferred_transport()
    overnight_transfers = travel_preferences.night_transfers()
    price_range = travel_preferences.budget()
    submit = st.form_submit_button("Create travel plan")
    if submit:
        if not selected_countries:
            st.warning("Please select at least one destination country")
        elif not travel_activities:
            st.warning("Please select the type of activities")
        elif not travel_pace:
            st.warning("Please select the desider travel pace")
        else:
            st.info("can create a plan now")
