from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

import home_host
import streamlit as st
import pandas as pd
import dbconnect
import plotly.express as px

def detected_list():
    mydb = dbconnect.connect_db()

    addressid = 1

    if 'selected_addressid' in st.session_state:
        addressid = st.session_state['selected_addressid']
    query = "SELECT A.AMENITYNAME,T.COUNT,T.START_DATE FROM TRANSACTIONS AS T JOIN AMENITY AS A ON T.AMENITYID = A.AMENITYID WHERE ADDRESSID=%s AND TRACKING_REQUIRED='yes' ORDER BY START_DATE ASC;" % addressid

    df = pd.read_sql(query, mydb);

    # Close database connection
    mydb.close();

    # Convert START_DATE to datetime
    df['START_DATE'] = pd.to_datetime(df['START_DATE'])

    # Pivot the DataFrame to have dates as index and amenities as columns
    df_pivot = df.pivot(index='START_DATE', columns='AMENITYNAME', values='COUNT').fillna(0)

    # Streamlit app
    st.title('Inventory Management and Tracking Chart ')

    # Convert the pivot table DataFrame to a format suitable for Plotly
    df_long = df_pivot.reset_index().melt(id_vars='START_DATE', var_name='Amenity', value_name='Count')

    # Create the interactive Plotly figure
    fig = px.line(df_long, x='START_DATE', y='Count', color='Amenity', markers=True)

    # Update layout options to format the dates with the year included
    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font_color='white',
        legend_title_font_color="white",
        legend_font_color="white",
        xaxis=dict(
            tickformat="%d-%b-%Y",  # Here's where we specify the tick label format
            title='CheckIn-date',  # Set the title for the x-axis
            title_font=dict(color='white'),
            tickfont=dict(color='white')

        ),
        yaxis=dict(
            title='Count',
            title_font=dict(color='white'),
            tickfont=dict(color='white')
        )
    )

    # Show the interactive figure in Streamlit
    st.plotly_chart(fig)