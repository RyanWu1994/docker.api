from flask import Flask , json, jsonify ,make_response , request
import logging
import mysql.connector
import os


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


test_useri = {
   "name": "Siang",
   "job_title": "SRE",
   "communicate_information": {
     "email": "asuna900717@gmail.com",
     "mobile": "0920-790-312"
   }
 }

mydb = mysql.connector.connect(
  #host=os.environ['HOST_IP'],
  host="192.168.0.12",
  user="admin",
  #password=os.environ['MYSQL_PASSWORD'],
  password="Pn123456",
  database="Testdb",
  connect_timeout=1000,
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS userinfo (id INT AUTO_INCREMENT PRIMARY KEY , name VARCHAR(255) , job_title VARCHAR(255), email VARCHAR(255), mobile VARCHAR(255))")
mycursor.close()

mydb.commit()
mydb.close()



def rows_to_json(cols,rows):
    result = []
    for row in rows:
        data = dict(zip(cols, row))
        result.append(data)
    return json.dumps(result, default=type_handler)

def db_connection(f_host,f_user,f_password,f_database):
    db_con = mysql.connector.connect(
      host=f_host,
      user=f_user,
      password=f_password,
      database=f_database,
      connect_timeout=1000,
    )
    return db_con

global_con = db_connection("192.168.0.12","admin","Pn123456","Testdb")

logging.info('Starting to running API server')

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello Flask API Example!</h1>"

@app.route('/user', methods=['GET'])
def user_all():
    try: 
      get_cursor = global_con.cursor()
      get_cursor.execute("SELECT * FROM userinfo")
      get_result = get_cursor.fetchall()
      users = []
      for entry in get_result:
          record = {
            'id': entry[0],
            'name': entry[1],
            'job_title': entry[2],
            "communicate_information": {
              "email": entry[3],
              "mobile": entry[4],
            }
          }
          users.append(record)

      get_cursor.close()
      res = make_response(jsonify(users), 200)
      #res = make_response(jsonify(test_useri), 200)
      return res
      #return jsonify(test_useri)
    except Exception as e:
      return {'error': str(e)}

@app.route('/user', methods=["POST"])
def add_user():
    try: 
        data = request.get_json()
        if data and "name" in data:
          names = data["name"]
        else:
            names = "Nonename"
      
        if data and "job_title" in data:
              job_title = data["job_title"]
        else:
            job_title = "Nonetitle"
      
        if data and "email" in data:
            email = data["email"]
        else:
            email = "Noneemail"

        if data and "mobile" in data:
            mobile = data["mobile"]
        else:
            mobile = "Nonemobile"

        add_user_cursor = global_con.cursor()
        sql = "INSERT INTO userinfo (name, job_title , email , mobile) VALUES (%s,%s,%s,%s)"
        val = (names, job_title,email,mobile)
        add_user_cursor.execute(sql, val)
        add_user_cursor.close()
        global_con.commit()

        res = make_response(jsonify(data), 200)
        return res
    except Exception as e:
        return {'error': str(e)}
@app.route('/user', methods=["PUT"])
def update_user():
    try: 
        sql = "UPDATE userinfo SET "
        data = request.get_json()

        if data and "id" in data:
          ids = data["id"]
        else:
          res = make_response(jsonify({'StatusCode':'user id  is not found'}), 404)
          return res      
        if data and "name" in data:
          names = data["name"]
          sql = "UPDATE userinfo SET name = \""+names + "\" WHERE id = "+ids
      
        if data and "job_title" in data:
          job_title = data["job_title"]
          sql = "UPDATE userinfo SET job_title = \""+job_title + "\" WHERE id = "+ids
      
        if data and "email" in data:
            email = data["email"]
            sql = "UPDATE userinfo SET email = \""+email + "\" WHERE id = "+ids

        if data and "mobile" in data:
            mobile = data["mobile"]
            sql = "UPDATE userinfo SET mobile = \""+mobile + "\" WHERE id = "+ids

        update_cursor = global_con.cursor()
        
        logging.info(sql)
        update_cursor.execute(sql)
        update_cursor.close()
        global_con.commit()

        res = make_response(jsonify({'StatusCode':'user updated success'}), 200)
        return res
    except Exception as e:
        return {'error': str(e)}

@app.route('/user/<id>', methods=["DELETE"])
def delete_user(id):
    try: 
        print(type(id),id)
        # Parse the arguments
        #req_id = request.values.get('id')
        delete_cursor = global_con.cursor()
        sql = "DELETE FROM userinfo WHERE id = " + id
        delete_cursor.execute(sql)
        global_con.commit()

        return {'StatusCode':'user deleted'}

    except Exception as e:
        return {'error': str(e)}

app.run(debug=True, host='127.0.0.1', port=8888)