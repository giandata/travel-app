import streamlit as st


@st.fragment
def render():
    import time

    if "feedback_submitted" not in st.session_state:
        st.session_state["feedback_submitted"] = False

    if st.session_state["feedback_submitted"]:
        st.write("Thank you for your feedback!")

    if not st.session_state["feedback_submitted"]:
        st.markdown("**Give the travel plan a rating:**")
        st.feedback(options="stars", key="rating")

        if st.session_state.get("rating") is not None:
            st.session_state["feedback_submitted"] = True
            st.info(
                f'You gave a {st.session_state["rating"] + 1} star{"s" if st.session_state["rating"] > 0 else ""} rating'
            )
