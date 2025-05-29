import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

st.title("Ultra Race Nutrition Planner")

st.sidebar.header("User Inputs")

discipline = st.sidebar.selectbox(
    "Race discipline",
    options=["50k", "100k", "6h", "12h"],
    index=0
)

lap_distance_m = st.sidebar.number_input(
    "Lap distance (meters)", min_value=100, max_value=10000, value=4842, step=1
)
lap_distance_km = lap_distance_m / 1000

start_time = st.sidebar.time_input(
    "Race start time", value=datetime(2025, 3, 1, 8, 0).time()
)
start_datetime = datetime.combine(datetime.today(), start_time)

pace_min = st.sidebar.number_input(
    "Pace (minutes per km)", min_value=1, max_value=10, value=4, step=1
)
pace_sec = st.sidebar.number_input(
    "Additional seconds per km", min_value=0, max_value=59, value=14, step=1
)
fluid_per_hour_ml = st.sidebar.number_input(
    "Fluid intake per hour (ml)", min_value=100, max_value=2000, value=500, step=1
)
carbs_per_hour_g = st.sidebar.number_input(
    "Carb intake per hour (g)", min_value=10, max_value=200, value=67, step=1
)
sodium_per_hour_mg = st.sidebar.number_input(
    "Sodium intake per hour (mg)", min_value=100, max_value=2000, value=400, step=1,
    help="Recommended: 300–600 mg per hour"
)
calories_per_hour_kcal = st.sidebar.number_input(
    "Calories intake per hour (kcal)", min_value=100, max_value=2000, value=300, step=10,
    help="Recommended: around 300 kcal per hour"
)

pace_per_km = pace_min + (pace_sec / 60)
lap_time_min = lap_distance_km * pace_per_km  # Time per full lap

lap_distances_km = []
total_time = 0

if discipline in ["50k", "100k"]:
    target_distance = 50 if discipline == "50k" else 100
    full_laps = int(target_distance // lap_distance_km)
    remaining_distance = target_distance - (full_laps * lap_distance_km)
    
    lap_distances_km = [lap_distance_km] * full_laps
    if remaining_distance > 0.001:
        lap_distances_km.append(remaining_distance)
        
elif discipline in ["6h", "12h"]:
    target_minutes = 6*60 if discipline == "6h" else 12*60
    full_laps = int(target_minutes // lap_time_min)
    remaining_time = target_minutes - (full_laps * lap_time_min)
    
    lap_distances_km = [lap_distance_km] * full_laps
    if remaining_time > 0.1:
        # Add partial lap for remaining time
        partial_distance = (remaining_time / pace_per_km)
        lap_distances_km.append(partial_distance)

cumulative_fluid = 0
cumulative_carbs = 0
cumulative_sodium = 0
cumulative_calories = 0
data = []
total_distance = 0

for i, lap_dist in enumerate(lap_distances_km):
    lap_time = lap_dist * pace_per_km  
    total_time += lap_time  
    lap_timestamp = start_datetime + timedelta(minutes=total_time)
    elapsed_time = timedelta(minutes=total_time)  
    
    total_distance += lap_dist
    elapsed_time_str = str(elapsed_time).split(".")[0]
    
    # Nutrition calculation (prorated for partial laps)
    fluid_intake = fluid_per_hour_ml * (lap_time / 60) if i > 0 else 0
    carbs_intake = carbs_per_hour_g * (lap_time / 60) if i > 0 else 0
    sodium_intake = sodium_per_hour_mg * (lap_time / 60) if i > 0 else 0
    calories_intake = calories_per_hour_kcal * (lap_time / 60) if i > 0 else 0
    
    cumulative_fluid += fluid_intake
    cumulative_carbs += carbs_intake
    cumulative_sodium += sodium_intake
    cumulative_calories += calories_intake

    data.append([
        i + 1,
        round(total_distance, 2),
        elapsed_time_str,  
        lap_timestamp.strftime("%H:%M:%S"),
        round(fluid_intake, 1),
        round(cumulative_fluid, 1),
        round(carbs_intake, 1),
        round(cumulative_carbs, 1),
        round(sodium_intake, 1),
        round(cumulative_sodium, 1),
        round(calories_intake, 1),
        round(cumulative_calories, 1),
        ""  # Empty notes field for user input
    ])

# Force exact time for time-based disciplines
if discipline in ["6h", "12h"]:
    total_time = 6*60 if discipline == "6h" else 12*60
    final_time_str = "06:00:00" if discipline == "6h" else "12:00:00"
    data[-1][3] = final_time_str  # Update final timestamp

df = pd.DataFrame(data, columns=[
    "Lap", "Total Distance (km)", "Elapsed Time", "Time", 
    "Fluid Intake (ml)", "Cumulative Fluid (ml)", 
    "Carbs Intake (g)", "Cumulative Carbs (g)",
    "Sodium Intake (mg)", "Cumulative Sodium (mg)",
    "Calories Intake (kcal)", "Cumulative Calories (kcal)",
    "Notes"
])

st.write("### Race Nutrition Plan (edit your Notes directly below)")
edited_df = st.data_editor(
    df,
    column_config={
        "Notes": st.column_config.TextColumn("Notes (what to eat/drink)")
    },
    num_rows="fixed",
    use_container_width=True  # This ensures the table uses all available width
)

st.write(f"### Total Race Time: {timedelta(minutes=total_time)}")
st.write(f"### Total Distance: {round(total_distance, 2)} km")

st.write("""
### Key Notes:
- **Time-based races (6h/12h):** Final lap shows partial distance covered in remaining time
- **Distance-based races:** May include a partial final lap to reach exact distance
- **First lap:** No nutrition intake (assumed starting with full supplies)
- **Sodium recommendation:** 300–600 mg per hour (you can adjust as needed)
- **Calories recommendation:** around 300 kcal per hour (you can adjust as needed)
- **Notes:** Add your planned food or drink for each lap directly in the table!
""")
