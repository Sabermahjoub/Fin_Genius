import streamlit as st

st.sidebar.title("Fin Genius App")

# --- Page setup ---
home_page = st.Page(
    page="./views/home.py",
    title="Home",
    icon=":material/account_circle:",
    default=True
)
advisor_page = st.Page(
    page="./views/advisor.py",
    title="Advisor",
    icon=":material/smart_toy:"
)

# --- Navigation ---
pg = st.navigation(pages=
    {
        "info": [home_page],
        "links":[advisor_page]
    })

# st.logo("./assets/codingisfun_logo.png")
st.sidebar.text("Made with ❤️ by FinGenius Team")
pg.run()