import re
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_login import login_required, current_user
from model.user import User

savedlocations_met_api = Blueprint('savedlocations_met_api', __name__, url_prefix='/api')

api = Api(savedlocations_met_api)

class SavedLocationAPI:
    """
    Define the API endpoints for the savedlocation model (session-authenticated).
    """
    class _CRUD(Resource):
        @login_required
        def get(self):
            """
            Return saved locations for all users.
            """
            print("✅ current_user.is_authenticated:", current_user.is_authenticated)
            print("👤 current_user:", current_user)
            users = User.query.all()
            all_locations = []

            for user in users:
                if user.savedlocation:
                    all_locations.append({
                        'user_id': user.id,
                        'uid': user.uid,
                        'savedlocation': user.savedlocation
                    })

            if not all_locations:
                return {'message': 'No saved locations found'}, 404

            return jsonify(all_locations)

        @login_required
        def post(self):
            """
            Create savedlocation for the authenticated user.
            """
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

        @login_required
        def put(self):
            """
            Update and add to the savedlocation of the authenticated user or a target user (if admin).
            """
            body = request.get_json()
            uid = body.get('uid') or current_user.uid

            user = User.query.filter_by(_uid=uid).first()
            if not user:
                return {'message': 'User not found'}, 404

            # Check permission: only allow editing others if Admin
            if current_user.uid != uid and current_user.role != 'Admin':
                return {'message': 'Unauthorized'}, 403

            new_savedlocation = body.get('savedlocation')
            if not new_savedlocation:
                return {'message': 'No new savedlocation provided'}, 400

            formatted_new_savedlocation = re.sub(r'\s*,\s*', ', ', new_savedlocation.strip())
            current_savedlocations = user.savedlocation.split(', ') if user.savedlocation else []
            combined_savedlocations = list(set(current_savedlocations + formatted_new_savedlocation.split(', ')))

            user.savedlocation = ', '.join(combined_savedlocations)
            user.update({'savedlocation': user.savedlocation})
            return jsonify({'message': f'Saved location updated for {user.uid}', 'savedlocation': user.savedlocation})


        @login_required
        def delete(self):
            """
            Delete a specified savedlocation for the current user or another user (admin).
            """
            body = request.get_json()
            uid = body.get('uid') or current_user.uid  # Fallback to current user if no uid provided

            user = User.query.filter_by(_uid=uid).first()

            if not user:
                return {'message': 'User not found'}, 404

            # Admin or self-deletion allowed
            if current_user.uid != uid and current_user.role != 'Admin':
                return {'message': 'Unauthorized'}, 403

            # Handle delete all
            if body.get('delete_all', True):
                user.savedlocation = ""
                user.update({'savedlocation': user.savedlocation})
                return {'message': f'All saved locations deleted for {user.uid}.'}, 200

            # Handle delete single location
            if 'savedlocation' not in body:
                return {'message': 'No savedlocation provided'}, 400

            if not user.savedlocation:
                return {'message': 'No savedlocation found for this user'}, 404

            savedlocation_to_delete = body['savedlocation']
            savedlocations = user.savedlocation.split(', ')

            if savedlocation_to_delete not in savedlocations:
                return {'message': 'savedlocation not found'}, 404

            savedlocations.remove(savedlocation_to_delete)
            user.savedlocation = ', '.join(savedlocations)
            user.update({'savedlocation': user.savedlocation})

            return {'message': f'Saved location removed from {user.uid}.'}, 200


# Register resource
api.add_resource(SavedLocationAPI._CRUD, '/savedlocationsmet')
