from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/can_move", methods=["POST", "OPTIONS"])
def can_move():
    req = request.get_json()
    print(req)
    if req and "test" in req:
        print(req["test"])
    return jsonify("ACK")


if __name__ == "__main__":
    app.run(debug=True)
