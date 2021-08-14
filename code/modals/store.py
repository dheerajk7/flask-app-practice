import sqlite3
from db import db

class StoreModal(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModal', lazy='dynamic')

    def __init__(self, name) -> None:
        self.name = name

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #return item modal object

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def get_json(self):
        return {'name': self.name, 'items': [item.get_json() for item in self.items.all()]}

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

