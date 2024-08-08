import streamlit as st
from datetime import datetime, timedelta
import os
import sys
from lists import *
import hmac
from openai import OpenAI

# The following line allows using absolute imports relative to "src"
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

# Absolutely importing src requires the workspace root to be set (see project_root)
import src


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()


def run():
    st.cache_data.clear()
    st.title("Travel Planner Ai ✈️")
    st.header("Tell the Engine about your dream travel, he will plan it for you!")

    logo_path = r"C:\Users\39380\Desktop\workspace\projects\travel-app\src\v1\logo.jpg"
    st.sidebar.image(logo_path)

    with st.container(border=True):

        st.subheader("Where do you want to travel?")
        st.write(
            "Which european countries you want to travel to? Select up to 5 countries"
        )
        selected_countries = st.multiselect(
            label="Countries to visit",
            options=countries,
            key="steps",
            help="Select up to 5 countries to visit",
            max_selections=5,
            placeholder="Choose at least 1 country",
            label_visibility="visible",
        )

        st.write("")

        st.divider()
        st.subheader("When do you want to travel?")

        col1, col2 = st.columns([3, 3], gap="large")
        with col1:
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

        with col2:
            duration = st.slider(
                label="How many days you want to travel?",
                min_value=1,
                max_value=10,
                step=1,
                key="duration",
                help="Select how many days you want to travel",
                label_visibility="visible",
            )

        st.divider()
        st.subheader("What is your travel style?")

        col1, col2 = st.columns(2)
        with col1:
            st.write("Select the activities to be searched:")
            from src.v1 import widget

            travel_type = widget.travel_type.render_toggle()

        with col2:
            travel_style = st.radio(
                label="Select the travel pace",
                options=["Relaxed", "Moderate", "Fast-paced"],
                index=None,
            )
        st.write("")
        with st.expander(
            "Provide more details about your travel preferences for personalized travel plan:"
        ):
            traveler_type = st.radio(
                label="Traveler type:",
                options=[
                    "Solo Traveler",
                    "Couple",
                    "Family travel",
                    "Group of friends",
                ],
            )
            transportation = st.multiselect(
                label="Select the transportation preferences",
                options=["Flights", "Train", "Car rental", "Public Transport", "Ferry"],
            )

            accomodation = st.radio(
                label="Preferred accomodation",
                options=["Hotel", "Vacation Rental", "Hostels", "Camping"],
            )
            overnight_transfers = st.checkbox(
                label="Check this box if you want to look for overnight transfers"
            )

            st.write("Budget Settings")
            price_range = st.select_slider(
                label="Provide an indicative price range (€)",
                options=price_ranges,
                help="Specify the travel budget to organize a travel that best suits you",
            )

        st.write("")
        picture = st.checkbox(label="Generate AI picture", value=False, key="picbox")

        disabled = selected_countries is None or travel_type is None

        if disabled == False:
            from src.v1.core.prompt_v1 import fill_script

            content = fill_script(
                selected_countries, duration, date, night_jets, price_range, travel_type
            )

    pressed = st.button(
        label="Creare Personalized travel plan",
        key="submit_form",
        disabled=disabled,
        use_container_width=True,
        type="primary",
    )
    if pressed:
        if not selected_countries:
            st.warning("Please select at least one destination country.")
        elif not travel_type:
            st.warning("Please select the type of activities.")
        else:
            # TRAVEL CREATION
            loading = st.info(
                "The Engine is creating a personalized travel... Wait for the plan 🚀🚀",
                icon="ℹ️",
            )

        client = OpenAI(api_key=st.secrets["OPENAPI_API_KEY"])
        response = src.v1.core.planner.make_plan(client, content)

        image_response = None
        if picture:
            image_response = src.v1.core.planner.create_image(
                client, travel_type, selected_countries
            )

            loading.empty()
            st.balloons()
            st.success("Travel plan is ready!", icon="✈️")

        title_and_summary, days, overall_summary, overall_summary_match = (
            src.v1.core.response_processor.response_splitter(response)
        )

        # Display itinerary summary
        st.markdown(title_and_summary)

        if image_response is not None:
            src.v1.core.planner.display_image_from_url(image_response)

        # Display each day’s details in a single expander
        tab_names = [day.split(":")[0] for day in days]
        if overall_summary_match:
            tab_names.append("Itinerary Summary")
            tabs = st.tabs(tab_names)
        # Loop through tabs and generate content
        for i, tab in enumerate(tabs[:-1]):
            with tab:
                st.markdown(days[i])
        with tabs[-1]:
            st.markdown(overall_summary)

        src.v1.widget.rating.render()

        st.download_button(data=response, label="Download itinerary")

        st.cache_data.clear()


if __name__ == "__main__":
    run()
