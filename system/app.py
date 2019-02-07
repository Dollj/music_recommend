from flask import Flask,render_template,request,session,redirect,url_for
from flask_pymongo import PyMongo
import base64
from decoration import login_required

app = Flask(__name__)
app.secret_key='cathykey'
app.debug=True
app.config.update(MONGO_URI='mongodb://localhost:27017/nlpcv1')
mongo = PyMongo(app)

#session要求只从登陆界面这个通道进入,。
#和服务端对话的过程，会话。
#cookie在客户端浏览器访问一个网页，浏览器在客户端写下一个文件去保存用户信息和状态，当第二次再访问时候浏览器直接访问过的打开文件，和上一次有联系

#cookie写的信息保存在客户端，容易受攻击，不安全，所以session的技术就出现，把信息保存在服务端，在第一次访问时侯，就是会话刚开始时候保存信息到服务端，这个信息会在整个会话过程中存在，直到会话结束就不存在


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('signin.html')
    else:
        user = request.form.get('user')
        pwd = request.form.get('password')
        #pwd=base64.b64encode(pwd)
        a = mongo.db.mycol.find_one({"username": user,'password':pwd})
        if a:
            session['user_info'] = a['username']  # 如果登陆成功，服务端把user传到user_info中
            return redirect(url_for('layui'))
        else:
            return render_template('signin.html', error='用户名或密码错误')  # 在表格中找不到对象



@app.route('/',methods=['GET'])
def home():
    #session.pop('user_info')
    user = session.get("user_info")#没有登陆直接进入home，user_info就没有值
    print(user)
    if user is None:
        return redirect(url_for('login'))#指向网页
    return render_template('layui.html')#渲染模板


@app.route('/registe',methods=['GET','POST'])
def registe():
    if request.method=='GET':
        return render_template('signup.html')
    else:
        user=request.form.get("user")#点了submit之后的填进去的名字送到了user变量中
        pwd=request.form.get("password")
        email=request.form.get("email")
        pwd1=request.form.get("password1")
        #pwd_result=base64.b64encode(pwd)
        #将加密的密码传到放到user字典，在if中放入数据库
        user_dict = {"username": user, "password": pwd, "email": email, "password1": pwd}
        #user_dict={"username":user,"password":pwd,"email":email,"password1":pwd1}
        if pwd==pwd1:
            a = mongo.db.mycol.find_one({"username": user})#判断姓名唯一性
            if not a:
                mongo.db.mycol.insert_one(user_dict)#将新用户插入到用户表
                return redirect(url_for('login'))
            else:
                return render_template('signup.html',msg="用户已存在")
        else:
            return render_template('signup.html',msg="密码不一致，请重新输入")



@app.route('/layui/',methods=['GET','POST'])
def layui():
    return render_template('layui.html')


@app.route('/music/',methods=['GET','POST'])
def music():
    return render_template('music_recommend.html')


@app.route('/happy/',methods=['GET','POST'])
def happy():
    from tableinput import happy
    table_happy=happy()
    return render_template('happy.html',table_happy=table_happy)

@app.route('/angry/',methods=['GET'])
def angry():
    from tableinput import angry
    table_angry = angry()
    return render_template('angry.html',table_angry=table_angry)

@app.route('/heal/',methods=['GET'])
def heal():
    from tableinput import heal
    table_heal= heal()
    return render_template('heal.html',table_heal=table_heal)

@app.route('/romantic/',methods=['GET'])
def romantic():
    from tableinput import romantic
    table_romantic = romantic()
    return render_template('romantic.html',table_romantic=table_romantic)

@app.route('/sad/',methods=['GET'])
def sad():
    from tableinput import sad
    table_sad = sad()
    return render_template('sad.html',table_sad=table_sad)

@app.route('/encourage/',methods=['GET'])
def encourage():
    from tableinput import encourage
    table_encourage = encourage()
    return render_template('encourage.html',table_encourage=table_encourage)

@app.route('/classify/',methods=['GET','POST'])
def classify():
    from svm import lr
    if request.method=='GET':
        return render_template('music_clf.html')
    else:
        lyric_content=request.form.get('lyric_content')
        lyric_output=lr(lyric_content)
        lyric_record={'input':lyric_content,'output':lyric_output}
        return render_template('music_clf_1.html',lyric_record=lyric_record)



@app.context_processor
def my_context_processor():
    user_id = session.get('user_info')
    if user_id:
        user = mongo.db.mycol.find_one({'username':user_id})
        if user:
            return {'user':user}
    else:
        return { }

if __name__ == '__main__':
    app.run()


