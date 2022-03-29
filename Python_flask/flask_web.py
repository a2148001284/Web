import sys
sys.path.append("./packet")
import flask
import pymysql
from flask import Flask, request

app=Flask(__name__,
          static_url_path='/static',
          static_folder='static',
          template_folder='templates'
          )

@app.route('/')
def index():
    return flask.render_template("index.html")


#功能1：登录部分
@app.route('/login')
def login():
    return flask.render_template("login.html")
    pass

@app.route('/login_address',methods=['POST'])
def login2():
    login_name=str(request.form.get('username'))
    login_pass=str(request.form.get('password'))
    db=pymysql.connect(host="localhost",user="root",password="201922",db="flask2")
    cur=db.cursor()
    sql="""SELECT * FROM student where username='%s' and password='%s' """%(login_name,login_pass)
    cur.execute(sql)
    a=cur.fetchone()
    if a[0]==None and a[1]==None and a[2]==None:
        return "login failed,please try again!!!"
    else:
        #登录成功 接下来设置一下cookie
        response=flask.make_response('login success!! please refer to /login_result')
        response.set_cookie('id',str(a[0]),max_age=150)
        response.set_cookie('username',str(a[1]),max_age=150)
        response.set_cookie('password',str(a[2]),max_age=150)
        return response
    pass

@app.route('/login_result')
def login3():
    if request.cookies.get('id')==None or request.cookies.get('username')==None or request.cookies.get('password')==None:
        response=flask.make_response('your accounts have not been logined!!please login first!')
        return response
    user_id=request.cookies.get('id')
    user_name=request.cookies.get('username')
    user_password=request.cookies.get('password')
    return flask.render_template("login_results.html",a=user_id,b=user_name,c=user_password)
    pass

@app.route('/login_out')
def login4():
    response=flask.make_response('login out success!!! cookies have been removed!')
    response.delete_cookie('id')
    response.delete_cookie('username')
    response.delete_cookie('password')
    return response
    pass

#功能2：查部分
@app.route('/search',methods=['GET'])
def search():
    username=request.args.get('uname')
    db = pymysql.connect(host="localhost", user="root", password="201922", db="flask2")
    cur=db.cursor()
    sql="""SELECT * FROM student where username='%s' """%(username)
    cur.execute(sql)
    #print(cur.fetchall())  #查询所有找到的结果 全部输出
    print(cur.fetchone()) #每次仅输出一条
    #print(cur.fetchmany(2))  #指定查询的条数 这里是2条
    #每次执行指针是不会复位的 如果需要复位 cur.scroll(0,mode="absolute") 这是绝对位置 指针回到0
    #cur.scroll(2,mode="relative") 这里是相对复位 正数则向下几个 负数则向上几个
    if cur.fetchone()==None:
        return "Search Failes!!"
    else:
        return "search successfully!!!"

#功能3：插入部分 新用户的注册功能
@app.route('/insert1')
def insert1():
    return flask.render_template("insert.html")
    pass

@app.route('/insert',methods=['POST'])
def consider_page():
    user_name=str(request.form.get('uname'))
    user_pass=str(request.form.get('passwd'))
    print("you have input the username:"+user_name)
    print("you have input the password"+user_pass)
    db=pymysql.connect(host="localhost",user="root",password="root",db="flask2")
    cur=db.cursor()
    sql="""INSERT INTO student(username,password)VALUES('%s','%s')"""%(user_name,user_pass)
    cur.execute(sql)
    db.commit()
    db.close()
    return "the user has been inserted successfully"
    pass


#功能4 修改用户的密码
@app.route('/update')
def update1():
    if request.cookies.get('id')!=None and request.cookies.get('username')!=None and request.cookies.get('password')!=None:
        a=str(request.cookies.get('id'))
        b=str(request.cookies.get('username'))
        c=str(request.cookies.get('password'))
        return flask.render_template("update.html",userid=a,username=b,password=c)
    else:
        response=flask.make_response("your login is failed,please login first to update your cookies!")
        return response

'''@app.route('/update_address',methods=['POST'])
def update2():
    old_password=str(request.form.get('pass1'))
    new1_password=str(request.form.get('pass2'))
    new2_password=str(request.form.get('pass3'))'''
    #验证逻辑1 通过将旧密码和cookie中的密码进行比对即可
'''    if old_password!=str(request.cookies.get('password')):
        response=flask.make_response('your old_password is wrong!please try again!')
        return response
    if new1_password !=new2_password:
        response=flask.make_response('your new password is different from each other,please try again!!')
        return response
    db=pymysql.connect(host="localhost",user="root",password="201922",db="flask2")
    cur=db.cursor()
    temp=str(request.cookies.get('username'))
    temp2=str(request.cookies.get('id'))
    sql="""UPDATE student SET password='%s' WHERE username='%s' and id='%s' """%(new2_password,temp,temp2)
    cur.execute(sql)
    a=cur.fetchone()
    #print(cur.fetchone())  如果更新语句执行成功 此处结果为None
    if a[0]==None:
        response=flask.make_response('update successfully!!!')
        return response
    else:
        response=flask.make_response('Unknown Error!')
        return response'''

    #验证逻辑2 验证旧密码和数据库中的密码的值

@app.route('/update_address',methods=['POST'])
def update2():
    #验证逻辑3 验证旧密码和数据库以及cookie中的值 但凡三者有一者不同 则可以认为存在问题 甚至cookie被篡改
    old_password = str(request.form.get('pass1'))
    new1_password = str(request.form.get('pass2'))
    new2_password = str(request.form.get('pass3'))
    a=str(request.cookies.get('username'))
    b=str(request.cookies.get('password'))
    c=str(request.cookies.get('id'))
    db = pymysql.connect(host="localhost", user="root", password="201922", db="flask2")
    cur = db.cursor()
    sql="""SELECT * FROM student WHERE username='%s' """%(a)
    cur.execute(sql)
    d=cur.fetchone()
    if old_password!=str(request.cookies.get('password')):
        response1=flask.make_response('your old_password is wrong!please try again!')
        return response1
    if new1_password !=new2_password:
        response2=flask.make_response('your new password is different from each other,please try again!!')
        return response2
    if old_password==d[2] and d[2]==b:
        sql2="""UPDATE student SET password='%s' WHERE username='%s' and id='%s' """%(new2_password,a,c)
        cur.execute(sql2)
        if cur.fetchone()==None:
            response3=flask.make_response('update successfully!!!')
            return response3
        else:
            response5=flask.make_response('Unknown Error!!!')
            return response5
    else:
        response4=flask.make_response('your cookies have been hacked or old_password is wrong! please try again!!')
        return response4



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8899,debug=True)



