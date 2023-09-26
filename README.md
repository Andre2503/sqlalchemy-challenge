# SQLAlchemy Challenge: Surfs Up!

Welcome to my Module 10 Challenge project, part of my Data Analytics Bootcamp. This repository contains an analysis of climate data using Python, SQLAlchemy, Pandas, and Matplotlib, along with a Flask API designed to serve the results.

## Repository Contents

- `SurfsUp`: A folder containing:
  - Jupyter notebook with detailed climate analysis.
  - `app.py` document that powers the Flask API for the climate app.
- `resources`: Contains the `hawaii.sqlite` database used for this challenge.

## Part 1: Analyse and Explore the Climate Data

### Key Steps:

1. Connected to the SQLite database using SQLAlchemy's `create_engine()`.
2. Reflected the tables into classes and saved references to `station` and `measurement` using `automap_base()`.
3. Linked Python to the database with a SQLAlchemy session. 

### Precipitation Analysis:

- Determined the most recent date in the dataset.
- Retrieved the previous 12 months of precipitation data.
- Loaded the data into a Pandas DataFrame and sorted it by date.
- Plotted the results.
- Printed the summary statistics for the precipitation data.

### Station Analysis:

- Calculated the total number of stations.
- Listed the most active stations in descending order.
- Identified the station with the greatest number of observations.
- Calculated the lowest, highest, and average temperatures for the most active station.
- Retrieved and plotted the previous 12 months of TOBS data for the most active station.

## Part 2: Designing a Climate App

Implemented a Flask API based on the previous analyses. Routes are:

- `/`: Home route, lists all available routes.
- `/api/v1.0/precipitation`: Returns a dictionary with dates as keys and precipitation as values in JSON format.
- `/api/v1.0/stations`: Returns a JSON list of all stations from the dataset.
- `/api/v1.0/tobs`: Provides a JSON list of temperature observations of the most active station for the previous year.
- `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`: Returns a JSON dictionary of the minimum, average, and maximum temperatures for a specified date range.

## Instructions to Run:

1. For the analysis, navigate to the `SurfsUp` folder and open the Jupyter notebook. Run the notebook.
2. For the Flask app, in the `SurfsUp` folder, run the `app.py` document and access the endpoints using a browser or API client.
