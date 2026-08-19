from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from app import db
from models import Trip, User
from middleware.auth import auth_middleware

trips_bp = Blueprint("trips", __name__)


def _parse_date(value):
    if value is None:
        return None
    try:
        # Accept ISO format date or full datetime
        d = datetime.fromisoformat(value)
        return d.date()
    except Exception:
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception:
            return None


@trips_bp.route("/trips", methods=["GET"])
@auth_middleware
def list_trips():
    user_id = get_jwt_identity()
    trips = Trip.query.filter_by(user_id=user_id).all()
    return jsonify([t.to_dict() for t in trips])


@trips_bp.route("/trips/<int:trip_id>", methods=["GET"])
@auth_middleware
def get_trip(trip_id: int):
    user_id = get_jwt_identity()
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != user_id:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(trip.to_dict())


@trips_bp.route("/trips", methods=["POST"])
@auth_middleware
def create_trip():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    destination = data.get("destination")
    start_date = _parse_date(data.get("start_date"))
    end_date = _parse_date(data.get("end_date"))
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    itinerary = data.get("itinerary")

    if not destination or not start_date:
        return jsonify({"error": "destination and start_date are required"}), 400

    trip = Trip(
        user_id=user_id,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        latitude=latitude,
        longitude=longitude,
        itinerary=itinerary,
    )
    db.session.add(trip)
    db.session.commit()
    return jsonify(trip.to_dict()), 201


@trips_bp.route("/trips/<int:trip_id>", methods=["PUT", "PATCH"])
@auth_middleware
def update_trip(trip_id: int):
    user_id = get_jwt_identity()
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != user_id:
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json() or {}
    if "destination" in data:
        trip.destination = data.get("destination")
    if "start_date" in data:
        d = _parse_date(data.get("start_date"))
        if d is None:
            return jsonify({"error": "Invalid start_date format"}), 400
        trip.start_date = d
    if "end_date" in data:
        trip.end_date = _parse_date(data.get("end_date"))
    if "latitude" in data:
        trip.latitude = data.get("latitude")
    if "longitude" in data:
        trip.longitude = data.get("longitude")
    if "itinerary" in data:
        trip.itinerary = data.get("itinerary")

    db.session.commit()
    return jsonify(trip.to_dict())


@trips_bp.route("/trips/<int:trip_id>", methods=["DELETE"])
@auth_middleware
def delete_trip(trip_id: int):
    user_id = get_jwt_identity()
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != user_id:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(trip)
    db.session.commit()
    return jsonify({}), 204
from flask import Blueprint, jsonify
from middleware.auth import auth_middleware

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/trips', methods=['GET'])
@auth_middleware
def get_trips():
    # This route is now protected and will only be accessible with a valid JWT token
    return jsonify({'message': "Protected route accessed successfully"})
