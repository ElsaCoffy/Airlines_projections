import prophet
import pandas as pd
import datetime


def generate_route_df(traffic_df: pd.DataFrame, homeAirport: str, pairedAirport: str) -> pd.DataFrame:
  """Extract route dataframe from traffic dataframe for route from home airport to paired airport

  Args:
  - traffic_df (pd.DataFrame): traffic dataframe
  - homeAirport (str): IATA Code for home airport
  - pairedAirport (str): IATA Code for paired airport

  Returns:
  - pd.DataFrame: aggregated daily PAX traffic on route (home-paired)
  """
  _df = (traffic_df
         .query('home_airport == "{home}" and paired_airport == "{paired}"'.format(home=homeAirport, paired=pairedAirport))
         .groupby(['home_airport', 'paired_airport', 'date'])
         .agg(pax_total=('pax', 'sum'))
         .reset_index()
         )
  print(_df.columns)
  return _df


def training_model(traffic_df : pd.DataFrame, homeAirport: str,  pairedAirport :str): 
    """Trains a Prophet model based on the traffic dataframe for the route from home airport to paired airport 

    Args:
    - traffic_df (pd.DataFrame): traffic dataframe
    - homeAirport (str): IATA Code for home airport
    - pairedAirport (str): IATA Code for paired airport 

    Returns:
    - a trained model for that route
    """
    _model = prophet.Prophet()
    _model.fit(generate_route_df(traffic_df,homeAirport,pairedAirport).rename(columns={'date': 'ds', 'pax_total': 'y'}))
    return _model       


def forecast_data(traffic_df : pd.DataFrame, homeAirport: str,  pairedAirport :str, forecastingRange: int, forecastingDateStart : datetime.date): 

    """Create a Prophet model, trains it and uses it to predict traffic dataframe for the route from home airport to paired airport. 
    The training happens on all the historical data. However, the evaluation of the data

    Args:
    - traffic_df (pd.DataFrame): traffic dataframe
    - homeAirport (str): IATA Code for home airport
    - pairedAirport (str): IATA Code for paired airport 
    - forecastingRange (int): Number of date to forecast
    - forecastingDateStart (date ):  Day of the start of forecasted data
    Returns:
    -_forecastedData (pd.DataFrame) : the forecasted data from the model, with their contribution.
    """

    _model = training_model(traffic_df,homeAirport,pairedAirport)
    # We generate the futureDf of the timestamps to forecast based on the parameters asked. We do not use the built-in function because it wouldn't handle the case where 
    # forecastingDateStart is prior to the latest historical data available. 
    traffic_df = generate_route_df(traffic_df,homeAirport,pairedAirport)
    if traffic_df['date'].min() < forecastingDateStart: 
      DateStart = traffic_df['date'].min()
    else :
      DateStart= forecastingDateStart
    
    future_date = pd.date_range(DateStart, forecastingDateStart + datetime.timedelta(days= forecastingRange)).to_frame(index=False, name='ds')
    historic_date = traffic_df.query('date < "{comparison}"'.format(comparison=forecastingDateStart)).rename(columns={'date' : 'ds'}).loc[:,['ds']]
    futureDf = pd.concat([historic_date,future_date])

    _forecastedData = _model.predict(futureDf)
    return _forecastedData

