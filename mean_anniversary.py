import pandas as pd
from datetime import date, datetime
import math
from statistics import mean
from numpy import argmin


def calculate_mean_anniversary(days_of_interest: list):
    """Calculates the mean anniversary based on the geometric center
    for a list of dates of the current year given in the format yyyy-mm-dd.
    """

    # Get current year
    datetime_now = datetime.now()
    year = int(datetime_now.strftime('%Y'))

    # Transform days of interest in proper dates
    dates_of_interest = []
    for day in days_of_interest:
        dates_of_interest.append(datetime.strptime(day, '%Y-%m-%d'))

    # Get number of days in current year
    n_days_in_year = int(date(year, 12, 31).strftime('%j'))

    # Calculate position and angle for each day
    delta_phi = 360 / n_days_in_year
    date_position = pd.DataFrame(columns=['date', 'position_x', 'position_y', 'phi'], index=range(n_days_in_year))
    current_phi = 0.0
    for i in range(n_days_in_year):
        current_day_in_year = i + 1
        date_position.iloc[i]['date'] = datetime.strptime(str(year) + str(current_day_in_year), '%Y%j')
        date_position.iloc[i]['position_x'] = math.cos(math.radians(current_phi))
        date_position.iloc[i]['position_y'] = math.sin(math.radians(current_phi))
        date_position.iloc[i]['phi'] = current_phi
        current_phi += delta_phi

    # Extract the positions of the dates of interest
    date_position_of_interest = date_position[date_position['date'].isin(dates_of_interest)]

    # Determine the geometric center
    geometric_center = [mean(date_position_of_interest['position_x']), mean(date_position_of_interest['position_y'])]

    # Handle special case
    if geometric_center == [0, 0]:
        return 'No unique solution found.'

    # Calculate the angle of the geometric center
    phi_geometric_center = None
    if geometric_center[0] > 0 and geometric_center[1] > 0:
        # Quadrant 1
        phi_geometric_center = math.degrees(math.atan(geometric_center[1] / geometric_center[0]))
    elif geometric_center[0] < 0 and geometric_center[1] > 0:
        # Quadrant 2
        phi_geometric_center = math.degrees(math.atan(geometric_center[1] / geometric_center[0])) + 180
    elif geometric_center[0] < 0 and geometric_center[1] < 0:
        # Quadrant 3
        phi_geometric_center = math.degrees(math.atan(geometric_center[1] / geometric_center[0])) + 180
    elif geometric_center[0] > 0 and geometric_center[1] < 0:
        # Quadrant 4
        phi_geometric_center = math.degrees(math.atan(geometric_center[1] / geometric_center[0])) + 360
    elif geometric_center[0] > 0 and geometric_center[1] == 0:
        phi_geometric_center = 0.0
    elif geometric_center[0] == 0 and geometric_center[1] > 0:
        phi_geometric_center = 90.0
    elif geometric_center[0] < 0 and geometric_center[1] == 0:
        phi_geometric_center = 180.0
    elif geometric_center[0] == 0 and geometric_center[1] < 0:
        phi_geometric_center = 270.0

    # Define the mean anniversary as the date with the closest angle to the angle of the geometric center
    mean_anniversary = date_position.iloc[argmin(abs(date_position['phi'] - phi_geometric_center))]['date']

    return mean_anniversary.date()
