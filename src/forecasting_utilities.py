import prophet
import pandas as pd


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


def forecast_data(traffic_df : pd.DataFrame, homeAirport: str,  pairedAirport :str, forecastingRange: int): 

    """Create a Prophet model, trains it and uses it to predict traffic dataframe for the route from home airport to paired airport 

    Args:
    - traffic_df (pd.DataFrame): traffic dataframe
    - homeAirport (str): IATA Code for home airport
    - pairedAirport (str): IATA Code for paired airport 
    - forecastingRange (int): 
    Returns:
    -_forecastedData (pd.DataFrame) : the forecasted data from the model, with their contribution.
    """
    _model = training_model(traffic_df,homeAirport,pairedAirport)
    futureDf = _model.make_future_dataframe(periods=forecastingRange)
    _forecastedData = _model.predict(futureDf)
    print(_forecastedData.head())
    return _forecastedData


    

def cleaning_forecasted_data(df_traffic: pd.DataFrame,forecastedData: pd.DataFrame):
  """Return a panda Dataframe ready for plotting, with the predicted data in a column 
    Args: 
    df_traffic (pd.DataFrame) : the traffic data frame
    forecastedData : the forecasted data

  



  """