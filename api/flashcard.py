from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from __init__ import db
from model.flashcard import Flashcard

flashcard_api = Blueprint('flashcard_api', __name__, url_prefix='/api')
CORS(flashcard_api, supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE'])
api = Api(flashcard_api)

class FlashcardAPI:

    class _CRUD(Resource):
        @cross_origin(supports_credentials=True)
        def post(self):
            data = request.get_json()
            term = data.get('term')
            definition = data.get('definition')
            lesson_id = data.get('lesson_id')

            if not term or not definition or not lesson_id:
                return jsonify({"message": "term, definition, and lesson_id are required"}), 400

            flashcard = Flashcard(term=term, definition=definition, lesson_id=lesson_id)
            flashcard.create()
            return jsonify({"message": "Flashcard created successfully", "flashcard": flashcard.read()})

        def get(self):
            lesson_id = request.args.get('lesson_id')
            if not lesson_id:
                return jsonify({"message": "lesson_id is required"}), 400

            flashcards = Flashcard.query.filter_by(lesson_id=lesson_id).all()
            return jsonify([fc.read() for fc in flashcards])

        def put(self):
            data = request.get_json()
            flashcard_id = data.get('id')

            if not flashcard_id:
                return jsonify({"message": "flashcard id is required"}), 400

            flashcard = Flashcard.query.get(flashcard_id)

            if not flashcard:
                return jsonify({"message": "Flashcard not found"}), 404

            flashcard.update(data)
            return jsonify({"message": "Flashcard updated successfully"})

        def delete(self):
            data = request.get_json()
            flashcard_id = data.get('id')

            if not flashcard_id:
                return jsonify({"message": "flashcard id is required"}), 400

            flashcard = Flashcard.query.get(flashcard_id)

            if not flashcard:
                return jsonify({"message": "Flashcard not found"}), 404

            flashcard.delete()
            return jsonify({"message": "Flashcard deleted successfully"})

api.add_resource(FlashcardAPI._CRUD, '/flashcard')