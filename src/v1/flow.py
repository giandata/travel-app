import streamlit as st
import os
import sys
from lists import *
import hmac
from openai import OpenAI
from PIL import Image
import form
from widget import travel_type, destination

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
    st.title("BlinkTravel App🛤️", anchor=False)
    st.header("Tell the Engine about your dream travel, he will plan it for you!")
    st.divider()

    if "travel_plan" not in st.session_state:
        st.session_state["travel_plan"] = None

    logo = "logo.png"
    logo_pic = Image.open(logo)
    st.sidebar.write("Welcome to the travel planner !")
    st.sidebar.image(logo_pic)
    st.sidebar.write(st.session_state)

    content, picture = form.render_form()

    # TRAVEL CREATION
    if content != None:
        client = OpenAI(api_key=st.secrets["OPENAPI_API_KEY"])
        response = src.v1.core.planner.make_plan(client, content)
        st.session_state["travel_plan"] = True

    image_response = None
    if picture:
        image_response = src.v1.core.planner.create_image(
            client, travel_type, destination
        )

    if st.session_state["travel_plan"]:
        # loading.empty()
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
        with st.container(border=True):
            if overall_summary_match:
                tab_names.append("Itinerary Summary")
                tabs = st.tabs(tab_names)
            # Loop through tabs and generate content
            for i, tab in enumerate(tabs[:-1]):
                with tab:
                    st.markdown(days[i])
            with tabs[-1]:
                st.markdown(overall_summary)

            # todo avoid launching ballons
            # todo make that only 1 feedback can be given
            src.v1.widget.rating.render()
        st.session_state["travel_plan"] = False

        # st.download_button(data=response, label="Download itinerary")
        # Generate the PDF
        # pdf_buffer = src.v1.core.pdf.create_pdf(
        #    title_and_summary, days, overall_summary)

        if st.session_state["steps"]:
            countries_name = "_".join(
                st.session_state.steps
            )  # Join country names with underscores
            file_name = f"{countries_name}_blinktravel_plan.txt"

        # Provide a download button
        @st.fragment
        def download_itinerary():
            st.download_button(
                label="Download itinerary",
                data=response,  # pdf_buffer :TODO WHEN JSON THEN PDF
                file_name=file_name,
                # mime="application/pdf",
            )

        download_itinerary()

        st.cache_data.clear()


if __name__ == "__main__":
    run()
