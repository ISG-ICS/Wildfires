from flask import Flask, send_from_directory, make_response

app = Flask(__name__, static_url_path='')

from data_preparation.connection import Connection

conn = Connection()()


@app.route("/temp")
def send_temp_data():
    resp = make_response(send_from_directory('data', 'temp.csv'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/realtime")
def send_realTime_data():
    resp = make_response(send_from_directory('data', 'realtime.txt'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/tweets")
def send_tweets_data():
    resp = make_response(send_from_directory('data', 'tweets-wildfire.json'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == "__main__":
    app.run()
