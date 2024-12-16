import streamlit as st
from streamlit import session_state as ss
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

CONFIG_FILENAME = 'config.yaml'

with open(CONFIG_FILENAME) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

if "authentication_status" not in ss:
    ss["authentication_status"] = None

# Show login and register tabs if the user is not authenticated
if ss["authentication_status"] is None or not ss["authentication_status"]:
    st.header('Welcome to Fin Genius – Your Trusted Financial Advisor')

    login_tab, register_tab = st.tabs(['Login', 'Register'])

    with login_tab:
        authenticator.login(location='main')

        # if ss["authentication_status"]:
        #     authenticator.logout(location='main')    
        #     st.write(f'Welcome *{ss["name"]}*')

        if ss["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif ss["authentication_status"] is None:
            st.warning('Please enter your username and password')

    with register_tab:
        if not ss["authentication_status"]:
            try:
                email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user()
                if email_of_registered_user:
                    st.success('User registered successfully')
            except Exception as e:
                st.error(e)

    # We call below code in case of registration, reset password, etc.
    with open(CONFIG_FILENAME, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

elif ss["authentication_status"] is True:

    st.sidebar.title("Fin Genius App")
    st.sidebar.write("")  # Empty content
    st.sidebar.write("") 
    # --- Page setup ---
    home_page = st.Page(
        page="./views/home.py",
        title="Home",
        icon="🏠",
        default=True
    )
    advisor_page = st.Page(
        page="./views/advisor.py",
        title="Advisor",
        icon="🤖"
    )
    charts_page = st.Page(
        page="./views/charts.py",
        title="Charts",
        icon="📊"
    )


    # --- Navigation ---
    pg = st.navigation(pages=
        [home_page, advisor_page, charts_page]
        )
    st.sidebar.write("") 
    st.sidebar.write("") 
    st.sidebar.write("") 
    st.sidebar.markdown("---")  # Separator line
    
    authenticator.logout(button_name="🔓 Logout", location="sidebar", key="1")
    
    # st.logo("./assets/codingisfun_logo.png")
    st.sidebar.text("Made with ❤️ by FinGenius Team")
    pg.run()