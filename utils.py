import pandas as pd
import math
import numpy as np
import plotly.graph_objects as go
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def get_mongo_df():
    uri = "mongodb+srv://art_sese_fi_2023:art_sese_fi_2023@cluster0.xpbbr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    db = client['vfe']  # Replace with your database name
    collection = db['cat62_vfe']  # Replace with your collection name
    data = list(collection.find())  # Get all documents from the collection
    df = pd.DataFrame(data)  
    return df

def filter_df(df,select_airport,slt_rad ):
	filtered_df = df[np.sqrt((df['calculated_x'])**2 + (df['calculated_y'])**2) <= 1852*slt_rad]
	filtered_df = filtered_df[filtered_df['dest']==select_airport]
	filtered_df['time_of_track'] = pd.to_datetime(filtered_df['time_of_track'])
	filtered_df = filtered_df.sort_values(by='time_of_track')
	return filtered_df

def get_all_flight(filtered_df):
	return filtered_df['acid'].unique()

def get_toc_df(lst,lower_th,higher_th):
    current_count = 0
    last_zero_index = -1

    for i, num in enumerate(lst):
        if num == 0:
            current_count += 1
            last_zero_index = i  # Update the last zero index
        else:
            if lower_th < current_count < higher_th:
                return last_zero_index  # Return the last zero index if the count is within range
            current_count = 0  # Reset the count if sequence breaks

    # Check if the last sequence of zeros had the required length range
    if lower_th < current_count < higher_th:
        return last_zero_index

    return None  # Return None if no sequence of zeros is found within the range


def get_toc_df(lst, lower_th, higher_th):
    current_count = 0
    last_zero_index = None  # Track the last valid zero index
    
    for i, num in enumerate(lst):
        if num == 0:
            current_count += 1
        else:
            # If the count of consecutive zeros is within the threshold range
            if lower_th < current_count < higher_th:
                last_zero_index = i - 1  # Update the latest valid sequence index
            current_count = 0  # Reset the count for the next sequence

    # Check the last sequence of zeros at the end of the list
    if lower_th < current_count < higher_th:
        last_zero_index = len(lst) - 1  # If valid, set the last index of the sequence

    return last_zero_index  # Return the latest valid zero index or None

def check_straight_zero_occurrence(lst, x, y):
    current_count = 0
    start_index = -1

    for i, num in enumerate(lst):
        if num == 0:
            if current_count == 0:
                start_index = i  # Mark the start of the zero sequence
            current_count += 1
        else:
            if x < current_count < y:
                return (start_index, i - 1)  # Return the first matching sequence
            current_count = 0
            start_index = -1

    # Check for the last sequence of zeros at the end of the list
    if x < current_count < y:
        return (start_index, len(lst) - 1)

    return 0,0 # Return None if no matching sequence is found

def get_lev_off_idx(df_flight,lower_th,higher_th):
    rocd_list = list(df_flight['rate_cd'])
    start_idx,end_idx = check_straight_zero_occurrence(list(df_flight['rate_cd']),lower_th,higher_th)
    if start_idx and end_idx :
        return start_idx,end_idx
    else : return 0,0

def down_sampling(lst, n):
    length = len(lst)
    if n >= length:
        return lst  # Return the whole list if n is greater than or equal to the list length
    k = length // n  # Dynamically calculate interval
    return lst[::k][:n]

def filter_geo(lst, n):
    for i, item in enumerate(lst):
        if item < n:
            return i,lst[i:]  # Slice the list starting from the first item greater than n
    return -1,[]  # Return an empty list if no item is greater than n


 # get df top of climb
def get_df_airborne(sba_df,track):
    rocd = list(sba_df[(sba_df['track_no']==track)&(sba_df['dist_from_last_position']==0)]['rate_cd'])
    start_df = get_toc_df(rocd,100,1000)
    geo_alt = list(sba_df[(sba_df['track_no']==track)&(sba_df['dist_from_last_position']==0)]['geo_alt'])
    #end_df = 
    if start_df != None:
        return sba_df[(sba_df['track_no']==track)&(sba_df['dist_from_last_position']==0)].iloc[start_df -100:]
    else :
        return pd.DataFrame()

def plot_alt(fig,df_flight):
    flight = df_flight.iloc[0]['acid']
    geo_track = df_flight['geo_alt']
    fig.add_trace(go.Scatter(x=np.arange(len(geo_track)), y=geo_track,
                mode='lines',
                name='markers',text=flight,line=dict(width=0.2, color='gray'),
                showlegend=False))

    
    return None

def get_dist(df_flight,lev_start,lev_end):
    x1,y1 = df_flight.iloc[lev_end]['calculated_x'] ,df_flight.iloc[lev_end]['calculated_y']
    x2,y2 = df_flight.iloc[lev_start]['calculated_x'] ,df_flight.iloc[lev_start]['calculated_y']
    
    return math.sqrt((x1 -x2)**2 + (y1 -y2)**2)

def round_timedelta(td):
    """Round Timedelta to the nearest minute. Round up if seconds > 30."""
    total_seconds = td.total_seconds()
    minutes, seconds = divmod(total_seconds, 60)
    
    if seconds > 30:
        minutes += 1  # Round up if seconds > 30
    
    # Return rounded Timedelta
    return int(minutes)

def final_plot(filtered_df):
	fig = go.Figure()
	time_list,dis_list = [],[]
	flights = filtered_df['acid'].unique()
	for flight in flights:
	    df_1 = filtered_df[filtered_df['acid']==flight]
	    tracks = df_1['track_no'].unique()
	    for track in tracks:
	        df_flight = get_df_airborne(df_1,track)

	        if len(df_flight !=0 ) :
	            lev_start,lev_end = get_lev_off_idx(df_flight,5,30)

	            tm = df_flight.iloc[lev_end]['time_of_track'] - df_flight.iloc[lev_start]['time_of_track']
	            dist = get_dist(df_flight,lev_start,lev_end)
	            dis_list.append(dist)
	            time_list.append(tm)

	            plot_alt(fig,df_flight)

	seconds = [td.total_seconds() for td in time_list]
	mean_seconds = sum(seconds) / len(seconds)

	sum(dis_list)/len(dis_list)

	fig.update_layout(width=800,  # Set the width
	    height=800,
	    title={'text':'<b>Descending over time of VTBS<b>','x':0.5,'xanchor':'center'},
	    xaxis_title='<b>N Time step<b>',
	    yaxis_title='<b>Geometric Altitude(ft.)</b>',
	    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
	    font=dict(
	        family="Courier New, monospace",  # Monospace font
	        size=14,                          # Font size
	        color="black"             # Font color
	    )
	)
	return fig

def map_plot():
    return 