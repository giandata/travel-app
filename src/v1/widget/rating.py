import streamlit as st

@st.fragment
def render():
    st.write("Give the travel plan a rating:")
    st.feedback(options = "stars", key="rating") 
    if st.session_state["rating"] is not None :
        st.write("Thank you for your feedback!")
        st.info(f'You gave a {st.session_state["rating"] +1 } star{'' if st.session_state["rating"] > 0 else 's'} rating')
        st.session_state
 

