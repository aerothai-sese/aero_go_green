import streamlit as st
import pandas as pd


st.set_page_config(
	page_title ="Vertical Flight Efficiency",
	page_icon="👋"

	)

st.header("Analysis of vertical flight efficiency.")

st.write("""
&nbsp;&nbsp;&nbsp;&nbsp;Flight efficiency KPIs measure the degree to which airspace users are offered the most efficient
trajectory on the day of operation. So far the focus of assessing trajectory-based flight efficiency
has been on horizontal measures in order to identify opportunities of ATM improvements in the
US and European system. Throughout the recent years the focus has shifted to address the
identification and measurement of ATM-related constraints on vertical flight profiles. In
particular, the analysis of fuel-efficient continuous descent operations has gained higher
momentum.
""", unsafe_allow_html=True)

st.write("""&nbsp;&nbsp;&nbsp;&nbsp;The underlying conceptual model of vertical flight operations is an abstraction of the flight
profile in distinct portions (i.e. segments). This profile is based on measured trajectory data (4D
position) of aircraft operations. A trajectory is therefore represented by the time-ordered set of
4D measurements associated to one flight, typically describing the flight path from the airport of
departure to the airport of destination (c.f. Figure 6-5). Based on the jointly agreed criteria for
describing level flight, the trajectory is mapped to level segments for further analysis. The
analysis focused on the arrival phase of a flight in terms of the top-of-descent within a 200NM
radius around the arrival airport.""")

st.image('./src/fig1_intro.png',caption="""Vertical Flight Profile : Level Segments [ 2015 Operational Performance: U.S./Europe ]""", use_column_width=True)
