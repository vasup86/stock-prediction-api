
from flask import Flask, abort, request, jsonify
from flask_cors import CORS, cross_origin


from forecast import predict


app = Flask(__name__)

CORS(app)

@app.route('/predict', methods=['POST'], strict_slashes=False)
@cross_origin()
def forecast():
    # get the ticker from the payl
    ticker = request.json['ticker'].upper()
    
    result = predict(ticker)

    # throw error 400 if no data
    if result  == 'No data':
        return jsonify({"errorType": 406, "message": result}), 406

    return jsonify({"result": result})


@app.route('/')
def homepage():
    return jsonify({"result":"connected"})


if __name__ == '__main__':
    app.run(debug=True)
