import numpy as np
import pandas as pd
import streamlit as st

from figure import plot_scatter
from utils import to_excel


def app():

    user_name = st.session_state["user_name"]
    user_data = st.session_state["user_data"]

    if user_name not in st.session_state.keys():
        st.session_state[user_name] = {}
        st.session_state[user_name][user_data] = []
    if user_data not in st.session_state[user_name].keys():
        st.session_state[user_name][user_data] = []

    st.markdown("#### Some Data ####")

    cols = st.columns((2, 2, 2, 5))
    with cols[0]:
        default = 0
        metric = st.selectbox(
            label="Metric A:",
            options=['metric1', 'metric2', 'metric3'],
            index=default,
        )
    with cols[2]:
        n_columns = st.number_input(
            label="Number of Columns:",
            min_value=2,
            max_value=16384,
            value=5000,
            key="n_columns_1"
        )
    with cols[3]:
        n_rows = st.number_input(
            label="Number of Rows:",
            min_value=2,
            value=100,
            max_value=1048576,
            key="n_rows_1"
        )

    cols = st.columns((3, 3))

    # create a random dataframe with 500 rows and 20 columns
    df = pd.DataFrame(np.random.randn(n_rows, n_columns), columns=[f"col_{i}" for i in range(n_columns)])
    st.session_state[user_name][user_data].append(df)
    with cols[0]:
        st.dataframe(df)
    with cols[1]:
        # create a scatter plot
        plot_scatter(df, x="col_0", y="col_1")

    to_excel(df, "Download", "data.xlsx")

    st.markdown("""---""")

    cols = st.columns((2, 2, 2, 5))
    with cols[0]:
        default = 0
        metric = st.selectbox(
            label="Metric B:",
            options=['metric1', 'metric2', 'metric3'],
            index=default,
        )
    with cols[2]:
        n_columns = st.number_input(
            label="Number of Columns:",
            min_value=2,
            value=5000,
            max_value=16384,
            key="n_columns_2"
        )
    with cols[3]:
        n_rows = st.number_input(
            label="Number of Rows:",
            min_value=2,
            value=100,
            max_value=1048576,
            key="n_rows_2"
        )
    cols = st.columns((3, 3))

    # create a random dataframe with 500 rows and 20 columns
    df = pd.DataFrame(np.random.randn(n_rows, n_columns), columns=[f"col_{i}" for i in range(n_columns)])
    st.session_state[user_name][user_data].append(df)
    with cols[0]:
        st.dataframe(df)
    with cols[1]:
        # create a scatter plot
        plot_scatter(df, x="col_0", y="col_1")

    to_excel(df, "Download", "data.xlsx")

    st.markdown("""---""")
