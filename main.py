import time
import warnings
import streamlit as st

from pages_ import page_1, page_2, page_3
from persist import persist, load_widget_state

# Suppress FutureWarnings globally
warnings.filterwarnings(
    "ignore", category=FutureWarning
)  # TODO - remember FutureWarnings are suppressed

PAGES = {
    "Page 1": page_1,
    "Page 2": page_2,
    "Page 3": page_3
}
USERNAMES = ['A', 'B', 'C']
USER_DATA_LIST = ['Data X', 'Data Y', 'Data Z']


def main():
    # wide screen
    st.set_page_config(page_title="App", layout="wide")

    # hide streamlit branding and hamburger icon menu
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # keep run number
    if "run_number" not in st.session_state:
        st.session_state["run_number"] = 0
    else:
        st.session_state["run_number"] += 1

    # login
    login_container = st.empty()
    with login_container.container():
        authenticate = True

    # authenticated
    if authenticate:
        try:
            login_container.empty()
            time.sleep(0.2)  # A hack to make the empty stick.

            if "page_container" not in st.session_state:
                st.session_state["page_container"] = st.empty()

            users = USERNAMES
            cols = st.sidebar.columns((2, 1))
            with cols[0]:
                if len(users) > 1:
                    index_default = (
                        users.index(st.session_state.get("user_name"))
                        if "user_name" in st.session_state
                        else 0
                    )
                    user_name = st.selectbox(
                        "User",
                        sorted(users),
                        key=persist("user_name"),
                        index=index_default,
                        on_change=on_user_change,
                    )
                else:
                    user_name = users[0]
                    st.session_state["user_name"] = user_name

                if "user_data_list" not in st.session_state:
                    st.session_state["user_data_list"] = USER_DATA_LIST

                data_name = st.selectbox(
                    "Data Name",
                    sorted(st.session_state["user_data_list"]),
                    key=persist("user_data"),
                    index=0,
                    on_change=on_data_change,
                )
                date = st.date_input("Date", key="date", on_change=on_date_change)
                # raise error if date > today
                if date > date.today():
                    st.error("Date cannot be in the future")
                    st.stop()
        except Exception as e:
            st.error(e)
            st.stop()
        persist(data_name)
        persist(user_name)
        persist(date)

        # display sidebar, with intro as home page
        st.sidebar.markdown(" ")
        st.sidebar.markdown(" ")
        st.sidebar.markdown("## Menu ##")

        if (
            "pages" not in st.session_state
        ):
            init_menu(user_name=user_name)

        with st.sidebar:
            selection = st.sidebar.radio(
                label="sidebar_radio",
                options=[
                    page
                    for page in PAGES
                    if page in st.session_state["pages"].keys()
                ],
                key='menu_selection',
                index=0,
                on_change=on_selection_change,
                label_visibility="hidden",
            )

        if selection not in st.session_state["pages"].keys():
            selection = list(st.session_state["pages"].keys())[0]
        page = st.session_state["pages"][selection]
        page_container = st.session_state["page_container"]
        with page_container.container():
            # Set top of page as initial position
            st.write("#")
            # logout button
            cols = st.columns((10, 1))
            with cols[1]:
                if st.button("Log out"):
                    st.session_state.clear()
                    st.rerun()

            # page rendering
            page.app()


# ------------------------------ UTILS ------------------------------ #


def on_user_change():
    user_name = st.session_state["user_name"]
    delete_usernames = [usernames for usernames in USERNAMES if usernames != st.session_state["user_name"]]
    for user in delete_usernames:
        delete_cache(user)
    init_menu(user_name=user_name)


def on_data_change():
    st.session_state["page_container"].empty()
    st.session_state["show_deal_analytics"] = False
    for user in USERNAMES:
        for data in USER_DATA_LIST:
            if user != st.session_state["user_name"]:
                delete_cache(user_name=user, user_data=data)
    time.sleep(0.2)


def on_selection_change():
    st.session_state["page_container"].empty()
    st.session_state["show_deal_analytics"] = False
    time.sleep(0.2)


def on_date_change():
    st.session_state["page_container"].empty()
    st.session_state["show_deal_analytics"] = False
    time.sleep(0.2)


def delete_cache(user_name: str, user_data: str = None) -> None:
    if user_data:
        if user_name in st.session_state.keys():
            if user_data in st.session_state[user_name].keys():
                st.session_state[user_name][user_data] = []
    else:
        if user_name in st.session_state.keys():
            st.session_state[user_name] = {}
    return


def init_menu(user_name: str) -> None:
    pages = PAGES
    st.session_state["pages"] = pages
    return


if __name__ == "__main__":
    load_widget_state()
    main()
