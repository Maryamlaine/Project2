DROP TABLE IF EXISTS flight;
DROP TABLE IF EXISTS airline;
DROP TABLE IF EXISTS airport;
DROP TABLE IF EXISTS cancellation;

CREATE TABLE "airline" (
    "airline_code" VARCHAR   NOT NULL,
    "airline_name" VARCHAR   NOT NULL,
    CONSTRAINT "pk_airline" PRIMARY KEY (
        "airline_code"
     )
);

CREATE TABLE "airport" (
    "airport_id" INT   NOT NULL,
    "airport_code" VARCHAR   NOT NULL,
    "airport_name" VARCHAR   NOT NULL,
    "address" VARCHAR,
    "city" VARCHAR   NOT NULL,
    "state" VARCHAR   NOT NULL,
    "longitude" FLOAT   NOT NULL,
    "latitude" FLOAT   NOT NULL,
    CONSTRAINT "pk_airport" PRIMARY KEY (
        "airport_id"
     )
);

CREATE TABLE "cancellation" (
    "cancellation_code" VARCHAR   NOT NULL,
    "cancellation_description" VARCHAR   NOT NULL,
    CONSTRAINT "pk_cancellation" PRIMARY KEY (
        "cancellation_code"
     )
);

CREATE TABLE "flight" (
    "flight_id" INT   NOT NULL,
    "year" INT   NOT NULL,
    "month" INT   NOT NULL,
    "day" INT   NOT NULL,
    "airline_code" VARCHAR   NOT NULL,
    "departure_airport" INT   NOT NULL,
    "arrival_airport" INT   NOT NULL,
    "departure_delay" FLOAT,
    "arrival_delay" FLOAT,
    "carrier_delay" FLOAT,
    "weather_delay" FLOAT,
    "national_aviation_system_delay" FLOAT,
    "security_delay" FLOAT,
    "late_aircraft_delay" FLOAT,
    "cancelled" INT NOT NULL,
    "cancellation_code" VARCHAR,
    CONSTRAINT "pk_flight" PRIMARY KEY (
        "flight_id"
     )
);



ALTER TABLE "flight" ADD CONSTRAINT "fk_flight_airline_code" FOREIGN KEY("airline_code")
REFERENCES "airline" ("airline_code");

ALTER TABLE "flight" ADD CONSTRAINT "fk_flight_departure_airport" FOREIGN KEY("departure_airport")
REFERENCES "airport" ("airport_id");

ALTER TABLE "flight" ADD CONSTRAINT "fk_flight_arrival_airport" FOREIGN KEY("arrival_airport")
REFERENCES "airport" ("airport_id");

ALTER TABLE "flight" ADD CONSTRAINT "fk_cancellation_code" FOREIGN KEY("cancellation_code")
REFERENCES "cancellation" ("cancellation_code");

