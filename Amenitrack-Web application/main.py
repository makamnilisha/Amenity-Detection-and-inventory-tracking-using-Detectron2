import streamlit as st

import home_guest
import login
import home_host


def main():
    #test comment
    st.title("Welcome to AmeniTrack")
    # first run will have nothing in session_state
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        login.show_login_page()
    else:
        if st.session_state['loggedIn']:
            if st.session_state['usertype'] == 'host':
                home_host.main_part()
            else:
                home_guest.main_part()
        else:
            login.show_login_page()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/




