from fastapi import HTTPException
import requests
from mysql_connector import MySQLConnector

_mysql_connector = MySQLConnector()

def get_average_rate_cars():
    mycursor = _mysql_connector.mydb.cursor()
    mycursor.execute('SELECT car_model, car_make, average_rate FROM car c '
                     'INNER JOIN car_rate cr ON c.id_car = cr.car_id_car '
                     'INNER JOIN rate r ON r.id_rate = cr.rate_id_rate')
    cars = mycursor.fetchall()
    formatted_cars = []
    for car in cars:
        car_info = {
            "model": car[0],
            "make": car[1],
            "average_rate": car[2]
        }
        formatted_cars.append(car_info)

    return formatted_cars


def get_popular_cars():
    mycursor = _mysql_connector.mydb.cursor()
    mycursor.execute(
        'SELECT car_model, car_make, count FROM car c '
        'INNER JOIN car_rate cr ON c.id_car = cr.car_id_car '
        'INNER JOIN rate r ON r.id_rate = cr.rate_id_rate ORDER BY count DESC')
    popular_cars = mycursor.fetchall()

    formatted_popular_cars = []
    for car in popular_cars:
        car_info = {
            "model": car[0],
            "make": car[1],
            "number of rates": car[2]
        }
        formatted_popular_cars.append(car_info)

    return formatted_popular_cars


def is_exist_in_db(name: str):
    name_to_lower = name.lower()
    mycursor = _mysql_connector.mydb.cursor()
    query = "SELECT id_car FROM car WHERE car_make = %s"
    mycursor.execute(query, (name_to_lower,))
    car_is_exist = mycursor.fetchone()
    if car_is_exist is not None:
        return True
    else:
        return False


def rate_car(name: str, rate: int):
    name_to_lower = name.lower()
    if not is_exist_in_db(name_to_lower):
        raise HTTPException(status_code=404, detail="Car not found")
    id_car = get_id_car(name)
    id_rate = get_id_rate(id_car)
    update_value_car(id_rate, rate)
    raise HTTPException(status_code=200, detail="Rating added successfully")


def update_value_car(id: int, rate: int):
    mycursor = _mysql_connector.mydb.cursor()
    query = ("Update rate Set count = count + 1, rate_sum = rate_sum + %s,  "
             "average_rate = round((rate_sum + %s) / (count + 1),2) WHERE id_rate = %s")
    values = (rate, rate, id)
    mycursor.execute(query, values)
    _mysql_connector.mydb.commit()


def get_id_rate(id: int):
    mycursor = _mysql_connector.mydb.cursor()
    query = ("SELECT cr.rate_id_rate FROM car_rate cr "
             "INNER JOIN car c ON c.id_car = cr.car_id_car WHERE c.id_car = %s")

    mycursor.execute(query, (id,))
    id_rate = mycursor.fetchone()
    return id_rate[0]


def get_id_car(model: str):
    mycursor = _mysql_connector.mydb.cursor()
    query = "Select id_car from car where car_make = %s"

    mycursor.execute(query, (model,))
    id_car = mycursor.fetchone()
    return id_car[0]



def is_exist(name: str, model: str):
    name_to_lower = name.lower()
    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{name_to_lower}?format=json'

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        results = data.get('Results', [])

        if results:
            for result in results:
                if (
                        result.get("Make_Name", "").lower() == name_to_lower
                        and result.get("Model_Name", "").lower() == model.lower()
                ):
                    return True

            return False
        else:
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None


def insert_new_car(name: str, model: str):
    if not is_exist(name, model):
        raise HTTPException(status_code=404, detail="Car not found")

    mycursor = _mysql_connector.mydb.cursor()

    check = "Select * from car where car_model = %s AND car_make = %s"
    check_value = (name, model)
    mycursor.execute(check, check_value)
    is_exist_in_db = mycursor.fetchone()
    if is_exist_in_db is None:

        query_car = "INSERT INTO car(car_model, car_make) VALUES(%s, %s)"
        values_car = (name, model)
        mycursor.execute(query_car, values_car)
        _mysql_connector.mydb.commit()

        query_rate = "INSERT INTO rate(count, rate_sum, average_rate) VALUES(%s, %s, %s)"
        values_rate = (0, 0, 0)
        mycursor.execute(query_rate, values_rate)
        _mysql_connector.mydb.commit()

        id_car_query = "SELECT MAX(id_car) FROM car"
        mycursor.execute(id_car_query)
        id_car = mycursor.fetchone()

        id_rate_query = "SELECT MAX(id_rate) FROM rate"
        mycursor.execute(id_rate_query)
        id_rate = mycursor.fetchone()

        if id_car is not None and id_rate is not None:
            insert_car_rate_id(int(id_car[0]), int(id_rate[0]))

        raise HTTPException(status_code=200, detail="Car added")
    else:
        raise HTTPException(status_code=404, detail="Car is already in database")


def insert_car_rate_id(id_car: int, id_rate: int):
    mycursor = _mysql_connector.mydb.cursor()
    query_car_rate = "INSERT INTO car_rate(car_id_car, rate_id_rate) VALUES(%s, %s)"
    values = (id_car, id_rate)
    mycursor.execute(query_car_rate, values)
    _mysql_connector.mydb.commit()