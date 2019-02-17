from flask import Flask,request,redirect,url_for,session
from flask import render_template
from models import Article,Liuyan,User
from exts import db
import config
from functools import wraps


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

def login_require(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
    user_id = session.get('user_id')
    if request.method == 'GET':
        return render_template('admin.html')
    else:
        user = User.query.filter(User.id == user_id).first().name
        if user=='Admin':
            biaoti = request.form.get('biaoti')
            boke = request.form.get('boke')
            syzs = request.form.get('boke')
            fmdz = request.form.get('fmdz')
            bkdz = request.form.get('bkdz')
            content = Article(biaoti=biaoti,neirong=boke,fmdz=fmdz,nrdz=bkdz,syzs=syzs)
            db.session.add(content)
            db.session.commit()
            return redirect(url_for('index'))

        else:
            return '权限不足！'


@app.route('/detail/<id>/',methods=['GET','POST'])
def detail(id):
    if request.method == 'GET':
        question_model = Article.query.filter(Article.id == id).first()
        return render_template('details.html', ques=question_model)


@app.context_processor
def my_context():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id==user_id).first()
        if user:
            return {'user':user}
    return { }

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/index')
def index():
    context = {
        'blog': Article.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/message',methods=['GET','POST'])
def message():
    user_id = session.get('user_id')
    if request.method == 'GET':
        context = {
            'liuyan':Liuyan.query.all()
            }
        return render_template('message.html',**context)
    else:
        if user_id:
            liuyan = request.form.get('liuyan')
            user = User.query.filter(User.id == user_id).first().name
            if user:
                liuyan1 = Liuyan(content=liuyan,name=user)
                db.session.add(liuyan1)
                db.session.commit()
                return redirect(url_for('message'))
        else:
            return '请先登录后才能留言哦！'



@app.route('/zhuce',methods=['GET','POST'])
def zhuce():
    if request.method=='GET':
        return render_template('zhuce.html')
    else:
        name = request.form.get('name')
        passwd1 = request.form.get('passwd1')
        passwd2 = request.form.get('passwd2')
        user = User.query.filter(User.name==name).first()
        if user:
            return '不好意思，这个昵称已经有啦！'
        else:
            if passwd1==passwd2:
                user = User(name=name,password=passwd1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                return '两次输入的密码不一致！'



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form.get('nichen')
        password = request.form.get('mima')
        user = User.query.filter(User.name == name, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return '密码输入错了( •̀ ω •́ )'


if __name__ == '__main__':
    app.run()
