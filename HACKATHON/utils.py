import streamlit as st

def logout_button():
    with st.container():
        col1, col2 = st.columns([9, 1])  # 9:1 ratio places button on right
        with col2:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.rerun()
