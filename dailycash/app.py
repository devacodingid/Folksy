import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
with open('../config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

df = pd.read_csv('sales.csv')
data_df = st.data_editor(df, column_config= {"sales": st.column_config.LineChartColumn("sales", width="medium")}, hide_index=True,)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

st.title("Chart flow")

# creating a login widget
authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    with st.sidebar:
        st.write(f'Welcome {st.session_state["name"]}')
        authenticator.logout('Logout', 'main')
    st.write(data_df)
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')