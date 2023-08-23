import mysql.connector
import json
import flask 

def getConntection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="root",
        password="root",
        database="contact_app"
        )
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE if not exists USERS (name VARCHAR(255), email VARCHAR(255), phone VARCHAR(20))")
    cursor.execute("CREATE TABLE if not exists LOGIN (username VARCHAR(255), password VARCHAR(30), created datetime not null default(current_timestamp))")
    cursor.execute("CREATE TABLE if not exists SESSION_METADATA (session_id INT(6)  NOT NULL AUTO_INCREMENT, username VARCHAR(255), starttime datetime not null default(current_timestamp), endtime datetime, PRIMARY KEY(session_id)) ")
    
    return conn

def is_valid(username,password):
    sql = "SELECT password from Login where username='{usr}'".format(usr=username)

    conn=getConntection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result_set = cursor.fetchall()
    if password==result_set[0][0]:
        cursor.execute("INSERT INTO SESSION_METADATA (username) VALUES ('{usr}')".format(usr=username))
        conn.commit()
        return True
    else:
        return False


def saveContact(name,email,phone):
    sql = "INSERT INTO USERS (name, email,phone) VALUES (%s, %s,%s)"
    val = (name,email,phone )
    conn=getConntection()
    cursor = conn.cursor()
    cursor.execute(sql, val)
    conn.commit()
    conn.close()

def registerUser(username,password):
    sql = "INSERT INTO LOGIN (username, password) VALUES (%s, %s)"
    val = (username,password )
    conn=getConntection()
    cursor = conn.cursor()
    cursor.execute(sql, val)
    conn.commit()
    conn.close()

def fetchContact():
    sql = "SELECT * from USERS"
    conn=getConntection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    conn.close()
    return flask.jsonify(result)



def sessionendTime(user):
    sql = "UPDATE SESSION_METADATA SET endtime = CURRENT_TIMESTAMP() WHERE username='{usr}' and endtime is null".format(usr=user)
    conn=getConntection()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()