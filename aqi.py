def calculate_aqi_pm25(pm25):
    """
    Calculate Indian AQI contribution from PM2.5.
    """

    if pm25 <= 30:
        return pm25 * 50 / 30

    elif pm25 <= 60:
        return 50 + (pm25 - 30) * 50 / 30

    elif pm25 <= 90:
        return 100 + (pm25 - 60) * 100 / 30

    elif pm25 <= 120:
        return 200 + (pm25 - 90) * 100 / 30

    elif pm25 <= 250:
        return 300 + (pm25 - 120) * 100 / 130

    else:
        return 400


def get_aqi_category(aqi):

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Satisfactory"

    elif aqi <= 200:
        return "Moderate"

    elif aqi <= 300:
        return "Poor"

    elif aqi <= 400:
        return "Very Poor"

    else:
        return "Severe"