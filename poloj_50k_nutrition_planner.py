import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


st.title("50k Ultra Poloj Race Nutrition Planner")


st.sidebar.header("User Inputs")
pace_min = st.sidebar.number_input("Pace (minutes per km)", min_value=1, max_value=10, value=4, step=1)
pace_sec = st.sidebar.number_input("Additional seconds per km", min_value=0, max_value=59, value=14, step=1)
fluid_per_hour_ml = st.sidebar.number_input("Fluid intake per hour (ml)", min_value=100, max_value=2000, value=500, step=1)
carbs_per_hour_g = st.sidebar.number_input("Carb intake per hour (g)", min_value=10, max_value=200, value=67, step=1)


pace_per_km = pace_min + (pace_sec / 60)

lap_distances_km = [1.5834] + [4.84166] * 10  
start_time = datetime(2025, 3, 1, 8, 0)  


total_time = 0  
cumulative_fluid = 0
cumulative_carbs = 0
data = []


for i, lap_dist in enumerate(lap_distances_km):
    lap_time = lap_dist * pace_per_km  
    total_time += lap_time  
    lap_timestamp = start_time + timedelta(minutes=total_time)  
    elapsed_time = timedelta(minutes=total_time)  

   
    elapsed_time_str = str(elapsed_time).split(".")[0]

    
    fluid_intake = fluid_per_hour_ml * (lap_time / 60) if i > 0 else 0
    carbs_intake = carbs_per_hour_g * (lap_time / 60) if i > 0 else 0
    
    cumulative_fluid += fluid_intake
    cumulative_carbs += carbs_intake
    
    data.append([
        i + 1,
        round(sum(lap_distances_km[: i + 1]), 2),
        elapsed_time_str,  
        lap_timestamp.strftime("%H:%M:%S"),
        round(fluid_intake, 1),
        round(cumulative_fluid, 1),
        round(carbs_intake, 1),
        round(cumulative_carbs, 1)
    ])


df = pd.DataFrame(data, columns=["Lap", "Total Distance (km)", "Elapsed Time", "Time", 
                                 "Fluid Intake (ml)", "Cumulative Fluid (ml)", 
                                 "Carbs Intake (g)", "Cumulative Carbs (g)"])

st.write("### Race Nutrition Plan")
st.dataframe(df)
