from flask import Flask,render_template,request,jsonify
import psycopg2
import psycopg2.extras
from psycopg2 import sql
from  werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

hostname='localhost'
database='Blog'
username='postgres'
pwd='DaMai69!'
port_id=5432
conn=None
cur=None

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'DaMai69!'  # Change this to your own secret key
jwt = JWTManager(app)

@app.route('/register',methods=['POST'])
def register():
    if request.method=='POST':
        request_data=request.get_json()

    get_username=request_data["username"]
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
                        username varchar(100) NOT NULL,
                        email  varchar(100) UNIQUE NOT NULL,
                        password   varchar(1000) NOT NULL)
                        '''
    cur.execute(create_script)

    cur.execute('INSERT INTO users(username,email,password) VALUES(%s,%s,%s)',(get_username,get_email,generate_password_hash(get_password)))

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


    loginQuery = sql.SQL("SELECT * FROM {table} WHERE {email} = %s ").format(
    table=sql.Identifier('users'),
    email=sql.Identifier('email'))

    cur.execute(loginQuery, (get_email, ))
    
    
    gotData = cur.fetchone()
    #print(gotData)
    if gotData!=None:
        if check_password_hash(gotData[-1],get_password):
            access_token = create_access_token(identity={"key":gotData[0]})
            return jsonify(access_token=access_token), 200
            #return "Login successful"
        else:
            return "Invalid credentials"
    else:
        return "no user found"

@app.route('/addblog',methods=['POST'])
@jwt_required()
def add_blog():
    if request.method=='POST':
        request_data=request.get_json()

    blog_title=request_data['title']
    blog_content=request_data['content']
    data_from_token=get_jwt_identity()

    conn=psycopg2.connect(host=hostname,
                        dbname=database,
                        user=username,
                        password=pwd,
                        port=port_id)
    cur=conn.cursor()


    create_script='''CREATE TABLE IF NOT EXISTS posts(
                     sno    SERIAL PRIMARY KEY,
                     title  varchar(100) NOT NULL,
                     content   varchar(100) NOT NULL,
                     user_key   int NOT NULL,
                     date   TIMESTAMP NOT NULL DEFAULT NOW()) 
                     '''
    cur.execute(create_script)
        
    cur.execute('INSERT INTO posts(title,content,user_key) VALUES(%s,%s,%s)',(blog_content,blog_title,data_from_token["key"]))

    conn.commit()

    cur.close()
    conn.close()

    return 'success'

@app.route('/addcomments',methods=['POST'])
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