from flask import Flask, request, send_from_directory, make_response
import psycopg2

app = Flask(__name__,static_url_path='')

#establish remote db connection
conn = psycopg2.connect(dbname='testdb', user='tester', password='testpassword', host='52.53.237.95', port='5432', sslmode='require')
cur = conn.cursor()


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
  resp = make_response(send_from_directory('data','tweets-wildfire.json'))
  resp.headers['Access-Control-Allow-Origin'] = '*'
  return resp


if __name__ == "__main__":
  app.run()
