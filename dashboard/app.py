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
    return render_template("flight.html")    

@app.route("/flights/<year>")
def flights(year):
    """Return the homepage."""
    airlines = session.query(
    Flight.airline_code, Airline.airline_code, func.avg(Flight.departure_delay)
    ).filter(
        Airline.airline_code == Flight.airline_code
    ).filter(
        Flight.year == year
    ).group_by(
        Flight.airline_code
    ).group_by(
        Airline.airline_code
    ).all()
    
    results = engine.execute(f"select d.airport_code, a.airport_code, avg(f.departure_delay) from flight f inner join airport d on f.departure_airport = d.airport_id inner join airport a on f.arrival_airport = a.airport_id where f.year={year} group by d.airport_code, a.airport_code")

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
    sel = [flight_table.departure_airport, flight_table.arrival_airport, flight_table.year, flight_table.day, 
    func.avg(flight_table.departure_delay), func.avg(flight_table.arrival_delay)]

    day = session.query(*sel).\
                group_by(flight_table.departure_airport, flight_table.arrival_airport, flight_table.year, flight_table.day).\
                all()
        
    day_list = []
    for i in range(len(day)):
        day_dict = {} 
        day_dict['departure_airport'] = day[i][0]
        day_dict['arrival_airport'] = day[i][1]
        day_dict['year'] = day[i][2]
        day_dict['day'] = day[i][3]
        day_dict['departure_delay'] = day[i][4]
        day_dict['arrival_delay'] = day[i][5]
        day_list.append(day_dict)
    
    return jsonify(day_list)


@app.route("/barChartAirport")
def bar_chart_airport():
    airport_results = session.query(airport_table.airport_id, airport_table.airport_code, airport_table.airport_name).order_by(airport_table.airport_name).all()
    airport_list = []
    for i in range(len(airport_results)):
        airport_dict = {} 
        airport_dict['airport_id'] = airport_results[i][0]
        airport_dict['airport_code'] = airport_results[i][1]
        airport_dict['airport_name'] = airport_results[i][2]
        airport_list.append(airport_dict)
    return jsonify(airport_list)
    

@app.route("/barData")
def bar_data():
    sel = [flight_table.departure_airport, flight_table.arrival_airport, airline_table.airline_name,flight_table.year,
    func.avg(flight_table.departure_delay), func.avg(flight_table.arrival_delay), 
    func.avg(flight_table.carrier_delay), func.avg(flight_table.weather_delay),  
        func.avg(flight_table.national_aviation_system_delay), 
    func.avg(flight_table.security_delay), func.avg(flight_table.late_aircraft_delay), func.avg(flight_table.cancelled)]

    delay = session.query(*sel).\
                    filter(flight_table.airline_code == airline_table.airline_code).\
                    group_by(flight_table.departure_airport, flight_table.arrival_airport, airline_table.airline_name,flight_table.year).\
                    all()

    delay_list = []
    for i in range(len(delay)):
        delay_dict = {} 
        delay_dict['departure_airport'] = delay[i][0]
        delay_dict['arrival_airport'] = delay[i][1]
        delay_dict['airline_name'] = delay[i][2]
        delay_dict['year'] = delay[i][3]
        delay_dict['departure_delay'] = delay[i][4]
        delay_dict['arrival_delay'] = delay[i][5]
        delay_dict['carrier_delay'] = delay[i][6]
        delay_dict['weather_delay'] = delay[i][7]
        delay_dict['nas_delay'] = delay[i][8]
        delay_dict['security_delay'] = delay[i][9]
        delay_dict['late_aircraft_delay'] = delay[i][10]
        delay_dict['cancelled'] = float(delay[i][11])
        delay_list.append(delay_dict)
    

    return jsonify(delay_list)


@app.route("/barChart")
def bar_chart():

    return render_template("barChart.html")


if __name__ == "__main__":
    app.run(debug=True)
