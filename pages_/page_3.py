import pandas as pd
import streamlit as st


def app() -> None:
    user_name = st.session_state["user_name"]
    user_data = st.session_state["user_data"]

    st.title(body="Uploads & Data")

    tab_1, tab_2 = st.tabs(
        tabs=['upload', 'data']
    )

    with tab_1:
        uploaded_file = st.file_uploader(label="Upload file", type=["xlsx"])
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            if user_name not in st.session_state.keys():
                st.session_state[user_name] = {}
                st.session_state[user_name][user_data] = []
            if user_data not in st.session_state[user_name].keys():
                st.session_state[user_name][user_data] = []
            st.session_state[user_name][user_data].append(df)
            st.write('Uploaded file:', df)
    with tab_2:
        if user_name in st.session_state.keys():
            if user_data in st.session_state[user_name].keys():
                for df in st.session_state[user_name][user_data]:
                    st.dataframe(df)