from flask import Flask, render_template, request, redirect, url_for
from models import db, BlogPost
import os

app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://myuser:mypassword@db:5432/mywebsite'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация БД
db.init_app(app)

# Создание таблиц при первом запуске
with app.app_context():
    db.create_all()

# Главная страница
@app.route('/')
def home():
    return render_template('index.html')

# О нас
@app.route('/about')
def about():
    return render_template('about.html')

# Контакты
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Блог - список постов
@app.route('/blog')
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

# Просмотр отдельного поста
@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    
    # Увеличиваем счётчик просмотров
    post.views += 1
    db.session.commit()
    
    return render_template('blog_post.html', post=post)

# Создание нового поста (простая форма)
@app.route('/blog/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author', 'Аноним')
        
        if title and content:
            new_post = BlogPost(title=title, content=content, author=author)
            db.session.add(new_post)
            db.session.commit()
            
            return redirect(url_for('blog'))
    
    return render_template('blog.html', create_mode=True)

# Удаление поста
@app.route('/blog/delete/<int:post_id>')
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    
    return redirect(url_for('blog'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)