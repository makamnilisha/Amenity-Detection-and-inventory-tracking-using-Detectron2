import streamlit as st
from user import login
def loggedIn_clicked(userName, password):
    st.balloons()
    if login(userName, password):
        st.session_state['loggedIn'] = True
        st.session_state['username'] = userName
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")
def loggedOut_clicked():
    st.session_state['loggedIn'] = False
def show_login_page():
    if st.session_state['loggedIn'] == False:
        userName = st.text_input(label="", value="", placeholder="Enter your user name")
        password = st.text_input(label="", value="", placeholder="Enter password", type="password")
        st.button("Login", on_click=loggedIn_clicked, args=(userName, password))

def show_logout_page():
    st.button("Log Out", key="logout", on_click=loggedOut_clicked)