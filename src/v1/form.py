import streamlit as st


# Absolutely importing src requires the workspace root to be set (see project_root)
def render_form():
    from widget import destination, departure, travel_type, travel_preferences
    from lists import night_jets

    content = None  # Initialize content to None
    loading = None  # Initialize loading to None
    picture = None  # Initialize picture to None

    with st.form(key="input_form", clear_on_submit=True, border=False):
        st.subheader("Where do you want to travel?", anchor=False)
        st.markdown(
            "Which European countries do you want to travel to? Select up to 5 countries"
        )
        selected_countries = destination.country_selection()  # required
        st.divider()
        st.subheader("When do you want to travel?", anchor=False)

        col1, col2 = st.columns([3, 3], gap="large")
        with col1:
            date = departure.departure_date()
        with col2:
            duration = departure.travel_duration()
        st.divider()
        st.subheader("What is your travel style?", anchor=False)
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.write("Select the type of activities for your travel (required):")
            travel_activities = travel_type.travel_activities()  # required
        with col2:
            travel_pace = travel_type.travel_pace()  # required
        with st.expander("Provide more details for your customized travel plan"):
            traveler_type = travel_preferences.traveler_type()
            accomodation = travel_preferences.accomodation()
            transportation = travel_preferences.preferred_transport()
            overnight_transfers = travel_preferences.night_transfers()
            price_range = travel_preferences.budget()
            picture = st.checkbox(
                label="Generate AI picture",
                value=False,
                key="picbox",
                help="Only for Premium Users",
            )

        submit = st.form_submit_button(
            "Generate travel plan",
            type="primary",
            use_container_width=True,
            help="Select at least 1 destination and the travel style settings",
        )

        if submit:
            if not selected_countries:
                st.warning("Please select at least one destination country")
            elif not travel_activities:
                st.warning("Please select the type of activities")
            elif not travel_pace:
                st.warning("Please select the desired travel pace")
            else:
                loading = st.info(
                    "The Engine is creating your custom travel ... Wait for the plan 🚀🚀",
                    icon="ℹ️",
                )
                from src.v1.core.prompt_v1 import fill_script

                content = fill_script(
                    selected_countries,
                    travel_activities,
                    travel_pace,
                    duration,
                    date,
                    night_jets,
                    price_range,
                    transportation=transportation,
                    accomodation=accomodation,
                    overnight_transfers=overnight_transfers,
                    traveler_type=traveler_type,
                )
        return content, picture
