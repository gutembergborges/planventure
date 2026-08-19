from flask import Blueprint, jsonify
from middleware.auth import auth_middleware

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/trips', methods=['GET'])
@auth_middleware
def get_trips():
    # This route is now protected and will only be accessible with a valid JWT token
    return jsonify({'message': "Protected route accessed successfully"})
