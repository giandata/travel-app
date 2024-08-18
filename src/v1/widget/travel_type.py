import streamlit as st

toggles = {
    "Historical and cultural": False,
    "Nature and landscapes": False,
    "Social and local events": False,
    "Food Lover": False,
    "Relax and wellness": False,
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


def travel_pace():
    travel_pace = st.radio(
        label="Select the travel pace",
        options=["Relaxed", "Moderate", "Fast-paced"],
        index=None,
        help="Required",
        key="travel_pace",
    )
    return travel_pace
