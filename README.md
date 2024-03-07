# Car Management System

This repository contains the backend code for a simple Car Management System API. The API allows users to perform various operations related to cars, including adding new cars, rating them, fetching the list of cars, and retrieving popular cars based on the number of ratings.
![image](https://github.com/DucMajek/Simple-Car-Api/assets/97256581/e9c561a5-52d3-4f6c-8dc8-8d849a41e450)


## Endpoints

### 1. Add a Car
#### `POST /cars`
* Request body should contain car make and model name.
* The existence of the car is checked using the [NHTSA API](https://vpic.nhtsa.dot.gov/api/).
  - If the car doesn't exist, an error is returned.
  - If the car exists, it is saved in the database.

### 2. Add a Rate for a Car
#### `POST /rate`
* Add a rate for a car on a scale from 1 to 5.

### 3. Get List of Cars
#### `GET /cars`
* Fetches a list of all cars already present in the application database.
* Provides their current average rating.

### 4. Get Popular Cars
#### `GET /popular`
* Returns a list of top cars in the database.
* Ranking is based on the number of rates received (not on average rate values).

## Getting Started
1. Clone the repository.
   ```bash
   git clone https://github.com/DucMajek/Simple-Car-Api.git
   ```
