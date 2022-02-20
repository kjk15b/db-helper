from flask import Flask, request
import sys

app = Flask(__name__)
dataStream = {"UR" : list(),
              "UL" : list(),
              "LR" : list(),
              "LL" : list()}
upperLimit = sys.argv[4]


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
    app.run(debug=sys.argv[1], host=sys.argv[2],
    port=sys.argv[3])