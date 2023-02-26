import pandas as pd
import numpy as np 
import streamlit as st
import altair as alt
from numerize.numerize import numerize

st.set_page_config(page_title='AirLine Passenger Satisfaction',
                   layout='wide',
                   initial_sidebar_state='expanded')

# ------------ REMOVE FOOTER AND HAMBRUGER -----------
st.markdown("""
            <style>
            .css-164nlkn.egzxvld1
            {
                visibility: hidden;
            }
            </style>
            """,
            unsafe_allow_html=True)

@st.cache_resource
def get_data():
    #df = pd.read_csv('C:/Users/Mohammed Dolib/Desktop/Airline Passenger Satisfaction/Airline Passenger Satisfaction.csv')
    df = pd.read_csv('https://github.com/mdolib/Airline-Dashboard/raw/main/Airline%20Passenger%20Satisfaction.csv')
    return df

df = get_data()

header_left, header_mid, header_right = st.columns([1,3,1], gap='large')
with header_mid:
    st.title("Airline Passenger Surevy DashBoard")
    
    
with st.sidebar:
    st.sidebar.header('Airline Surevy Dashboard')
    gender_filter = st.multiselect(label='Select Gender:',
                                   options=df['Gender'].unique(),
                                   default=df['Gender'].unique())
    
    customer_type_filter = st.multiselect(label='Select Customer Type:',
                                          options=df['Customer Type'].unique(),
                                          default=df['Customer Type'].unique())
    
    age_filter = st.slider(label='Select Age', value=(df['Age'].min(), df['Age'].max()))
    
    # age_filter = st.multiselect(label='Select Age:',
    #                                       options=df['Age'].unique(),
    #                                       default=df['Age'].unique())
    
    Type_of_travel_filter = st.multiselect(label='Select Type of Travel:',
                                          options=df['Type of Travel'].unique(),
                                          default=df['Type of Travel'].unique())
    
    class_filter = st.multiselect(label='Select Type of Class:',
                                          options=df['Class'].unique(),
                                          default=df['Class'].unique())
    
    st.sidebar.markdown("""
                        ---
                        Created by : [Mohammed Dolib](https://www.linkedin.com/in/mohammed-dolib-96a09973)
                        """)

df1 = df.query("Gender == @gender_filter & `Customer Type` == @customer_type_filter & Age.between(@age_filter[0],@age_filter[1]) & `Type of Travel` == @Type_of_travel_filter & Class == @class_filter")

total_flight_distance = float(df1['Flight Distance'].sum())
total_departure_delay_in_minutes = float(df1['Departure Delay in Minutes'].sum()/60)
total_Arrival_delay_in_minutes = float(df1['Arrival Delay in Minutes'].sum()/60)
total_passengers = float(df1['id'].count())


st.markdown('### Metrics')
total1,total2,total3,total4 = st.columns(4,gap='large')

with total1:
    st.image('images/air-traffic.png', use_column_width='auto')
    st.metric(label='Total Flight Distances', value=numerize(total_flight_distance))

with total2:
    st.image('images/departure.png')
    st.metric(label='Toatal Departure Delay in Hours', value=round(total_departure_delay_in_minutes,2))
    
with total3:
    st.image('images/landing.png')
    st.metric(label='Total Arrival Delay in Hours', value=round(total_Arrival_delay_in_minutes,2))

with total4:
    st.image('images/passanger.png')
    st.metric(label='Total Passengers on Survey', value=numerize(total_passengers))

st.write('---')

q1,q2 = st.columns(2,gap='large')
with q1:
    fig1 = alt.Chart(df1).mark_bar().encode(
    x='Gender',
    y='count()'
    )
    st.altair_chart(fig1, use_container_width=True)
    
with q2:
    fig2 = alt.Chart(df1).mark_circle().encode(
        x='Departure Delay in Minutes',
        y='count()',
        color='Gender',
        size='satisfaction'
    )
    st.altair_chart(fig2,use_container_width=True)

st.write('---')

with st.container():
    st.markdown('### Services Rate By Passengers From 1 to 5')
    q3,q4 = st.columns((5,5))
    with q3:
        st.write('Online Booking')
        fig3 = alt.Chart(df1).mark_bar().encode(
            x='Ease of Online booking',
            y='count()'
            )
        st.altair_chart(fig3,use_container_width=True)
    
    with q4:
        st.write('Counters Services')
        fig4 = alt.Chart(df1).mark_bar().encode(
        x='Checkin service',
        y='count()'
        )
        st.altair_chart(fig4,use_container_width=True)
