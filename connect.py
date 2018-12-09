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


@app.route("/v1/board/init", methods=["GET"])
def init_board():

    def piece(name, color, row, col):
        return {"piece": name, "color": color, "row": row, "col": col}
    pieces = [
        piece("rook", "white", "1", "h"), piece("knight", "white", "1", "g"),
        piece("bishop", "white", "1", "f"), piece("king", "white", "1", "e"),
        piece("queen", "white", "1", "d"), piece("bishop", "white", "1", "c"),
        piece("knight", "white", "1", "b"), piece("rook", "white", "1", "a"),
        piece("pawn", "white", "2", "h"), piece("pawn", "white", "2", "g"),
        piece("pawn", "white", "2", "f"), piece("pawn", "white", "2", "e"),
        piece("pawn", "white", "2", "d"), piece("pawn", "white", "2", "c"),
        piece("pawn", "white", "2", "b"), piece("pawn", "white", "2", "a"),
        piece("pawn", "black", "7", "h"), piece("pawn", "black", "7", "g"),
        piece("pawn", "black", "7", "f"), piece("pawn", "black", "7", "e"),
        piece("pawn", "black", "7", "d"), piece("pawn", "black", "7", "c"),
        piece("pawn", "black", "7", "b"), piece("pawn", "black", "7", "a"),
        piece("rook", "black", "8", "h"), piece("knight", "black", "8", "g"),
        piece("bishop", "black", "8", "f"), piece("king", "black", "8", "e"),
        piece("queen", "black", "8", "d"), piece("bishop", "black", "8", "c"),
        piece("knight", "black", "8", "b"), piece("rook", "black", "8", "a")
    ]
    return jsonify({"board": pieces, "turn": "white", "number_of_moves": "0",
                    "list_of_moves": []})


if __name__ == "__main__":
    app.run(debug=True)
