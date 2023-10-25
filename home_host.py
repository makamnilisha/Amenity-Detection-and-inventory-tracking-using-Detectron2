import streamlit as st
import pandas as pd
import Detector
import dbconnect
import folium
from streamlit_folium import st_folium, folium_static
from Detector import *
from PIL import Image
from streamlit_option_menu import option_menu
import login
import aboutus


def main_part():
    selected = option_menu(menu_title=None,
                           options=['Home', 'Upload', 'Inventory', 'About Us'],
                           icons=['house', 'image', 'list', 'envelope'],
                           menu_icon="cast",
                           default_index=0,
                           orientation="horizontal"
                           )
    if selected == 'Home':
        st.title("Home")
    if selected == 'Upload':
        detection()
    if selected == 'Inventory':
        st.title("Inventory")
    if selected == 'About Us':
        aboutus.aboutus()


def listing(username, list_address):
    st.sidebar.header('Hello ' + username + '!')
    st.sidebar.header('Listing information')
    ticker = st.sidebar.selectbox(
        'select the address to verify amenities',
        list_address)
    button = st.sidebar.button("upload available amenities")
    st.sidebar.button("Log Out", key="logout", on_click=login.loggedOut_clicked)
    return ticker, button


def show_landing_page():
    username = st.session_state['username']
    mydb = dbconnect.connect_db()
    cursor1 = mydb.cursor()
    cursor2 = mydb.cursor()
    cursor1.execute(
        "SELECT A.ADDRESSID, A.LONGITUDE, A.LATITUDE, CONCAT(A.STREET1, ' ',A.STREET2,' ', A.CITY, ' ',A.STATE, ' ',A.ZIPCODE) FROM ADDRESS A, USER_LIST B WHERE A.USERID = B.USERID and B.USERNAME = %s;",
        [username])

    results1 = cursor1.fetchall()
    df = pd.DataFrame(results1, columns=['ADDRESSID', 'longitude', 'latitude', 'ADDRESS'])
    cursor2.execute(
        "SELECT AD.ADDRESSID, A.AMENITYNAME, AL.QUANTITY from AMENITY A , AMENITIES_LIST AL, USER_LIST UL, ADDRESS AD  where A.AMENITYID=AL.AMENITYID AND AL.ADDRESSID=AD.ADDRESSID AND AL.USERID=UL.USERID AND UL.USERNAME=%s;",
        [username])
    results2 = cursor2.fetchall()
    df1 = pd.DataFrame(results2, columns=['ADDRESSID', 'amenityname', 'quantity'])
    # mappoint = df[['latitude', 'latitude']]
    list_address = list(df['ADDRESS'])
    ticker, button = listing(username, list_address)
    ##
    addressid = list(df[df["ADDRESS"] == ticker]["ADDRESSID"])[0]
    st.header("Available Amenities")
    st.subheader(ticker)
    st.write(df1[df1["ADDRESSID"] == addressid][['amenityname', 'quantity']])
    ##
    m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()],
                   zoom_start=10, control_scale=True)

    # Loop through each row in the dataframe
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
        st_folium(m, width=300)


def detection():
    # st.title('Airbnb Object Detection and Inventory Management')
    st.header('Please upload an image')
    detector = Detector()
    image_file = st.file_uploader("Upload An Image", type=['png', 'jpeg', 'jpg'])
    if image_file is not None:
        # file_details = {"FileName": image_file.name, "FileType": image_file.type}
        # st.write(file_details)

        # img = Image.open(image_file)

        newsize = (320, 320)

        # st.image(img, caption='Uploaded Image.')
        with open(image_file.name, mode="wb") as f:
            f.write(image_file.getbuffer())
        # st.success("Saved File")
        listofitems = detector.onImage(image_file.name)
        img_ = Image.open("result.jpg")
        img_ = img_.resize(newsize)
        st.image(img_, caption='Processed Image.')
        item_counts = {}
        for item in listofitems:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1
        for key, value in item_counts.items():
            st.checkbox(str(value) + " " + str(key), key=key)
        # for item in listofitems :
        #    st.checkbox(item)
        return listofitems
