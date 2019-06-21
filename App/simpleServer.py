from flask import Flask, request, send_from_directory, make_response,jsonify
import psycopg2

def load_src(name, fpath):
    import os, imp
    return imp.load_source(name, os.path.join(os.path.dirname(__file__), fpath))
load_src("connection", "../data_preparation/connection.py")

from connection import Connection

app = Flask(__name__,static_url_path='')

#establish remote db connection

cur = Connection()().cursor()

tweet_query = "select r.create_at,l.top_left_long,l.top_left_lat,l.bottom_right_long,l.bottom_right_lat from records r,locations l where r.id=l.id";

@app.route("/temp")
def send_temp_data():
  resp = make_response(send_from_directory('data','temp.csv'))
  resp.headers['Access-Control-Allow-Origin'] = '*'
  return resp

@app.route("/realtime")
def send_realTime_data():
  resp = make_response(send_from_directory('data','realtime.txt'))
  resp.headers['Access-Control-Allow-Origin'] = '*'
  return resp

@app.route("/tweets")
def send_tweets_data():

  cur.execute(tweet_query);

  d = []

  for row in cur.fetchall():
    object = {}
    object["create_at"] = row[0].isoformat()
    object["long"] = row[1]
    object["lat"]  = row[2]
    d.append(object)

  resp = make_response(jsonify(d))
  resp.headers['Access-Control-Allow-Origin'] = '*'
  return resp


if __name__ == "__main__":
  app.run()
