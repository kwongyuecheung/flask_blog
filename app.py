from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required,current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)





class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

# #login functions
# @login_manager.user_loader
# def load_user(username):
#     if username not in User:
#         return
#     user = User()
#     user.username = username
#     return user



class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('index.html', posts = posts)
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    date_posted = post.date_posted.strftime('%B %d,%Y')
    return render_template('post.html',post = post,date_posted = date_posted)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods =['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title = title, subtitle = subtitle, author = author, content = content, date_posted= datetime.now())
    db.session.add(post)
    db.session.commit()
    
    return redirect(url_for('index'))

# @app.route('/login',methods =['POST'])
# def login():
#     # if request.method =='GET':
#     #     return render_template('login.html')
#     inputuser = request.form['inputuserid']
#     if (inputuser in User) and (request.form['password']==User[inputuser]['password']):
#         user = User()
#         user.id = inputuser
#         login_user(user)
#         return redirect(url_for('add.html'))
#     return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)