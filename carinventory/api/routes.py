from flask import Blueprint, request,jsonify
from flask_migrate import current
from carinventory.helpers import token_required
from carinventory.models import db,User, Car,car_schema, cars_schema
api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/getdata")
def getdata():
    return {"some": "value", "foo":"bar"}

@api.route("/car", methods = ["POST"])
@token_required
def create_car(current_user_token):
    print(request.get_json(force=True))
    doors = request.json["doors"]
    seats = request.json["seats"]
    model = request.json["model"]
    year = request.json["year"]
    color = request.json["color"]
    price = request.json["price"]
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    car = Car(doors,seats,model,year,color,price,user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route("/car", methods = ["GET"])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route("/car/<id>", methods = ["GET"])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({"message": "that was not what I asked for stupid"}), 401

@api.route("/car/<id>", methods = ["POST", "PUT"])
@token_required
def update_car(current_user_token,id):
    car = Car.query.get(id)

    car.doors = request.json["doors"]
    car.seats = request.json["seats"]
    car.model = request.json["model"]
    car.year = request.json["year"]
    car.color = request.json["color"]
    car.price = request.json["price"]
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route("/car/<id>", methods = ["DELETE"])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)