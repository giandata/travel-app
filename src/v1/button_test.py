import streamlit as st
import time

# Initialize session state variables
if "plan_created" not in st.session_state:
    st.session_state.plan_created = False
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False
if "response" not in st.session_state:
    st.session_state.response = None
if "image_response" not in st.session_state:
    st.session_state.image_response = None
if "destinations" not in st.session_state:
    st.session_state.destinations = []
if "activities" not in st.session_state:
    st.session_state.activities = []
if "pace" not in st.session_state:
    st.session_state.pace = None
st.sidebar.write(st.session_state)


# Define a function to check if all required inputs are filled
def inputs_filled():
    return (
        st.session_state.destinations
        and st.session_state.activities
        and st.session_state.pace
    )


# User inputs
st.session_state.destinations = st.multiselect(
    "Select your destinations", ["Italy", "France", "Spain"]
)

st.session_state.activities = st.multiselect(
    "Select your travel activities",
    ["Sightseeing", "Hiking", "Food Tasting", "Shopping"],
)

st.session_state.pace = st.radio(
    "Select your travel pace", ["Relaxed", "Moderate", "Fast"], index=None
)


def callback():
    st.session_state.button_clicked = True


# MOCK APP
# Define the button click behavior
def click_button():
    if not st.session_state.destinations:
        st.warning("Select the destinations ")
        st.session_state.button_clicked = False
    elif not st.session_state.activities:
        st.warning("Select the activities")
        st.session_state.button_clicked = False
    elif not st.session_state.pace:
        st.warning("select the travel pace")
        st.session_state.button_clicked = False
    else:
        st.session_state.button_clicked = True  ## GANCIO PER DISATTIVAZIONE BOTTONE
        st.session_state.loading = st.info(
            "The Engine is creating your custom travel ... Wait for the plan 🚀🚀",
            icon="ℹ️",
        )
        st.session_state.plan_created = False

        # Simulated travel plan result
        st.session_state.response = "Your custom travel plan: Visit Italy and enjoy sightseeing and food tasting at a relaxed pace."
        st.session_state.plan_created = True
        st.session_state.loading.empty()
        st.success("Travel plan is ready!")


### lo renderizza quando il codice di sopra finisce, ecco perchè non immediatamente viene disattivato il bottone!!
# possible work around : show modal saying plan is created

# Render the button
if not st.session_state.button_clicked:
    if st.button(
        label="Create Personalized Travel Plan",
        use_container_width=True,
        type="primary",
        help="Select at least 1 destination and the travel style settings",
        disabled=st.session_state.button_clicked,  ## RACCOGLIE GANCIO DISATTIVAZIONE
    ):
        click_button()

# Display the travel plan if created
if st.session_state.plan_created:
    st.markdown(st.session_state.response)
    if st.button("Start New Plan"):
        # Save the current plan here if needed
        st.session_state.plan_created = False
        st.session_state.button_clicked = False
        st.session_state.destinations = []
        st.session_state.activities = []
        st.session_state.pace = None
        st.session_state.response = None
        st.cache_data.clear()
