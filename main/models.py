from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    tovars = db.relationship('Tovar', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Tovar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    photo = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Tovar {self.title}>'

