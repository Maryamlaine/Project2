DROP TABLE IF EXISTS flight;
DROP TABLE IF EXISTS airline;
DROP TABLE IF EXISTS airport;


CREATE TABLE "airline" (
    "airline_id" INT   NOT NULL,
    "IATA_airline_code" VARCHAR   NOT NULL,
    "airline_name" VARCHAR   NOT NULL,
    CONSTRAINT "pk_airline" PRIMARY KEY (
        "airline_id"
     )
);

CREATE TABLE "airport" (
    "airport_id" INT   NOT NULL,
    "airport_name" VARCHAR   NOT NULL,
    "IATA_airport_code" VARCHAR   NOT NULL,
    "city" VARCHAR   NOT NULL,
    "state" VARCHAR   NOT NULL,
    "country" VARCHAR   NOT NULL,
    "latitude" FLOAT   NOT NULL,
    "longitude" FLOAT   NOT NULL,
    CONSTRAINT "pk_airport" PRIMARY KEY (
        "airport_id"
     )
);

CREATE TABLE "flight" (
    "flight_id" INT   NOT NULL,
    "departure_year" INT   NOT NULL,
    "departure_month" INT   NOT NULL,
    "departure_day" INT   NOT NULL,
    "departure_time" INT   NOT NULL,
    "arrival_time" INT   NOT NULL,
    "departure_delay" FLOAT   NOT NULL,
    "arrival_delay" FLOAT   NOT NULL,
    "airline_id" INT   NOT NULL,
    "departure_airport" INT   NOT NULL,
    "destination_airport" INT   NOT NULL,
    "air_system_delay" FLOAT,
    "security_delay" FLOAT,
    "airline_delay" FLOAT,
    "late_aircraft_delay" FLOAT,
    "weather_delay" FLOAT,
    CONSTRAINT "pk_flight" PRIMARY KEY (
        "flight_id"
     )
);

ALTER TABLE "flight" ADD CONSTRAINT "fk_flight_airline_id" FOREIGN KEY("airline_id")
REFERENCES "airline" ("airline_id");

ALTER TABLE "flight" ADD CONSTRAINT "fk_flight_departure_airport" FOREIGN KEY("departure_airport")
REFERENCES "airport" ("airport_id");

ALTER TABLE "flight" ADD CONSTRAINT "fk_flight_destination_airport" FOREIGN KEY("destination_airport")
REFERENCES "airport" ("airport_id");

