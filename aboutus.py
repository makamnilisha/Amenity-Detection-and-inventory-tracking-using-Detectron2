import streamlit as st

def aboutus():
    st.empty
    st.title("About Us")
    st.header("Our mission")
    st.write ("Help hosts and guest to have a smooth rental process fron start to end. ")
    st.header("Contributors")
    st.markdown('<a href="mailto:faiza.ayoun@sjsu.edu">Faiza Ayoun</a>', unsafe_allow_html=True)
    st.markdown('<a href="mailto:joshnadevi.vadapalli@sjsu.edu">Joshna Devi Vadapalli</a>', unsafe_allow_html=True)
    st.markdown('<a href="mailto:nilisha.makamprashantha@sjsu.edu">Nilisha Makam Prashantha</a>', unsafe_allow_html=True)
    st.markdown('<a href="mailto:sangamithra.murugesan@sjsu.edu">Sangamithra Murugesan</a>', unsafe_allow_html=True)
    st.write("From San Jose State University, Department of Applied Data Science")


