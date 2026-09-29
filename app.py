import streamlit as st
import time
from aqi import calculate_aqi_pm25, get_aqi_category

st.set_page_config(
    page_title="AQI Detection & Exposure Monitoring",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------

if "monitoring" not in st.session_state:
    st.session_state.monitoring = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None


# -----------------------------
# AUTOMATIC RECOMMENDATIONS
# -----------------------------

def get_recommendations(category, exposure_risk):

    if category == "Good":
        return [
            "Air quality is generally satisfactory.",
            "Normal outdoor activities can be continued.",
            "Continue monitoring air quality periodically."
        ]

    elif category == "Satisfactory":
        return [
            "Air quality is acceptable for most people.",
            "Sensitive individuals should monitor symptoms.",
            "Consider reducing prolonged outdoor activity if discomfort occurs."
        ]

    elif category == "Moderate":
        return [
            "Reduce prolonged or strenuous outdoor activity.",
            "Sensitive individuals should consider limiting outdoor exposure.",
            "Monitor air quality before extended outdoor activities."
        ]

    elif category == "Poor":
        return [
            "Reduce unnecessary outdoor exposure.",
            "Avoid prolonged or strenuous outdoor exercise.",
            "Sensitive individuals should take additional precautions.",
            "Consider using appropriate respiratory protection when recommended."
        ]

    elif category == "Very Poor":
        return [
            "Avoid prolonged outdoor exposure where possible.",
            "Avoid strenuous outdoor exercise.",
            "Keep indoor spaces appropriately protected from outdoor pollution.",
            "Follow local air-quality and health guidance."
        ]

    else:
        return [
            "Minimize outdoor exposure.",
            "Avoid strenuous outdoor activities.",
            "Stay indoors where practical and reduce indoor pollution sources.",
            "Follow local health guidance and official air-quality alerts."
        ]


# -----------------------------
# TITLE
# -----------------------------

st.title("🌍 AQI Detection, Exposure Monitoring & Alert System")

st.write(
    "Software prototype for real-time air-quality monitoring, "
    "exposure tracking and health-risk alerts."
)

st.info(
    "Prototype Mode: Sensor values are currently simulated. "
    "ESP32 hardware integration will be added in the next phase."
)


# -----------------------------
# SENSOR INPUTS
# -----------------------------

st.subheader("🌡️ Simulated Sensor Data")

col1, col2 = st.columns(2)

with col1:

    pm25 = st.slider(
        "PM2.5 (µg/m³)",
        min_value=0,
        max_value=300,
        value=92
    )

    pm10 = st.slider(
        "PM10 (µg/m³)",
        min_value=0,
        max_value=500,
        value=140
    )

with col2:

    temperature = st.slider(
        "Temperature (°C)",
        min_value=0,
        max_value=50,
        value=29
    )

    humidity = st.slider(
        "Humidity (%)",
        min_value=0,
        max_value=100,
        value=68
    )


# -----------------------------
# AQI CALCULATION
# -----------------------------

aqi = calculate_aqi_pm25(pm25)

category = get_aqi_category(aqi)


# -----------------------------
# AQI DISPLAY
# -----------------------------

st.subheader("📊 Current Air Quality")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "AQI",
    f"{aqi:.0f}"
)

col2.metric(
    "PM2.5",
    f"{pm25} µg/m³"
)

col3.metric(
    "PM10",
    f"{pm10} µg/m³"
)

col4.metric(
    "Temperature",
    f"{temperature} °C"
)

st.metric(
    "Humidity",
    f"{humidity}%"
)

st.write(
    f"### Air Quality Category: **{category}**"
)


# -----------------------------
# AIR QUALITY WARNING
# -----------------------------

if category == "Good":

    st.success(
        "🟢 GOOD — Air quality is satisfactory."
    )

elif category == "Satisfactory":

    st.success(
        "🟢 SATISFACTORY — Air quality is acceptable."
    )

elif category == "Moderate":

    st.warning(
        "🟡 MODERATE — Sensitive individuals should take precautions."
    )

elif category == "Poor":

    st.warning(
        "🟠 POOR — Reduce prolonged outdoor exposure."
    )

elif category == "Very Poor":

    st.error(
        "🔴 VERY POOR — Avoid prolonged outdoor exposure."
    )

else:

    st.error(
        "🚨 SEVERE — Minimize outdoor exposure and follow local health guidance."
    )


# -----------------------------
# EXPOSURE MONITORING
# -----------------------------

st.divider()

st.subheader("⏱️ Exposure Monitoring")

if not st.session_state.monitoring:

    st.write(
        "Start monitoring to record the user's exposure duration."
    )

    if st.button("▶️ Start Exposure Monitoring"):

        st.session_state.monitoring = True
        st.session_state.start_time = time.time()

        st.rerun()

else:

    elapsed_seconds = time.time() - st.session_state.start_time

    elapsed_minutes = int(elapsed_seconds // 60)

    elapsed_seconds_display = int(elapsed_seconds % 60)

    st.metric(
        "Current Exposure Time",
        f"{elapsed_minutes} min {elapsed_seconds_display} sec"
    )

    # -----------------------------
    # EXPOSURE RISK
    # -----------------------------

    if category in ["Good", "Satisfactory"]:

        exposure_risk = "LOW"

    elif category == "Moderate":

        exposure_risk = "MODERATE"

    elif category == "Poor":

        exposure_risk = "HIGH"

    else:

        exposure_risk = "VERY HIGH"


    st.write(
        f"### Exposure Risk: **{exposure_risk}**"
    )


    # -----------------------------
    # EXPOSURE WARNING
    # -----------------------------

    if exposure_risk == "LOW":

        st.success(
            "Current exposure-risk estimate is low."
        )

    elif exposure_risk == "MODERATE":

        st.warning(
            "Consider reducing prolonged exposure."
        )

    elif exposure_risk == "HIGH":

        st.warning(
            "⚠️ High exposure-risk estimate. "
            "Reduce unnecessary outdoor exposure."
        )

    else:

        st.error(
            "🚨 Very high exposure-risk estimate. "
            "Minimize exposure and follow local health guidance."
        )


    # -----------------------------
    # AUTOMATIC RECOMMENDATIONS
    # -----------------------------

    st.divider()

    st.subheader("💡 Automatic Health Precautions")

    recommendations = get_recommendations(
        category,
        exposure_risk
    )

    for recommendation in recommendations:

        st.write(f"• {recommendation}")


    # -----------------------------
    # STOP MONITORING
    # -----------------------------

    if st.button("⏹️ Stop Monitoring"):

        st.session_state.monitoring = False
        st.session_state.start_time = None

        st.rerun()


    # -----------------------------
    # REFRESH TIMER
    # -----------------------------

    time.sleep(1)

    st.rerun()