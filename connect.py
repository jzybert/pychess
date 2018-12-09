from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def index():
    return 'Hello'


@app.route("/v1/piece/value/<string:piece_name>", methods=["GET"])
def get_piece_value(piece_name):
    piece_name = piece_name.lower()

    def format_json(value):
        return jsonify({"piece": piece_name, "value": value})

    if piece_name == "king":
        return format_json(100000000)
    if piece_name == "queen":
        return format_json(9)
    if piece_name == "rook":
        return format_json(5)
    if piece_name == "bishop" or piece_name == "knight":
        return format_json(3)
    if piece_name == "pawn":
        return format_json(1)
    return format_json(-1)


if __name__ == "__main__":
    app.run(debug=True)
