import streamlit as st


def travel_pace():
    travel_pace = st.radio(
        label="**Select the travel pace**",
        options=["Static", "Relaxed", "Moderate", "Fast-paced"],
        index=None,
        help="How often you would like to change destinations during your trip. This will help us plan your travel pace",
        key="travel_pace",
        horizontal=True,
    )
    return travel_pace


toggles = {
    "City sightseeing": False,
    "Cultural and Historic": False,
    "Hiking and Nature": False,
    "Social and Events": False,
    "Local cuisine": False,
    "Relax and Wellness": False,
    "Concerts and Festivale": False,
    "Locals experience": False,
    "Hidden Gems": False,
}


def render_toggle():
    if "toggle_states" not in st.session_state:
        st.session_state.toggle_states = toggles

    def update_toggle(key):
        st.session_state.toggle_states[key] = not st.session_state.toggle_states[key]

    for key in toggles:
        st.toggle(
            label=key,
            value=st.session_state.toggle_states[key],
            key=key,
            label_visibility="visible",
            on_change=update_toggle,
            args=(key,),
        )

    return [key for key, value in st.session_state.toggle_states.items() if value]


def travel_activities():
    activities = st.pills(
        label="**Choose at least 1 type of activity**",
        options=[
            "City sightseeing",
            "Cultural and Historic",
            "Local cuisine",
            "Hiking and Nature",
            "Relax and Wellness",
            "Social and Events",
            "Concerts and Festivals",
            "Locals experience",
            "Hidden Gems",
        ],
        selection_mode="multi",
        default=None,
        key="travel activities",
        label_visibility="visible",
        help="Required",
    )
    st.session_state["travel_activities"] = activities
    return st.session_state["travel_activities"]
