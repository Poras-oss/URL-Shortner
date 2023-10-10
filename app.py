from flask import Flask, render_template, request, redirect, jsonify
import hashlib, sqlite3, base64

app = Flask(__name__)

name = "URL Shortening Service"


@app.route("/shortner")
def url_shortner():
    url = request.args.get('url')
    #We have to check if its already exists in database
    lastID = last()
    integer_bytes = lastID.to_bytes((lastID.bit_length() + 7) // 8, byteorder='big')
    base64_encoded = base64.b64encode(integer_bytes).decode('utf-8')

    connect = sqlite3.connect('database.db')
    connect.execute('INSERT into data(url,shortenURL )VALUES(?, ?)', (url, base64_encoded))
    connect.commit()

    return "http://localhost:5000?url="+base64_encoded


@app.route("/")
def index():
    base64 = request.args.get('url')
    if base64:
        #Fetching original url
        connect = sqlite3.connect('database.db')
        cursor = connect.execute('SELECT url FROM data WHERE shortenURL = ?', (base64,))
        url = cursor.fetchone()
        connect.close()
        
        return redirect('http://'+url[0])
        #render_template("index.html", name=url[0])
    else:
        return render_template("index.html")    
   
    



@app.route("/show")
def show():
   connect = sqlite3.connect('database.db')
   cursor =  connect.execute("SELECT * FROM data")
   rows = cursor.fetchall()
   connect.close()
   return render_template("show.html", rows=rows)  


def last():
   connect = sqlite3.connect('database.db')
   cursor =  connect.execute("SELECT COUNT(*) from data")
   rows = cursor.fetchall()
   connect.close()
   return rows[0][0]
