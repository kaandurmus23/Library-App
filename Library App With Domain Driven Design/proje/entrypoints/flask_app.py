from flask import Flask, request, jsonify
from proje.service_layer.application_service import (
    create_and_add_book,
    create_and_add_member,
    borrow_book_for_member,
    return_book_for_member
)
from sqlalchemy import create_engine
from proje.adapters.orm import metadata, start_mappers
from proje.config import Config

app = Flask(__name__)

app.config.from_object(Config)

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
metadata.create_all(engine)
start_mappers()

@app.route("/add_book", methods=["POST"])
def add_book():
    data = request.json
    book_id = create_and_add_book(data["name"])
    return jsonify({"message": "Book added", "book_id": book_id}), 201

@app.route("/add_member", methods=["POST"])
def add_member():
    data = request.json
    member_id = create_and_add_member(data["name"])
    return jsonify({"message": "Member added", "member_id": member_id}), 201

@app.route("/borrow_book", methods=["POST"])
def borrow_book():
    data = request.json
    if borrow_book_for_member(data["book_id"], data["member_id"]):
        return jsonify({"message": "Book borrowed"}), 201
    return jsonify({"message": "Borrow operation failed"}), 400

@app.route("/return_book", methods=["POST"])
def return_book():
    data = request.json
    if return_book_for_member(data["book_id"], data["member_id"]):
        return jsonify({"message": "Book returned"}), 200
    return jsonify({"message": "Return operation failed"}), 400

if __name__ == "__main__":
    app.run(debug=True)
