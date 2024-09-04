import base64
import uuid
from typing import List
import io
import re
import pandas as pd
import streamlit as st


def to_excel(
    df: pd.DataFrame | pd.DataFrame,
    button_label: str,
    name: str,
    do_not_modify_columns: List[int] = None,
    keep_index: bool = True,
    **kwargs,
):
    buffer = io.BytesIO()
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(buffer, engine="xlsxwriter")
    # Write the DataFrame
    (
        df.to_excel(writer, sheet_name="Sheet1", startrow=1, index=keep_index)
        if do_not_modify_columns is not None
        else df.to_excel(writer, sheet_name="Sheet1", index=keep_index)
    )

    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    if do_not_modify_columns is not None:
        do_not_modify_columns = [0] + [i + 1 for i in do_not_modify_columns]
        red_fill_format = workbook.add_format({"bg_color": "red", "bold": True})
        for col in do_not_modify_columns:
            worksheet.write(0, col, "Do not modify this column", red_fill_format)

    # Close the Pandas Excel writer and output the Excel file to the buffer
    writer.save()

    # TODO: TO REFACTOR WHEN AVAILABLE STREAMLIT DOWNLOAD BUTTON WITHOUT RERUN (MAY-JUL 2024)
    # NOTE: params: `key` and `kwargs["use_container_width"]` are not evaluated due to this
    # temporary custom implementation. Unique `key` is guaranteed by `uuid4()` and all
    # download buttons have same size
    try:
        b64: str = base64.b64encode(buffer.getvalue()).decode()
    except AttributeError:
        b64: str = base64.b64encode(buffer.getvalue()).decode()

    button_uuid: str = str(object=uuid.uuid4()).replace("-", "")
    button_id: str = re.sub(pattern="\d+", repl="", string=button_uuid)
    custom_css: str = f""" 
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    download_link: str = (
        custom_css
        + f'<a download="{name}.xlsx" id="{button_id}" href="data:file/txt;base64,{b64}">{button_label}</a><br></br>'
    )
    st.markdown(body=download_link, unsafe_allow_html=True)