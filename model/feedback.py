from __init__ import db, app
from sqlalchemy.exc import IntegrityError

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    sentiment = db.Column(db.String(10), nullable=False)
    comment = db.Column(db.String(255), nullable=False)

    def __init__(self, sentiment, comment):
        self.sentiment = sentiment
        self.comment = comment

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def read(self):
        return {
            "id": self.id,
            "sentiment": self.sentiment,
            "comment": self.comment
        }



    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

def init_feedback():
    """
    Create the feedback table (if needed).
    """
    with app.app_context():
        db.create_all()