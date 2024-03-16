# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd


#################################################
# Database Setup
#################################################
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

database_path = "../Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
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
@app.route('/')

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! </br>
    Available Routes: <br/>
    <ol>
    <li>/api/v1.0/precipitation <br/>
    <li>/api/v1.0/stations <br/>
    <li>/api/v1.0/tobs <br/>
    <li>/api/v1.0/temp/start/end <br/>
    ''')

# Define precipitation route
@app.route('/api/v1.0/precipitation')

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Define stations route
@app.route('/api/v1.0/stations')

def stations():
    result_station = session.query(Station.station).all()
    stations = list(np.ravel(result_station))
    return jsonify(stations)

# Define monthly temperature route
@app.route('/api/v1.0/tobs')

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temp_results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    temps = list(np.ravel(temp_results))
    
    return jsonify(temps)

# Define statistics route
@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results_sel = session.query(*sel).\
        filter(Measurement.date <= start).all()
        temps = list(np.ravel(results_sel))
        return jsonify(temps)
    
    results_sel = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results_sel))
    return jsonify(temps)

# http://127.0.0.1:5000/