from datetime import datetime
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy


db_dir = Path(__file__).parent
db_file = db_dir / Path('funt.sqlite')
db = SQLAlchemy()


class Exam(db.Model):
    __tablename__ = 'exam'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'<Exam {self.id}>'
