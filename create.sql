-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-02-22 17:12:15.909

-- tables
-- Table: car
CREATE TABLE car (
    id_car int  NOT NULL AUTO_INCREMENT,
    car_model varchar(20)  NOT NULL,
    car_make int  NOT NULL,
    average_rate int  NOT NULL,
    CONSTRAINT car_pk PRIMARY KEY (id_car)
);

-- Table: car_rate
CREATE TABLE car_rate (
    car_id_car int  NOT NULL,
    rate_id_rate int  NOT NULL,
    CONSTRAINT car_rate_pk PRIMARY KEY (car_id_car,rate_id_rate)
);

-- Table: rate
CREATE TABLE rate (
    id_rate int  NOT NULL AUTO_INCREMENT,
    count int  NOT NULL,
    rate_sum int  NOT NULL,
    CONSTRAINT rate_pk PRIMARY KEY (id_rate)
);

-- foreign keys
-- Reference: Table_3_car (table: car_rate)
ALTER TABLE car_rate ADD CONSTRAINT Table_3_car FOREIGN KEY Table_3_car (car_id_car)
    REFERENCES car (id_car);

-- Reference: Table_3_rate (table: car_rate)
ALTER TABLE car_rate ADD CONSTRAINT Table_3_rate FOREIGN KEY Table_3_rate (rate_id_rate)
    REFERENCES rate (id_rate);

-- End of file.

