from flask import Flask, jsonify
import numpy as np
import pandas as pd

import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


start_date='2016-08-01'
end_date='2016-08-28'



app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    date_prcp=session.query(Measurement.date, Measurement.prcp).all()
    data={}
    for row in date_prcp:
        data[row[0]]=row[1]
    return jsonify(data)
        
@app.route('/api/v1.0/stations')
def stations():
    stat=session.query(Station.station).all()
    return jsonify(stat)

@app.route('/api/v1.0/tobs')
def temps():
    data_12_mo=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>= prev_year).all()
    return jsonify(data_12_mo)






@app.route("/api/v1.0/<start_date>")
def start_date_agg(start_date):

    canonicalized = start_date.replace(" ", "").lower()
    
    start_date_agg= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
    filter(Measurement.date >= start_date).all()
    for date in start_date_agg:
        search_term = start_date_agg["2016-08-01"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(start_date_agg)

    return jsonify({"error": f"Character with real_name {start_date_agg} not found."}), 404


# @app.route("/api/v1.0/justice-league/superhero/<superhero>")
# def justice_league_by_superhero__name(superhero):
#     """Fetch the Justice League character whose superhero matches
#        the path variable supplied by the user, or a 404 if not."""

#     canonicalized = superhero.replace(" ", "").lower()
    
#     for character in justice_league_members:
#         search_term = character["superhero"].replace(" ", "").lower()

#         if search_term == canonicalized:
#             return jsonify(character)

#     return jsonify({"error": "Character not found."}), 404




if __name__ == "__main__":
    app.run(debug=True)
