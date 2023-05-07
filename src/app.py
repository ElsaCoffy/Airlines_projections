import datetime
import pandas as pd
import streamlit as st
from plotting import  draw_ts_multiple
from forecasting_utilities  import generate_route_df,forecast_data


     
def end_date(date_forecast, date_fin_dataset,nb_days): 
    if date_fin_dataset >= date_forecast+  datetime.timedelta(days=nb_days):
        return 0
    return 0


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

st.write(type(forecast_date))
if run_forecast: 
    ## Getting the historical traffic data 
    traffic_df  = generate_route_df(df,home_airport,paired_airport).drop(columns=["home_airport","paired_airport"])
    traffic_df= traffic_df.query('date <= "{comparison}"'.format(comparison=forecast_date))
    ## Doing the forecasting 
    traffic_df["prediction"] = [ None for k in range(traffic_df['date'].size)]


    st.markdown('# Table des vols, pour la destination choisie, avec le nombre de passager total par jour')

    st.markdown('## Table generated  from the forecast ')
    st.dataframe(traffic_df, width=600, height=300)

    # 

    st.plotly_chart(draw_ts_multiple(traffic_df, 'pax_total', covid_zone=True,display=False))
    st.plotly_chart(draw_ts_multiple(forecast_data(df,home_airport,paired_airport,nb_days).rename(columns={'ds': 'date', 'yhat': 'pax_total'}), 'pax_total', covid_zone=True,display=False))
