from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:123456@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text())

    def __init__(self, title, content):
        self.title = title
        self.content = content

@app.route('/blog', methods=['GET'])
def index():

    if request.args.get('post_id'):
        post_id = request.args.get('post_id')
        post = Post.query.get(post_id)

        return render_template('post.html', 
            title = "It's a blog!", 
            post_title = post.title, 
            content = post.content)

    posts = Post.query.all()
    
    return render_template('posts.html',
        title="It's a Blog!", 
        posts=posts)

@app.route('/newpost', methods=['GET','POST'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        contents = request.form['contents']
        post = Post(title, contents)
        db.session.add(post)
        db.session.commit()
        return render_template('post.html', 
            title = "It's a blog!", 
            post_title = post.title, 
            content = post.content)

    return render_template('add.html', 
        title = "Add a Blog Entry!")

if __name__ == '__main__':
    app.run()