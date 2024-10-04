import streamlit as st
import plotly.graph_objects as go
from utils import *

st.header("Level-off during descent")
st.write("Distance and time flown in level flight after Top of Descent.")
st.write("""
This KPI is intended to give an indication of the amount of level flight during the descent phase. Ideally, there should be no level flight during descents because level flight results in a higher fuel burn and possibly more noise. Ideally, aircraft should be able to descend from Top of Descent until touchdown.""")

airports_thailand = {
    "VTBS": "Suvarnabhumi Airport",
    "VTBD": "Don Mueang International Airport",
    "VTSP": "Phuket International Airport",
    "VTCC": "Chiang Mai International Airport",
    "VTSS": "Hat Yai International Airport",
    "VTUD": "Udon Thani International Airport"
}

st.subheader("Parameter selection")
col1,col2,col3 = st.columns(3)
with col1 :
    select_airport = st.selectbox("Select Airport by ICAO code",options =list(airports_thailand.keys()))
    slt_rad = st.slider("Select analysis radius (NM)",min_value=150,max_value=250,value=200,step=10)
with col2 :
    rocd_thrd = st.slider("Select Vertical speed limit (+-Ft/minute)",min_value= 0,max_value=1000,value=0,step=100)
    band = st.slider("Select Level band limit(Feet)",min_value= 150,max_value=300,value=200,step=10)

with col3 :
    min_lev_time = st.slider("Select Minimum level time(Sec)",min_value= 50,max_value=500,value=200,step=5)

    min_fl = st.slider("Select Minimum altitude(ft)",min_value= 1000,max_value=10000,value=2000,step=1000)
#excld_box_per =st.slider("Select analysis radius (NM)",min_value=150,max_value=250,value=200,step=10)
#excld_box_time = st.slider("Select analysis radius (NM)",min_value=150,max_value=250,value=200,step=10)

#df = pd.read_csv('../cat062_20240805_202408071426.csv')
df = get_mongo_df()
filtered_df = filter_df(df,select_airport,slt_rad )
fig = final_plot(filtered_df)
st.write("The analysis may take a few moments to load")
st.plotly_chart(fig,use_container_width=True)