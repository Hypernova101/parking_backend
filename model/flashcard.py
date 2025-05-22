from __init__ import db, app
from sqlalchemy.exc import IntegrityError

class Flashcard(db.Model):
    __tablename__ = 'flashcards'

    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(255), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    lesson_id = db.Column(db.Integer, nullable=False)  # Link to specific lesson content

    def __init__(self, term, definition, lesson_id):
        self.term = term
        self.definition = definition
        self.lesson_id = lesson_id

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        return {
            "id": self.id,
            "term": self.term,
            "definition": self.definition,
            "lesson_id": self.lesson_id
        }

    def update(self, data):
        self.term = data.get('term', self.term)
        self.definition = data.get('definition', self.definition)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def restore(data):
        for card_data in data:
            card_id = card_data.pop('id', None)
            if card_id:
                flashcard = Flashcard.query.get(card_id)
                if flashcard:
                    flashcard.update(card_data)
                else:
                    flashcard = Flashcard(**card_data)
                    flashcard.create()
            else:
                flashcard = Flashcard(**card_data)
                flashcard.create()

def initFlashcards():
    with app.app_context():
        db.create_all()