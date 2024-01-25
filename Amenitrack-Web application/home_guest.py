import streamlit as st
import pandas as pd
import dbconnect
import folium
from streamlit_folium import st_folium
from upload_screen_guest import detection, check_lists
from streamlit_option_menu import option_menu
import login
import aboutus
import Inventory
def main_part():
    selected = option_menu(menu_title=None,
                           options=['Home', 'Upload', 'About Us'],
                           icons=['house', 'image', 'envelope'],
                           menu_icon="cast",
                           default_index=0,
                           orientation="horizontal"
                           )

    username, df, df1 = show_landing_page()
    list_address = list(df['ADDRESS'])
    #ticker, button = listing(username, list_address)
    ticker = listing(username, list_address)
    ##
    addressid = list(df[df["ADDRESS"] == ticker]["ADDRESSID"])[0]
    show_map(df, df1)
    #if "item_counts" not in st.session_state:
    #    st.session_state["item_counts"] = {}

    if selected == 'Home':
        st.session_state["item_counts"] = {}
        if ticker:
            st.header("Available Amenities")
            st.subheader(ticker)
            st.write(df1[df1["ADDRESSID"] == addressid][['amenityname', 'quantity']])


    if selected == 'Upload':
        item_counts = detection()
        if item_counts is not None:
            st.subheader(ticker)
            check_lists(df1, addressid)

    if selected == 'About Us':
        aboutus.aboutus()

    show_landing_page()


def listing(username, list_address):
    st.sidebar.header('Hello ' + username + '!')
    st.sidebar.header('Listing information')
    ticker = st.sidebar.selectbox(
        'select the address to verify amenities',
        list_address)
    # button = st.sidebar.button("upload available amenities")
    st.sidebar.button("Log Out", key="logout", on_click=login.loggedOut_clicked)
    return ticker  # , button


def show_landing_page():
    username = st.session_state['username']
    mydb = dbconnect.connect_db()
    cursor1 = mydb.cursor()
    cursor2 = mydb.cursor()
    cursor1.execute(
        "SELECT distinct A.ADDRESSID, A.LONGITUDE, A.LATITUDE, CONCAT(A.STREET1,' ', A.CITY, ' ',A.STATE, ' ',A.ZIPCODE) FROM ADDRESS A, USER_LIST B, TRANSACTIONS C WHERE B.USERID = C.USERID_GUEST and A.ADDRESSID= C.ADDRESSID and CHANGED_BY is null and B.USERNAME =  %s;",
        [username])
    results1 = cursor1.fetchall()
    df = pd.DataFrame(results1, columns=['ADDRESSID', 'longitude', 'latitude', 'ADDRESS'])
    cursor2.execute(
        "SELECT distinct AD.ADDRESSID, A.AMENITYNAME, AL.QUANTITY, C.USERID_HOST from AMENITY A , AMENITIES_LIST AL, USER_LIST UL, "
        "ADDRESS AD, TRANSACTIONS C  where A.AMENITYID=AL.AMENITYID AND AL.ADDRESSID=AD.ADDRESSID AND "
        "AL.USERID=UL.USERID AND UL.USERID = C.USERID_HOST AND C.ADDRESSID=AD.ADDRESSID AND C.USERID_GUEST= (SELECT "
        "USERID FROM USER_LIST WHERE USERNAME = %s);", [username])
    results2 = cursor2.fetchall()
    df1 = pd.DataFrame(results2, columns=['ADDRESSID', 'amenityname', 'quantity', 'hostid'])
    return username, df, df1



def show_map(df, df1):
    m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()],
                   zoom_start=10, control_scale=True)
    with st.sidebar:
        for i, row in df.iterrows():
            # Filter the amenities DataFrame for the current address
            amenities_for_address = df1[df1['ADDRESSID'] == row['ADDRESSID']]
            # Setup the content of the popup
            popup_content = f"<b>Address:</b> {str(row['ADDRESS'])}<br>"
            # Create a list to store amenity names with quantities
            amenity_list = []
            # Loop through amenities for the current address and add to the list
            for _, amenity_row in amenities_for_address.iterrows():
                amenity_list.append(f"{amenity_row['amenityname']} ({amenity_row['quantity']})")

            # Combine the amenity names with quantities into a string
            amenities_str = "<br>".join(amenity_list)

            # Add the combined amenities string to the popup content
            popup_content += f"<b>Amenities:</b> {amenities_str}<br>"

            # Create a marker with the popup content
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(popup_content, min_width=200, max_width=200)
            ).add_to(m)

        st.write("Map with Address and Amenity Information")
        st_folium(m, width=300, height=300)
