import streamlit as st
from user import login
def loggedIn_clicked(userName, password):
    st.balloons()
    user = login(userName, password)
    if not user:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")
    else:
        st.session_state['loggedIn'] = True
        st.session_state['username'] = userName
        st.session_state['usertype'] = user[2]
def loggedOut_clicked():
    st.session_state['loggedIn'] = False
def show_login_page():
    if st.session_state['loggedIn'] == False:
        userName = st.text_input(label="", value="", placeholder="Enter your user name")
        password = st.text_input(label="", value="", placeholder="Enter password", type="password")
        st.button("Login", on_click=loggedIn_clicked, args=(userName, password))
        st.markdown("#")
        st.markdown("#")
        st.title("Sign-Up Page")

        # Create a sign-Up form
        with st.form(key='sign_up_form'):
            first_name = st.text_input("First Name").strip()
            last_name = st.text_input("Last Name").strip()
            user_name = st.text_input("User Name").strip()
            email = st.text_input("Email ID", max_chars=50).strip()
            password = st.text_input("Password", type='password').strip()
            submit_button = st.form_submit_button(label='Sign Up')

def show_logout_page():
    st.button("Log Out", key="logout", on_click=loggedOut_clicked)