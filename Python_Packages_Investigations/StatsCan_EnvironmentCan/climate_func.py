# Import libraries and modules
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from dateutil import rrule
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re
from fuzzywuzzy import fuzz 
from tqdm import tnrange, tqdm_notebook
from time import sleep



def store_data_in_soup_frames(province,start_year,max_pages):
    
    try:
        if province in {'BC','PE','NS','NL','NB','QC','ON','MB','SK','AB','YT','NT','NU'} and type(start_year)==str and len(start_year)==4 and type(max_pages)==int:
        # Store each page in a list and parse them later
            soup_frames = []

            for i in tnrange(100, desc='Downloading Data'):
                startRow = 1 + i*100
                sleep(0.01)
    
                base_url = "http://climate.weather.gc.ca/historical_data/search_historic_data_stations_e.html?"
                queryProvince = "searchType=stnProv&timeframe=1&lstProvince={}&optLimit=yearRange&".format(province)
                queryYear = "StartYear={}&EndYear=2017&Year=2017&Month=5&Day=29&selRowPerPage=100&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&".format(start_year)
                queryStartRow = "startRow={}".format(startRow)

                response = requests.get(base_url + queryProvince + queryYear + queryStartRow) # Using requests to read the HTML source
                soup = BeautifulSoup(response.text, 'html.parser') # Parse with Beautiful Soup
                soup_frames.append(soup)

            return soup_frames
        else:
            print("INVALID INPUT\n\nENTER A PROVINCE AS A STRING:\n'BC','PE','NS','NL','NB','QC','ON','MB','SK','AB','YT','NT'\nENTER YEAR AS A STRING:'1992'\nENTER A MAXIMUM NUMBER OF PAGES AS AN INTEGER, i.e. 1,2,3,4,5")
    except:
        print("INVALID INPUT\n\nENTER A PROVINCE AS A STRING:\n'BC','PE','NS','NL','NB','QC','ON','MB','SK','AB','YT','NT'\nENTER YEAR AS A STRING:'1992'\nENTER A MAXIMUM NUMBER OF PAGES AS AN INTEGER, i.e. 1,2,3,4,5")
        
        
def generate_pandas_dataframe_from_soups(soup_frames):
    
    # Empty list to store the station data
    station_data = []
    for i in tnrange(len(soup_frames), desc='Generating Pandas DataFrames'):# For each soup
        sleep(0.01)
        forms = soup_frames[i].findAll("form", {"id" : re.compile('stnRequest*')}) # We find the forms with the stnRequest* ID using regex
        for form in forms:
            try:

                # The stationID is a child of the form
                station = form.find("input", {"name" : "StationID"})['value']
            
                # The station name is a sibling of the input element named lstProvince
                name = form.find("input", {"name" : "lstProvince"}).find_next_siblings("div")[0].text
            
                # The intervals are listed as children in a 'select' tag named timeframe
                timeframes = form.find("select", {"name" : "timeframe"}).findChildren()
                intervals =[t.text for t in timeframes]
            
                # We can find the min and max year of this station using the first and last child
                years = form.find("select", {"name" : "Year"}).findChildren()            
                min_year = years[0].text
                max_year = years[-1].text
            
                # Store the data in an array
                data = [station, name, intervals, min_year, max_year]
                station_data.append(data)
            except:
                pass

    # Create a pandas dataframe using the collected data and give it the appropriate column names
    stations_df = pd.DataFrame(station_data, columns=['StationID', 'Name', 'Intervals', 'Year Start', 'Year End'])
    return stations_df
    
    
def get_weather_data_by_loc(stations_df, location_name):
    
    try:
        tolerance = 90
        by_city_df = stations_df[stations_df['Name'].apply(lambda x: fuzz.token_set_ratio(x, location_name)) > tolerance]
        return by_city_df
    except:
        print("INVALID INPUT. ENTER A PANDAS DF FROM SOUPS AND A LOCATION, i.e, VANCOUVER, WHISTLER...")
    
def switch_rate(option):
    switcher={
        1: "Hourly",
        2: "Daily",
        3: "Weekly",
        4: "Monthly"
    }
    
    return switcher.get(option,"Invalid option was chosen, please enter an integer value from the list 1,2,3,4")
    

def get_weather_data_by_date(stations_df, chosen_option):
    
    try:
        
        weather_rate = switch_rate(chosen_option)
        chosen_weather_rate = stations_df.loc[stations_df['Intervals'].map(lambda x: weather_rate in x)]
        return chosen_weather_rate
    except:
        print("INVALID INPUT. ENTER A PANDAS DF FROM SOUPS AND AN INTEGER FROM THE LIST 1, 2, 3, 4")
        
       
################################################################################

# Call Environment Canada API
# Returns a dataframe of data
# UPDATE: October 4th 2018: Environment Canada API updated, 
#    we need to skip 15 rows instead of 16. `getHourlyData()` updated with skiprows=15
def getHourlyData(stationID, year, month):
    base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
    query_url = "format=csv&stationID={}&Year={}&Month={}&timeframe=1".format(stationID, year, month)
    api_endpoint = base_url + query_url
    return pd.read_csv(api_endpoint, skiprows=15)

def download_data_date_range(stationID,start_d,end_d):
    try:
        #stationID = 51442
        start_date = datetime.strptime(start_d, '%b%Y')
        end_date = datetime.strptime(end_d, '%b%Y')

        frames = []
        ran = [dt for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date)]
        ran_len = len(ran)
        for i in tnrange(ran_len, desc='Downloading Data'):    
            sleep(0.01)
            df = getHourlyData(stationID, ran[i].year, ran[i].month)
            frames.append(df)

        weather_data = pd.concat(frames)
        weather_data['Date/Time'] = pd.to_datetime(weather_data['Date/Time'])
        weather_data['Temp (°C)'] = pd.to_numeric(weather_data['Temp (°C)'])
        return weather_data
    
    except:
        print("INVALID INPUT. ENTER AN INTEGER FOR stationID, A STRING FOLLOWING THE FORMAT MonYEAR, i.e. Jun2015")
    