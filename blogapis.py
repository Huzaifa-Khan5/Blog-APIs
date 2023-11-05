from flask import Flask,render_template,request,jsonify
import psycopg2
import psycopg2.extras
from psycopg2 import sql

hostname='localhost'
database='Blog'
username='postgres'
pwd='DaMai69!'
port_id=5432
conn=None
cur=None

app = Flask(__name__)

@app.route('/register',methods=['POST'])
def register():
    if request.method=='POST':
        request_data=request.get_json()

    get_email=request_data['email']
    get_password=request_data['password']

    conn=psycopg2.connect(host=hostname,
                            dbname=database,
                            user=username,
                            password=pwd,
                            port=port_id)
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    loginQuery = sql.SQL("select email from {table} where {pkey} = %s").format(table=sql.Identifier('users'),pkey=sql.Identifier('email'))

    cur.execute(loginQuery, (get_email,))
    userdetails=cur.fetchall()
    print(userdetails)
    if len(userdetails)>0:
        return 'email already exists'
        
    create_script = '''CREATE TABLE IF NOT EXISTS users(
                        sno    SERIAL PRIMARY KEY,
                        email  varchar(100) UNIQUE NOT NULL,
                        password   varchar(100) NOT NULL)
                        '''
    cur.execute(create_script)

    cur.execute('INSERT INTO users(email,password) VALUES(%s,%s)',(get_email,get_password))

    conn.commit()

    cur.close()
    conn.close()

    return ''

@app.route('/login',methods=['POST'])
def login():
    if request.method=='POST':
        request_data=request.get_json()

    get_email=request_data['email']
    get_password=request_data['password']

    conn=psycopg2.connect(host=hostname,
                            dbname=database,
                            user=username,
                            password=pwd,
                            port=port_id)
        
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    loginQuery = sql.SQL("SELECT * FROM {table} WHERE {email} = %s AND {password} = %s").format(
    table=sql.Identifier('users'),
    email=sql.Identifier('email'),
    password=sql.Identifier('password'))
    cur.execute(loginQuery, (get_email, get_password))
    if cur.fetchone():
        return "Login successful"
    else:
        return "Invalid credentials"

@app.route('/addblog',methods=['POST'])
def add_blog():
    if request.method=='POST':
        request_data=request.get_json()

    blog_title=request_data['title']
    blog_content=request_data['content']

    conn=psycopg2.connect(host=hostname,
                        dbname=database,
                        user=username,
                        password=pwd,
                        port=port_id)
    cur=conn.cursor()

    create_script='''CREATE TABLE IF NOT EXISTS posts(
                     sno    SERIAL PRIMARY KEY,
                     title  varchar(100 NOT NULL,
                     content   varchar(100) NOT NULL,
                     date   TIMESTAMP NOT NULL DEFAULT NOW()) 
                     '''
    cur.execute(create_script)
        
    cur.execute('INSERT INTO posts(title,content) VALUES(%s,%s)',(blog_content,blog_title))

    conn.commit()

    cur.close()
    conn.close()

    return 'success'

@app.route('/blog',methods=['POST'])
def get_comment():
    if request.method=='POST':
        request_data=request.get_json()

    name=request_data['name']
    comment=request_data['comment']

    conn=psycopg2.connect(host=hostname,
                        dbname=database,
                        user=username,
                        password=pwd,
                        port=port_id)
        
    cur=conn.cursor()

    create_script='''CREATE TABLE IF NOT EXISTS comments(
                        sno    SERIAL PRIMARY KEY,
                        name  varchar(100) NOT NULL,
                        comment   varchar(100) NOT NULL,
                        date   TIMESTAMP NOT NULL DEFAULT NOW()) 
                        '''
    cur.execute(create_script)

    cur.execute('INSERT INTO comments(name,comment) VALUES(%s,%s)',(name,comment))

    conn.commit()

    cur.close()
    conn.close()

    return 'coment added successfully'


if __name__ =="__main__":
    app.run(debug=True)