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
@app.route('/')
def home():
    
    # there is some code here usually 
    
    return (f"welcome to my page <br/>"
            f"<br/>"
            f"available pages: <br/>"
            f"/api/v1.0/precipitation <br/>"
            f"/api/v1.0/stations <br/>"
            f"/api/v1.0/tobs <br/>"
            f"/api/v1.0/<start> <br/>"
            f"/api/v1.0/<start>/<end>"
            )
    
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

@app.route('/api/v1.0/stations')
def stat():
    stats = session.query(Station.station).all()
    session.close()
    stats = list(np.ravel(stats))
    return jsonify(stats)

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

@app.route('/api/v1.0/<start>')
def start():
    session = Session(engine)
    
    all_dates = session.query(Measure.date).order_by(Measure.date.desc()).all()
    start = all_dates[25]
    start = dt.date(2017, 8, 17)
    
    temps = session.query(func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)).filter(Measure.date >= start).all()
    

if __name__ == "__main__":
    app.run(debug=True)