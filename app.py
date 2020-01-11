import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################



@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/startend"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    end_date = '2017-08-23'
    new_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
    
    # Perform a query to retrieve the data and precipitation scores
    last_date_year = new_date - dt.timedelta(days=365)
    start_date = last_date_year.strftime("%Y-%m-%d")
    
    dates = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date>=start_date).\
    filter(Measurement.date<=end_date).\
    order_by(Measurement.date)

    precip = {date: p for date, p in dates}

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()

    stations = []
    for station in results:
        station = results[0]
        stations.append(station)
   
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    end_date = '2017-08-23'
    new_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
    
    last_date_year = new_date - dt.timedelta(days=365)
    start_date = last_date_year.strftime("%Y-%m-%d")

    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date>=start_date).\
    filter(Measurement.date<=end_date).\
    order_by(Measurement.date)

    tobs = {tob: t for tob, t in results}

    return jsonify(tobs)

@app.route("/api/v1.0/start")
def start():

    end_date = '2017-08-23'
    new_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
    
    last_date_year = new_date - dt.timedelta(days=365)
    start_date = last_date_year.strftime("%Y-%m-%d")

    TMIN = session.query(func.min(Measurement.tobs)).\
           filter(Measurement.date == start_date).all()
    
    TMAX = session.query(func.max(Measurement.tobs)).\
           filter(Measurement.date == start_date).all()

    TAVG = session.query(func.avg(Measurement.tobs)).\
           filter(Measurement.date == start_date).all()
    
    results = [TMIN, TMAX, TAVG]
    return jsonify(results)

@app.route("/api/v1.0/startend")
def startend():
    end_date = '2017-08-23'
    new_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
    
    last_date_year = new_date - dt.timedelta(days=365)
    start_date = last_date_year.strftime("%Y-%m-%d")

    TMIN = session.query(func.min(Measurement.tobs)).\
           filter(Measurement.date.between(start_date, end_date)).all()
    
    TMAX = session.query(func.max(Measurement.tobs)).\
            filter(Measurement.date.between(start_date, end_date)).all()
    TAVG = session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date.between(start_date, end_date)).all()    
    
    results = [TMIN, TMAX, TAVG]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)