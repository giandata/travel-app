##TODO make a def and use a fragment
with st.form(key="receive_plan", clear_on_submit=True, border=False):
    st.text_input(label="Insert your email")
    submitted = st.form_submit_button("Receive plan")
if submitted:
    st.success("check your inbox")
