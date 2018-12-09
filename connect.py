from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def index():
    return 'Hello'


@app.route("/v1/piece/value/<string:piece_name>", methods=["GET"])
def get_piece_value(piece_name):
    piece_name = piece_name.lower()
    if piece_name == "king":
        return jsonify({"piece": piece_name, "value": 100000000})
    if piece_name == "queen":
        return jsonify({"piece": piece_name, "value": 9})
    if piece_name == "rook":
        return jsonify({"piece": piece_name, "value": 5})
    if piece_name == "bishop" or piece_name == "knight":
        return jsonify({"piece": piece_name, "value": 3})
    if piece_name == "pawn":
        return jsonify({"piece": piece_name, "value": 1})
    return jsonify({"piece": piece_name, "value": -1})


if __name__ == "__main__":
    app.run(debug=True)
