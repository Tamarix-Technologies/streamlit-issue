import pandas as pd
import plotly.express as px
import streamlit as st


def plot_scatter(
    data: pd.DataFrame,
    x: str,
    y: str
) -> pd.DataFrame:
    fig = px.scatter(
        data,
        x=x,
        y=y,
        template="plotly_dark",
        size_max=60,
    )
    st.plotly_chart(fig, use_container_width=True)
    return data


