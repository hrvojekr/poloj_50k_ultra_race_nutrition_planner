# Ultra Race Nutrition Planner

A simple, interactive Streamlit app to plan your nutrition for ultra races (50k, 100k, 6h, 12h).  

---

## Deployed Application

You can try the live app here: [Ultra Race Nutrition Planner](https://ultraracenutritionplanner.streamlit.app/)

---

Easily calculate and visualize your fluid, carbs, sodium, and calories intake per lap, and add custom notes for each lap.

---

## Features

- **Supports both distance and time-based races:** 50k, 100k, 6h, and 12h
- **Custom lap distance** (in meters)
- **Adjustable pace** (min/km and sec/km)
- **Set hourly intake goals** for:
  - Fluids (ml)
  - Carbs (g)
  - Sodium (mg)
  - Calories (kcal)
- **Editable per-lap notes** (enter what to eat/drink on each lap directly in the table)
- **Wide, user-friendly table** for easy planning and review

---

## Quick Start

1. **Clone this repo:**
    ```
    git clone https://github.com/<your-username>/<repo-name>.git
    cd <repo-name>
    ```

2. **Install dependencies:**
    ```
    pip install streamlit pandas
    ```

3. **Run the app:**
    ```
    streamlit run ultra_race_nutrition_planner.py
    ```

4. Open your browser to the provided local URL (usually [http://localhost:8501](http://localhost:8501)).

---

## How to Use

1. Set your race discipline (50k, 100k, 6h, or 12h) and lap distance.
2. Enter your expected pace and nutrition targets per hour.
3. The app calculates per-lap and cumulative nutrition needs.
4. Edit the **Notes** column in the table to add your planned food/drink for each lap.
5. Review your full race plan at a glance!

---

## Recommendations

- **Sodium:** 300–600 mg per hour
- **Calories:** ~300 kcal per hour
- **Carbs:** 60–90 g per hour
- Adjust these based on your personal needs and race conditions.

---

## License

MIT License

---

## Author

Created by Hrvoje Krpan 

---

**Feel free to open issues or submit pull requests for improvements!**
