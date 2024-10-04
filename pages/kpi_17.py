import streamlit as st
import pandas as pd
import numpy as np
from utils import *

#df = pd.read_csv('../../cat062_20240805_202408071426.csv')


airport = []
st.write("KPI 17 : Level-off during climb")
st.write("Definition : Distance and time flown in level flight before Top of Climb.")
st.write("""**Variant 1**: Average distance flown in level flight before Top of Climb \n
**Variant 2**: Average time flown in level flight before Top of Climb""")


values = st.slider("**Select times invter of 0 rate of climb.**",min_value=0,max_value= 40,value= (10, 30),step=1)
st.write("Values:", values[0])
