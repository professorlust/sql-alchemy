import numpy as np

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

# Save reference to the tables
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
        f"/api/v1.0/stations</a><br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of date and rain"""
    # Query all Measurement
    results = session.query(Measurement).all()

    # Create a dictionary from the row data and append to a list of all_rain
    all_rain = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict["date"] = measurement.date
        measurement_dict["prcp"] = measurement.prcp
        all_rain.append(measurement_dict)

    return jsonify(all_rain)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all Stations
    results2 = session.query(Station).all()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station in results2:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)
    
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of tobs"""
    # Query all Measurements (last year)
    results3 = session.query(Measurement).filter(Measurement.date > '2016-08-23').all()

    # Create a dictionary from the row data and append to a list of all_temps
    all_temps = []
    for temps in results3:
        temps_dict = {}
        temps_dict["date"] = temps.date
        temps_dict["tobs"] = temps.tobs
        all_temps.append(temps_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/start")
def start():
    """Return a list of measurements from start"""
    # Query all Measurements from start
    results4 = session.query(Measurement.date, func.max(Measurement.tobs).label("max"), func.min(Measurement.tobs).label("min"), func.avg(Measurement.tobs).label("avg")).group_by(Measurement.date).filter(Measurement.date >= '2016-08-23').all()

    # Create a dictionary from the row data and append to a list of all_temps
    all_tempstart = []
    for tempstart in results4:
        tempstart_dict = {}
        tempstart_dict["date"] = tempstart.date
        tempstart_dict["maxtobs"] = tempstart.max
        tempstart_dict["mintobs"] = tempstart.min
        tempstart_dict["avgtobs"] = tempstart.avg
        all_tempstart.append(tempstart_dict)

    return jsonify(all_tempstart)
    
@app.route("/api/v1.0/start_end")
def start_end():
    """Return a list of measurements from start to end"""
    # Query all Measurements from start
    results5 = session.query(Measurement.date, func.max(Measurement.tobs).label("max"), func.min(Measurement.tobs).label("min"), func.avg(Measurement.tobs).label("avg")).group_by(Measurement.date).filter(Measurement.date >= '2012-08-23').filter(Measurement.date <= '2017-08-23').all()

    # Create a dictionary from the row data and append to a list of all_temps
    range_tempstart = []
    for temprange in results5:
        temprange_dict = {}
        temprange_dict["date"] = temprange.date
        temprange_dict["maxtobs"] = temprange.max
        temprange_dict["mintobs"] = temprange.min
        temprange_dict["avgtobs"] = temprange.avg
        range_tempstart.append(temprange_dict)

    return jsonify(range_tempstart)

if __name__ == '__main__':
    app.run(debug=True)
