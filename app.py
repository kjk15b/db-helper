from flask import Flask, request
import sys

app = Flask(__name__)
dataStream = {"UR" : list(),
              "UL" : list(),
              "LR" : list(),
              "LL" : list()}
upperLimit = 100

app.route("/")
def home():
    return "Hello World"

app.route('/data/ingest/<sensor>', methods=["POST"])
def ingestRoute(sensor):
    if request.method == "POST":
        data = request.form.to_dict()
        value = data['data']
        print("Received: {} {} Hz".format(sensor, value))
        if len(dataStream[sensor]) > upperLimit:
            dataStream[sensor].pop(0)
        dataStream[sensor].append(value)
        return "Received - Got it"
    return "Nothing to see here"



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",
    port=5050)