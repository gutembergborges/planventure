from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from app import db
from models import Trip
from middleware.auth import auth_middleware
from utils.parsers import parse_date
from utils.itinerary import generate_default_itinerary

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/trips', methods=['GET', 'POST'])
@auth_middleware
def handle_trips():
    if request.method == 'POST':
        return create_trip()
    return get_trips()

def get_trips():
    user_id = get_jwt_identity()
    trips = Trip.query.filter_by(user_id=user_id).all()

    return jsonify(
        [trip.to_dict() for trip in trips]
    ), 200

def create_trip():
    data = request.get_json() or {}

    # Validate required fields
    required_fields = ['destination', 'start_date', 'end_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        user_id = get_jwt_identity()
        destination = data['destination']
        start_date = parse_date(data['start_date'])
        end_date = parse_date(data['end_date'])
        if start_date is None or end_date is None:
            return jsonify({'error': 'Invalid date format'}), 400

        itinerary = data.get('itinerary')
        if not itinerary:
            itinerary = generate_default_itinerary(destination, start_date, end_date)

        trip = Trip(
            user_id=user_id,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            itinerary=itinerary,
        )

        db.session.add(trip)
        db.session.commit()

        return jsonify(
            trip.to_dict()
        ), 201
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create trip'}), 500

@trips_bp.route('/trips/<int:trip_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@auth_middleware
def handle_trip(trip_id):
    if request.method == 'GET':
        return get_trip(trip_id)
    elif request.method in ['PUT', 'PATCH']:
        return update_trip(trip_id)
    elif request.method == 'DELETE':
        return delete_trip(trip_id)

# ...rest of the existing code for get_trip, update_trip, and delete_trip
def get_trip(trip_id):
    user_id = get_jwt_identity()
    trip = Trip.query.get_or_404(trip_id, user_id)
    # trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()

    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
    
    return jsonify(trip.to_dict())

def update_trip(trip_id: int):
    user_id = get_jwt_identity()
    trip = Trip.query.get_or_404(trip_id, user_id)
    # trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()

    if not trip:
        return jsonify({'error': 'Trip not found'}), 404

    data = request.get_json()

    try:
        if 'destination' in data:
            trip.destination = data.get('destination')
        if 'start_date' in data:
            d = parse_date(data.get('start_date'))
            if d is None:
                return jsonify({'error': 'Invalid start_date format'}), 400
            trip.start_date = d
        if 'end_date' in data:
            trip.end_date = parse_date(data.get('end_date'))
        if 'latitude' in data:
            trip.latitude = data.get('latitude')
        if 'longitude' in data:
            trip.longitude = data.get('longitude')
        if 'itinerary' in data:
            trip.itinerary = data.get('itinerary')

        db.session.commit()
        return jsonify({'message': 'Trip updated successfully'}), 200
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update trip'}), 500

def delete_trip(trip_id: int):
    user_id = get_jwt_identity()
    trip = Trip.query.get_or_404(trip_id, user_id)

    if not trip:
        return jsonify({'error': 'Trip not found'}), 404

    try:
        db.session.delete(trip)
        db.session.commit()
        return jsonify({'message': 'Trip deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete trip'}), 500

@trips_bp.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed'}), 405