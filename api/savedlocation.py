import re
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from __init__ import app
from api.jwt_authorize import token_required
from model.user import User

savedlocations_api = Blueprint('savedlocations_api', __name__, url_prefix='/api')

api = Api(savedlocations_api)

class SavedLocationAPI:
    """
    Define the API endpoints for the savedlocation model.
    """
    class _CRUD(Resource):
        """
        savedlocation API operation for Create, Read, Update, Delete.
        """

        @token_required()
        def get(self):
            """
            Return the savedlocation of the authenticated user as a JSON object.
            """
            current_user = g.current_user
            user = User.query.filter_by(_uid=current_user.uid).first()
            if not user or not user.savedlocation:
                return {'message': 'No savedlocation found for this user'}, 404
            return jsonify(user.savedlocation)

        @token_required()
        def post(self):
            """
            Create savedlocation for the authenticated user.
            """
            current_user = g.current_user
            user = User.query.filter_by(_uid=current_user.uid).first()
            if not user:
                return {'message': 'User not found'}, 404

            body = request.get_json()
            new_savedlocation = body.get('savedlocation')
            if not new_savedlocation:
                return {'message': 'No savedlocation provided'}, 400

            formatted_savedlocation = re.sub(r'\s*,\s*', ', ', new_savedlocation.strip())
            user.savedlocation = formatted_savedlocation
            user.update({'savedlocation': user.savedlocation})
            return jsonify(user.savedlocation)

        @token_required()
        def put(self):
            """
            Update and add to the savedlocation of the authenticated user.
            """
            current_user = g.current_user
            user = User.query.filter_by(_uid=current_user.uid).first()
            if not user:
                return {'message': 'User not found'}, 404

            body = request.get_json()
            new_savedlocation = body.get('savedlocation')
            if not new_savedlocation:
                return {'message': 'No new savedlocation provided'}, 400

            formatted_new_savedlocation = re.sub(r'\s*,\s*', ', ', new_savedlocation.strip())
            current_savedlocations = user.savedlocation.split(', ') if user.savedlocation else []
            combined_savedlocations = list(set(current_savedlocations + formatted_new_savedlocation.split(', ')))
            user.savedlocation = ', '.join(combined_savedlocations)
            user.update({'savedlocation': user.savedlocation})
            return jsonify(user.savedlocation)

        @token_required()
        def delete(self):
            """
            Delete a specified savedlocation of the authenticated user.
            """
            body = request.get_json()

            if not body or 'savedlocation' not in body:
                return {'message': 'No savedlocation provided'}, 400
            
            current_user = g.current_user
            savedlocation_to_delete = body.get('savedlocation')
            savedlocations = current_user.savedlocation.split(', ')

            if savedlocation_to_delete not in savedlocations:
                return {'message': 'savedlocation not found'}, 404

            savedlocations.remove(savedlocation_to_delete)
            current_user.savedlocation = ', '.join(savedlocations)
            current_user.update({'savedlocation': current_user.savedlocation})

            return {'message': 'savedlocation deleted successfully'}, 200

api.add_resource(SavedLocationAPI._CRUD, '/savedlocations')
