from flask import Flask
from models import Tovar, Category, db




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tovornyak.db'
db.init_app(app)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Создаем категории
        mebel_category = Category(name='Мебель')
        ode_category = Category(name='Одежда')
        teh_category = Category(name='Бытовая техника')
        prod_category = Category(name='Продукты')
        auto_category = Category(name='Машины')



        db.session.add(mebel_category)
        db.session.add(ode_category)
        db.session.add(teh_category)
        db.session.add(prod_category)
        db.session.add(auto_category)

        db.session.commit()
        print('Созданы категории Мебель, Одежда,Продукты ,Машины  и Бытовая техника')

    print('Создана база данных tovornyak')
