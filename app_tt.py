#IMPORT DEPENDANCIES
# Python SQL toolkits and Object Relational Mapper's
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, select

import numpy as np
#import pandas as pd

import datetime as dt
from datetime import datetime, timedelta

# Import Flask
from flask import Flask, jsonify

# Setup the Database
# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a base using automap_base
Base = automap_base()
# Reflect an existing database into a new model &
# reflect the tables
Base.prepare(engine,reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Create an app (Flask)
app = Flask(__name__)

# Create the FLask Routes
# List all routes that are available from the requirements
#Create the opening route / page
@app.route("/")
def homepage():
    
    return(
        f"Welcome to the Climate App!<br/>"
        f"I have never been to Hawaii, but I am sure it is awesome - hopefully the Climate App helps you decide when to go. <br/>"
        f"<br/>"
        f"The available pages are:<br/>"
        
        f"/api/v1.0/precipitation<br/>"
        f"Convert the query dates & temperature for the last year. <br/>"
        f"<br/>"

        f"/api/v1.0/stations<br/>"
        f"Return a JSON list of stations from the dataset. <br/>"
        f"<br/>"

        f"/api/v1.0/tobs<br/>"
        f"Query the dates and temperature observations of the most active station for the last year of data. <br/>"
        f"<br/>"

        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"- Returns an Aveage Max, and Min temperature for given period.<br/>"
        f"<br/>"

        f"Note that the data set is only from 01/01/2010 to 23/08/2017 so climate change in the last 3 years may have changed the best time to go.<br/>"
    )

# Create the rainfall / precipitation route / page from the previous year

@app.route("/api/v1.0/precipitation")
def precipitation():
    ytd = timedelta(days=365)
    year_ago = dt.date(2017, 8, 23) - ytd
    year_rain = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= year_ago).order_by(Measurement.date.desc()).all()
    
    #create the JSON objects
    rainfall_list = [year_rain]
    return jsonify(rainfall_list)

# Create a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    act_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()

    #create the JSON objects
    stations_list = [act_station]
    return jsonify(stations_list)

# Create a JSON list of the temperatures from the station that has the most readings for the last year

@app.route("/api/v1.0/tobs")
def tobs():
    last_year_obs = []
    station_highest = session.query(funct.count())
    observations = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()
    
    
    last_year_obs = list(np.ravel(observations))
    return jsonify(last_year_obs)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

@app.route("/api/v1.0/yyyy-mm-dd/yyyy-mm-dd")

if __name__ == "__main__":
    app.run(debug=True)