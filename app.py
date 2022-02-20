from flask import Flask, request
import sys
import requests

app = Flask(__name__)
dataStream = {"UR" : list(),
              "UL" : list(),
              "LR" : list(),
              "LL" : list()}
upperLimit = sys.argv[4]
daq = sys.argv[5]
port = sys.argv[6]

def attemptDeliver():
    backupStream = dataStream
    for key in dataStream.keys():
        url = "http://{}:{}/data/ingest/{}".format(daq, port, key)
        for i in range(len(dataStream[key])):
            try:
                feedBack = requests.post(url, data={'data' : dataStream[key][i]})
                print("FEEDBACK=\n \
                        \tStatus={}\n \
                        \tHeaders={}\n \
                        \tElapsed={}\n \
                        \tRequest={}".format(feedBack.status_code, feedBack.headers,
                        feedBack.elapsed, feedBack.request.body))
                backupStream[key].pop(i)
            except:
                print("Could not deliver to: {}".format(url))
    dataStream = backupStream


@app.route('/data/ingest/<sensor>', methods=["POST"])
def ingestRoute(sensor):
    if request.method == "POST":
        data = request.form.to_dict()
        value = data['data']
        print("Received: {} {} Hz".format(sensor, value))
        if len(dataStream[sensor]) > upperLimit:
            dataStream[sensor].pop(0)
        dataStream[sensor].append(value)
        attemptDeliver()
        return "Received - Got it"
    return "Nothing to see here"



if __name__ == '__main__':
    app.run(debug=sys.argv[1], host=sys.argv[2],
    port=sys.argv[3])