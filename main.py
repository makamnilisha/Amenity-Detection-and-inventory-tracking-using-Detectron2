import streamlit as st
import pandas as pd
import dbconnect
import folium
from streamlit_folium import st_folium, folium_static

### test commit to github
def listing(list_address):
    st.sidebar.header('Listing information')
    ticker = st.sidebar.selectbox(
        'select the address to verify amenities',
        list_address)
    button = st.sidebar.button("upload available amenities")
    return ticker, button


def main():
    username = st.sidebar.text_input('username')
    username = 'bobby'
    #username1='tommy'
    mydb = dbconnect.connect_db()
    cursor1 = mydb.cursor()
    cursor2=mydb.cursor()
    cursor1.execute(
        "SELECT A.ADDRESSID, A.LONGITUDE, A.LATITUDE, CONCAT(A.STREET1, ' ',A.STREET2,' ', A.CITY, ' ',A.STATE, ' ',A.ZIPCODE) FROM ADDRESS A, USER_LIST B WHERE A.USERID = B.USERID and B.USERNAME = %s;",
        [username])

    results1=cursor1.fetchall()
    df = pd.DataFrame(results1, columns=['ADDRESSID', 'longitude', 'latitude', 'ADDRESS'])
    cursor2.execute("SELECT AD.ADDRESSID, A.AMENITYNAME, AL.QUANTITY from AMENITY A , AMENITIES_LIST AL, USER_LIST UL, ADDRESS AD  where A.AMENITYID=AL.AMENITYID AND AL.ADDRESSID=AD.ADDRESSID AND AL.USERID=UL.USERID AND UL.USERNAME='bobby';")
    results2 = cursor2.fetchall()
    df1 = pd.DataFrame(results2,columns=['ADDRESSID','amenityname','quantity'])
    #mappoint = df[['latitude', 'latitude']]
    list_address = list(df['ADDRESS'])
    listing(list_address)
    m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()],
                   zoom_start=10, control_scale=True)

    # Loop through each row in the dataframe
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
            popup=folium.Popup(popup_content, min_width=300, max_width=300)
        ).add_to(m)

    st.write("Map with Address and Amenity Information")
    st_folium(m, width=700)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/










