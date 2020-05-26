import json

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/echo', methods=['POST'])
def foo():
    data = request.json

    echo_ = data['echo']
    bytes_ = bytes(echo_, 'utf-16')
    bytes_str = bytes_.__str__()
    return jsonify(echo=bytes_str)


if __name__ == "__main__":
    app.run()
