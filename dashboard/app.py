import os
#import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@flightdb.cbg99jbqtg8u.us-east-2.rds.amazonaws.com/flightdb"
# db = SQLAlchemy(app)
engine = create_engine("postgresql://postgres:postgres@flightdb.cbg99jbqtg8u.us-east-2.rds.amazonaws.com/flightdb")
# # reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# # Save references to each table
Airline = Base.classes.airline
Airport = Base.classes.airport
Flight= Base.classes.flight

# # Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    """Return the homepage."""
    results = session.query(Airline.airline_name).all()
    for airline_name in results:
        # print(airline_name)
        return render_template("index.html")

@app.route("/airports")
def airports():
    """Return the homepage."""
    locations = session.query(Airport.airport_code, Airport.airport_name,Airport.city ,Airport.state, Airport.longitude,Airport.latitude).all()
    # print(locations)
    list_airports = []
    for x in locations:
        print(x)
    for airport_code, airport_name, city, state, longitude, latitude in locations:
        y = { 'iata':airport_code, 
               'name': airport_name, 
                'city': city, 
                'state': state, 
                'country': 'USA', 
                'latitude': latitude,
                'longitude': longitude 
        }
        list_airports.append(y)
        # print(jsonify(list_airports))
    return jsonify(list_airports)

@app.route("/flight")
def flight():
    return render_template("flight.html")    

@app.route("/flights")
def flights():
    """Return the homepage."""
    airlines = session.query(
	Flight.airline_code, Airline.airline_code, func.avg(Flight.departure_delay)
	).filter(
		Airline.airline_code == Flight.airline_code
	).filter(
		Flight.year == '2020'
	).group_by(
		Flight.airline_code
	).group_by(
		Airline.airline_code
	).all()
    
    results = engine.execute("select d.airport_code, a.airport_code, avg(f.departure_delay) from flight f inner join airport d on f.departure_airport = d.airport_id inner join airport a on f.arrival_airport = a.airport_id group by d.airport_code, a.airport_code")
    # results = session.query(Flight.departure_airport, Flight.arrival_airport, func.avg(Flight.departure_delay).label("count")).\
    #     group_by(Flight.departure_airport, Flight.arrival_airport).all()
    # print(results)
    list_delays = []
    # for x in results:
        # print(x)
    for departure_airport, arrival_airport, departure_delay in results:
        y = { 'origin':departure_airport, 
               'destination': arrival_airport, 
                'count':  departure_delay
        }
        list_delays.append(y)
        # print(jsonify(list_delays))
    return jsonify(list_delays)
    # return redirect('/delay')

# @app.route("/delay")
# def delay():
#     return render_template("flight.html")


if __name__ == "__main__":
    app.run(debug=True)
