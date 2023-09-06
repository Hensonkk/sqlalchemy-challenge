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


if __name__ == "__main__":
    app.run(debug=True)