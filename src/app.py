import datetime
import pandas as pd
import streamlit as st
from plotting import  draw_ts_multiple
from forecasting_utilities  import generate_route_df,forecast_data


     



HOME_AIRPORTS = ('LGW', 'LIS', 'LYS')
PAIRED_AIRPORTS = ('FUE', 'AMS', 'ORY')

df = pd.read_parquet('src/data/traffic_10lines.parquet')

st.title('Traffic Forecaster')

with st.sidebar:
    home_airport = st.selectbox(
        'Home Airport', HOME_AIRPORTS)
    paired_airport = st.selectbox(
        'Paired Airport', PAIRED_AIRPORTS)
    forecast_date = st.date_input('Forecast Start Date')
    nb_days = st.slider('Days of forecast', 7, 30, 1)
    run_forecast = st.button('Forecast')
    
#Input Data
st.write('Home Airport selected:', home_airport)
st.write('Paired Airport selected:', paired_airport)
st.write('Days of forecast:', nb_days)
st.write('Date selected:', forecast_date)

if run_forecast: 
    ## Getting the historical traffic data 
    traffic_df  = generate_route_df(df,home_airport,paired_airport).drop(columns=["home_airport","paired_airport"])
    traffic_df= traffic_df.query('date <= "{comparison}"'.format(comparison=forecast_date))
    ## Doing the forecasting 

    complete_data = forecast_data(df,home_airport,paired_airport,nb_days,forecast_date)

    complete_data=  complete_data.rename(columns={'ds': 'date', 'yhat': 'prediction'})

    complete_data.merge(traffic_df, on ='date', how = 'left',sort=True)



    st.markdown('# Table des vols, pour la destination choisie, avec le nombre de passager total par jour')

    st.markdown('## Table generated  from the forecast ')
    st.dataframe(complete_data, width=600, height=300)

    st.plotly_chart(draw_ts_multiple(complete_data, 'pax_total', covid_zone=True,display=False,prediction ='prediction'))

