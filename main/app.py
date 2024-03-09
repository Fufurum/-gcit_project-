from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Category, Tovar
from werkzeug.utils import secure_filename
import os




app = Flask(__name__)
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = './static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tovornyak.db'
app.config['SECRET_KEY'] = 'vladislav_secret_key_2024'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)


@app.route('/')
def index():
    tovars = Tovar.query.all()
    return render_template('index.html', tovars=tovars)
    

@app.route('/tovar/<int:tovar_id>')
def tovar(tovar_id):
    tovar = Tovar.query.get_or_404(tovar_id)
    return render_template('tovar.html', tovar=tovar)

@app.route('/category/<int:category_id>')
def category(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template('category.html', category=category)

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        price = request.form['price']
        category_id = request.form['category']
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo = file.filename
            tovar = Tovar(title=title, content=content, price=price,category_id=category_id,photo=photo)
            db.session.add(tovar)
            db.session.commit()
        
        
   
    categories = Category.query.all()
    return render_template('add.html', categories=categories)

@app.route('/edit/<int:tovar_id>', methods=['GET', 'POST'])
def edit(tovar_id):
    tovar = Tovar.query.get_or_404(tovar_id)
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo = file.filename
            tovar.title = request.form['title']
            tovar.content = request.form['content']
            tovar.category_id = request.form['category']
            tovar.price = request.form['price']
            tovar.photo = photo
            db.session.commit()
    categories = Category.query.all()
    return render_template('edit.html', tovar=tovar, categories=categories)

@app.route('/delete/<int:tovar_id>', methods=['GET', 'POST'])
def delete(tovar_id):
    tovar = Tovar.query.get_or_404(tovar_id)
    if request.method == 'POST':
        db.session.delete(tovar)
        db.session.commit()
        flash('Товар удален')
        return redirect(url_for('index'))
    return render_template('delete.html', tovar=tovar)

if __name__ == '__main__':
    app.run(debug=True)

