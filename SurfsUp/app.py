# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measure = Base.classes.measurement
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

# created a route to display my initial homepage
@app.route('/')
def home():
    
    #Setup initial page on website
    
    return (f"welcome to my page <br/>"
            f"<br/>"
            f"available pages: <br/>"
            f"/api/v1.0/precipitation <br/>"
            f"/api/v1.0/stations <br/>"
            f"/api/v1.0/tobs <br/>"
            f"/api/v1.0/<start> <br/>"
            f"/api/v1.0/<start>/<end>"
            )
    
# created a route to display precipitation data for whole year from most recent date
@app.route('/api/v1.0/precipitation')
def prcp():
    most_recent_date = dt.date(2017, 8, 23)
    year_ago = most_recent_date - dt.timedelta(days = 365)
    prcp = session.query(Measure.date, Measure.prcp).filter(Measure.date >= year_ago).all()

    prcp_dict = {}
    for x in prcp:
        date, precip = x
        prcp_dict[date] = precip   
    return jsonify(prcp_dict)


# created a route to display a list of all the stations
@app.route('/api/v1.0/stations')
def stat():
    stats = session.query(Station.station).all()
    session.close()
    stats = list(np.ravel(stats))
    return jsonify(stats)


# created a route to display the temperatures over the course of a year for the most active station
@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    
    most_recent_date = session.query(Measure.date).order_by(Measure.date.desc()).first()

    most_recent_date = dt.date(2017, 8, 23)

    year_ago = most_recent_date - dt.timedelta(days = 365)

    station_obs_count = session.query(Measure.station, func.count(Measure.station)).\
                    group_by(Measure.station).\
                    order_by(func.count(Measure.station).desc())

    most_active = station_obs_count[0][0]
    temp_dates_ma = session.query(Measure.date, Measure.tobs).filter(Measure.date >= year_ago, Measure.station == "USC00519281").all()
    session.close()
    temp_dates_ma = list(np.ravel(temp_dates_ma))
    return jsonify(temp_dates_ma)

# created a route and function that allows the user to input a start and end date to access the minimum temp, max temp, and avg temp for user inputs
@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def stats(start=None, end=None):
    sel = [func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measure.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measure.date >= start).\
        filter(Measure.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)