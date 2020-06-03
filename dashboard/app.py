
import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy




#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Database Setup
#################################################

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/moving_violations.sqlite"
#db = SQLAlchemy(app)
# engine = create_engine("sqlite:///moving_violations.sqlite")

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@flightdb.cbg99jbqtg8u.us-east-2.rds.amazonaws.com/flightdb"
db = SQLAlchemy(app)

# # reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)
# Base.prepare(engine, reflect=True)

# # Save references to each table
airline = Base.classes.airline

# # Create our session (link) from Python to the DB
session = Session(db.engine)




#################################################
# Flask Routes
#################################################


@app.route("/")
def index():
    """Return the homepage."""
    results = session.query(airline.airline_name).all()
    for airline_name in results:
        print(airline_name)
    return render_template("index.html")



# @app.route("/heatmap")
# def heatmap():
#     """Return the heatmap of moving violations"""

#     return render_template("heatmap.html")

# @app.route("/mapmarker")
# def mapmarker():
#     """Return the map showing the cluster with concentration of moving violations"""

#     return render_template("marker.html")


# @app.route("/chartjs")
# def chartjs():
#     """Return a chart with the top 10 location with the highest fine"""

#     return render_template("my_chartjs.html")


if __name__ == "__main__":
    app.run(debug=True)