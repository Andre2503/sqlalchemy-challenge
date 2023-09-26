import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, between

from flask import Flask, jsonify

#Database set up 
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

#refelct the database into a new model 
Base = automap_base()

#reflect the tables
Base.prepare(autoload_with=engine)

#check name of tables
print(Base.classes.keys())

#save reference to the table 
Measurement = Base.classes.measurement
Station = Base.classes.station

#flask setup 
app = Flask(__name__)

#flask routes 
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Hi there! Welcome, hope you can find what you are after below<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YY-MM-DD *returns min, avg and max for all dates > or = to supplied date*<br/>"
        f"/api/v1.0/YY-MM-DD/YY-MM-DD *returns min, avg and max for all dates between supplied dates*"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    """Returns a list of all precipitation data"""
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close

    all_prcp = []
    for date, prcp in results:
        prcp_dict ={}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    """Returns a JSON list of stations from the dataset"""
    results = session.query(Station.station, Station.name).all()

    session.close()

    #convert results in dictionary for readability
    all_stations = [(station, name) for station, name in results] #is this ok or should I use a dictionary instead? 

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    """Returns tobs from most active station for previous year"""
    results = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-18').\
        filter(Measurement.station == 'USC00519281').all() 
    
    session.close()

    #unpack tuple
    all_tobs = list(np.ravel(results))

    #return jason
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
     
     """Fetch the min, avergage and max temp for the for all temps on and after the date
      matching the date supplied by the user, or a 404 if not"""
     
     session = Session(engine)

     results = session.query(Measurement.date, 
                             func.min(Measurement.tobs),
                             func.avg(Measurement.tobs),
                             func.max(Measurement.tobs)).filter(Measurement.date >= start_date).group_by(Measurement.date).all()

     session.close

     #list comprehension to store results in a dictionary 
     metric_list = [{"date":date, "TMIN":min_temp, "TAVG": avg_temp, "TMAX": max_temp} for date, min_temp, avg_temp, max_temp in results] 

     #return json
     return jsonify(metric_list)

    
@app.route("/api/v1.0/<start>/<end>")
def start_end (start, end):

    """Fetch the min, avergage and max temp for all temps between the start and end date
      supplied by the user, or a 404 if not"""
    
    session = Session(engine)

    results = session.query(Measurement.date,
                            func.min(Measurement.tobs),
                            func.avg(Measurement.tobs),
                            func.max(Measurement.tobs)).filter(Measurement.date.between(start, end)).group_by(Measurement.date).all()
    
    session.close

    #transform results into a dictionary for JSON response
    data_list = [{"date":date, "TMIN":min_temp, "TAVG":avg_temp, "TMAX":max_temp} for date, min_temp, avg_temp, max_temp in results]

    #prepare json response

    return jsonify(data_list)

    

if __name__ == "__main__":
    app.run(debug=True)
