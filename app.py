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

# Create a database session object
session = Session(engine)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year_precip = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= year_ago).all() 
    session.close() 
    return jsonify(last_year_precip)

@app.route("/api/v1.0/stations")
def stations():
    active_station = session.query(Measurements.station, func.count(Measurements.station)).group_by(Measurements.station).\
    order_by(func.count(Measurements.station).desc()).all()
    all_stations = []
    for station, count in results:
        all_stations = {}
        all_stations["station"] = station
        all_stations["count"] = count
        all_stations.append(all_stations)
    session.close() 
    return jsonify(active_station)
    
@app.route("/api/v1.0/tobs")
def temps():
    lowest_temp = session.query(Measurements.station, func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).\
                            filter(Measurements.station == "USC00519281").all()
    session.close() 
    return jsonify(lowest_temp)

@app.route("/api/v1.0/start")
def start():
    #Design a query that lists the min/max/avg totals for each station 
    sel = [Measurements.station, 
       func.min(Measurements.tobs), 
       func.max(Measurements.tobs), 
       func.avg(Measurements.tobs)]
       
    start = session.query(*sel).\
        group_by(Measurements.station).\
        order_by(Measurements.station).all()
    session.close()  
    return jsonify(start) 

# @app.route("/api/v1.0/start/end")
# def end():
    #Design a query that lists the min/max/avg totals for each station 
    # sel = [Measurements.station, 
    #    func.min(Measurements.tobs), 
    #    func.max(Measurements.tobs), 
    #    func.avg(Measurements.tobs)]
       
    # start = session.query(*sel).\
    #     group_by(Measurements.station).\
    #     order_by(Measurements.station).all()
    # session.close()  
    # return jsonify(start) 




if __name__ == '__main__':
    app.run(debug=True)
