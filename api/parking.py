# # routes/parking_api.py

# from flask import Blueprint, request, jsonify
# from flask_restful import Api, Resource
# from model.parking import ParkingAvailabilityModel

# parking_api = Blueprint('parking_api', __name__, url_prefix='/api/parking')
# api = Api(parking_api)

# model_instance = ParkingAvailabilityModel()

# class ParkingAPI:
#     class _Predict(Resource):
#         def post(self):
#             data = request.get_json()
#             required_fields = ['pole_id', 'day_of_week', 'hour_of_day']

#             if not all(field in data for field in required_fields):
#                 return {"error": "Missing required fields", "required_fields": required_fields}, 400

#             pole_id = data['pole_id']
#             day_of_week = int(data['day_of_week'])
#             hour_of_day = int(data['hour_of_day'])

#             probability = model_instance.predict(pole_id, day_of_week, hour_of_day)

#             return jsonify({'predicted_parking_availability_percent': probability})

# api.add_resource(ParkingAPI._Predict, '/predict')
