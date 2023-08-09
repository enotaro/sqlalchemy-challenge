# Import the dependencies.
import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)  

    # Create query
    one_year_from_last = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    precip_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_from_last).all()

    # Close session
    session.close()

     # Create a dictionary from the row data and append to a list of precip
    precip = []
    for date, prcp in precip_data:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip.append(precip_dict)

    return jsonify()

# stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)  
    
    # Create query
    station_data = session.query(Station.station, Station.name).all()

    # Close session
    session.close()

     # Create a dictionary from the row data and append to a list of all stations
    all_stations = []
    for station, name in station_data:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        all_stations.append(station_dict)
    
     return jsonify(all_stations)

# tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)   

    # Create query
    one_year_from_last = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    most_active_last_year = session.query(Measurement.tobs).\
                                        filter(Measurement.date >= one_year_from_last).\
                                        filter(Measurement.station == "USC00519281").\
                                        order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of data for most active station
    active_year = []
    for tobs in most_active_last_year:
        tobs_dict = {}
        tobs_dict["tobs"] = tobs
        active_year.append(tobs_dict)

    return jsonify(tobs_dict)

# start route
@app.route("/api/v1.0/<start>")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)   

    # Accept start date as a parameter from the URL
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    
    # Create query
    start_values = session.query(func.min(Measurement.tobs),
                            func.max(Measurement.tobs),
                            func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= start_date).all()

    # Close session
    session.close()

    all_values_start = []
    for start_min, start_max, start_avg in start_values:
        start_values_dict = {}
        start_values_dict["min"] = start_min
        start_values_dict["max"] = start_max
        start_values_dict["avg"] = start_avg
        all_values_start.append(start_values_dict)

    return jsonify(all_values_start)

# start/end route
@app.route("/api/v1.0/<start>/<end>")
def startend():
   # Create our session (link) from Python to the DB
    session = Session(engine)  

    # Accept start and end dates as parameters from the URL
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")

    # Create query
    start_end_values = session.query(func.min(Measurement.tobs),
                            func.max(Measurement.tobs),
                            func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= start_date and Measurement.date <= end_date).all()

    # Close session
    session.close()

    all_values_start_end = []
    for start_end_min, start_end_max, start_end_avg in start_end_values:
        start_end_values_dict = {}
        start_end_values_dict["min"] = start_end_min
        start_end_values_dict["max"] = start_end_max
        start_end_values_dict["avg"] = start_end_avg
        all_values_start_end.append(start__endvalues_dict)

    return jsonify(all_values_start_end)

if __name__ == '__main__':
    app.run(debug=True)
