from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from model.feedback import Feedback

feedback_api = Blueprint('feedback_api', __name__, url_prefix='/api')
api = Api(feedback_api)

class FeedbackAPI:
    class _Submit(Resource):
        def post(self):
            try:
                data = request.get_json()
                current_app.logger.debug("📥 Received data: %s", data)

                if not data:
                    return {'message': 'No input data provided'}, 400
                if data.get('sentiment') not in ('up', 'down'):
                    return {'message': 'Sentiment must be "up" or "down"'}, 400
                if not data.get('comment', '').strip():
                    return {'message': 'Comment is required'}, 400

                feedback = Feedback(
                    sentiment=data['sentiment'],
                    comment=data['comment'].strip()
                )
                feedback.create()

                # RETURN A PLAIN DICT, NOT jsonify(...)
                return feedback.read(), 201

            except Exception as e:
                current_app.logger.error("💥 Server error: %s", e, exc_info=True)
                return {'message': 'Internal server error', 'error': str(e)}, 500

# Register the endpoint
api.add_resource(FeedbackAPI._Submit, '/feedback')
