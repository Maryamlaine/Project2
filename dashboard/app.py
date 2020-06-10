import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
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

flight_table = Base.classes.flight
airport_table = Base.classes.airport
airline_table = Base.classes.airline

Airline = Base.classes.airline
Airport = Base.classes.airport
Flight= Base.classes.flight


#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/bubbleChart")
def bubble_chart():
    return render_template("bubbleChart.html")


@app.route("/bubbleData_v1")
def bubble_data_2019():
    sel = [flight_table.arrival_airport,
       airport_table.airport_name,
       airport_table.city,
       airport_table.state,
       airport_table.longitude,
       airport_table.latitude,
       func.avg(flight_table.arrival_delay),
       func.avg(flight_table.departure_delay)]

    flight_2019 = session.query(*sel).\
                    filter(flight_table.arrival_airport == airport_table.airport_id).\
                    filter_by(year = 2019).\
                    group_by(flight_table.arrival_airport,
                            airport_table.airport_name,
                            airport_table.city,
                            airport_table.state,
                            airport_table.longitude,
                            airport_table.latitude).\
                    all()

    flight_list = []
    for i in range(len(flight_2019)):
        flight_dict = {} 
        flight_dict['airport_id'] = flight_2019[i][0]
        flight_dict['airport_name'] = flight_2019[i][1]
        flight_dict['city'] = flight_2019[i][2]
        flight_dict['state'] = flight_2019[i][3]
        flight_dict['longitude'] = flight_2019[i][4]
        flight_dict['latitude'] = flight_2019[i][5]
        flight_dict['arrival_delay'] = flight_2019[i][6]
        flight_dict['departure_delay'] = flight_2019[i][7]
        flight_list.append(flight_dict)
    

    return jsonify(flight_list)


@app.route("/bubbleData_v2")
def bubble_data_2020():
    sel = [flight_table.arrival_airport,
            airport_table.airport_name,
            airport_table.city,
            airport_table.state,
            airport_table.longitude,
            airport_table.latitude,
            func.avg(flight_table.arrival_delay),
            func.avg(flight_table.departure_delay)]

    flight_2020 = session.query(*sel).\
                    filter(flight_table.arrival_airport == airport_table.airport_id).\
                    filter_by(year = 2020).\
                    group_by(flight_table.arrival_airport,
                            airport_table.airport_name,
                            airport_table.city,
                            airport_table.state,
                            airport_table.longitude,
                            airport_table.latitude).\
                    all()

    flight_list = []
    for i in range(len(flight_2020)):
        flight_dict = {} 
        flight_dict['airport_id'] = flight_2020[i][0]
        flight_dict['airport_name'] = flight_2020[i][1]
        flight_dict['city'] = flight_2020[i][2]
        flight_dict['state'] = flight_2020[i][3]
        flight_dict['longitude'] = flight_2020[i][4]
        flight_dict['latitude'] = flight_2020[i][5]
        flight_dict['arrival_delay'] = flight_2020[i][6]
        flight_dict['departure_delay'] = flight_2020[i][7]
        flight_list.append(flight_dict)
    

    return jsonify(flight_list)


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
    return render_template("flightRoutes.html")    

@app.route("/flights/<year>")
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

    list_delays = []

    for departure_airport, arrival_airport, departure_delay in results:
        y = { 'origin':departure_airport, 
               'destination': arrival_airport, 
                'count':  departure_delay
        }
        list_delays.append(y)

    return jsonify(list_delays)
    

@app.route("/calendarData")
def calendar_data():
    sel = [flight_table.day, func.avg(flight_table.arrival_delay)]

    day = session.query(*sel).\
                            filter_by(year = 2019).\
                            group_by(flight_table.day).\
                            all()
    
    day_list = []
    for i in range(len(day)):
        day_dict = {} 
        day_dict['day'] = day[i][0]
        day_dict['avg_arrival_delay'] = day[i][1]
        day_list.append(day_dict)
    
    return jsonify(day_list)


@app.route("/calendarMap")
def calendar_map():
    return render_template("calendar.html")


@app.route("/barChartAirport")
def bar_chart_airport():
    airport_results = session.query(airport_table.airport_name).order_by(airport_table.airport_name).all()
    airport_list = []
    for i in range(len(airport_results)):
        airport_dict = {} 
        airport_dict['airport_name'] = airport_results[i][0]
        airport_list.append(airport_dict)
    return jsonify(airport_list)
    
@app.route("/barData")
def bar_data():
    airline = pd.read_sql(session.query(airline_table).statement, session.bind) 
    flight = pd.read_sql(session.query(flight_table).statement, session.bind) 
    airport = pd.read_sql(session.query(airport_table).statement, session.bind)
    flight_2019 = flight[(flight.year == 2019)]
    flight_airport = pd.merge(flight_2019, airport, left_on = "departure_airport", right_on = "airport_id")
    flight_airport.drop(["city", "state", "longitude", "latitude", "address", "departure_airport", "airport_id"], axis = 1, inplace = True)
    flight_airport.rename(columns = {'airport_name': 'departure_airport', 'airport_code': 'departure_airport_code'}, inplace = True)
    new_flight_airport = pd.merge(flight_airport, airport, left_on = "arrival_airport", right_on = "airport_id")
    new_flight_airport.drop([ "city", "state", "longitude", "latitude", "address","arrival_airport", "airport_id"], axis=1, inplace = True)
    new_flight_airport.rename(columns = {'airport_name': 'arrival_airport', 'airport_code': 'arrival_airport_code'}, inplace = True)
    flight_airline = pd.merge(new_flight_airport, airline, on = "airline_code")
    flight_airline.drop(["Code", "airline_code"], axis = 1, inplace = True)
    flight_airline.rename(columns = {'Description': 'airline'}, inplace = True)
    count_airports = flight_airline.groupby(["arrival_airport", "departure_airport","airline"]).agg("count")["flight_id"].reset_index()
    delay = flight_airline.groupby(["arrival_airport", "departure_airport", "airline"]).agg("mean")[["departure_delay", "arrival_delay","carrier_delay","weather_delay","national_aviation_system_delay","security_delay", "late_aircraft_delay","cancelled"]].reset_index()
    df = pd.merge(delay, count_airports, on = ["arrival_airport", "departure_airport", "airline"])
    df_dict = df.to_json(orient='records')

    return jsonify(df_dict)


@app.route("/barChartAirport")
def bar_chart():

    return render_template("calendar.html")


if __name__ == "__main__":
    app.run(debug=True)
