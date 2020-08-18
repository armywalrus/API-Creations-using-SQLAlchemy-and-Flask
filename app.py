import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurement
Stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
session = Session(engine)
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year_precip = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= year_ago).all()  
    return jsonify(last_year_precip)

    # @app.route("/api/v1.0/stations<br")
    # def stations():


    # @app.route("/api/v1.0/tobs")
    # def temps():


    # @app.route("/api/v1.0/<start>")
    # def start():


    # @app.route("/api/v1.0/<start>/<end>")
    # def end():
if __name__ == '__main__':
    app.run(debug=True)
