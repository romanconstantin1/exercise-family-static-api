"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members

    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_family_member(id):
    find_member = jackson_family.get_member(id)
    if "not_found" in find_member[0]:
        return jsonify({"msg": f"A family member with the ID {id} was not found"}), 400

    response_body = {
        "msg": "A family member was found",
        "first_name": find_member[0]["first_name"],
        "id": find_member[0]["id"],
        "age": find_member[0]["age"],
        "lucky_numbers": find_member[0]["lucky_numbers"]
    }
    
    return jsonify(response_body), 200


@app.route('/member', methods=['POST'])
def add_family_member():
    new_request = request.json
    new_member = jackson_family.add_member(new_request)
    if "missing_params" in new_member:
        return jsonify({"msg": "One or more required parameters is missing"}), 400
    
    response = {
        "msg": "New family member added successfully",
        "new_member": f'New family member: {new_member["first_name"]}'
    }
    return jsonify(response), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def remove_family_member(id):
    deleted_member = jackson_family.delete_member(id)
    if "not_found" in deleted_member:
        return jsonify({"msg": f"A family member with the ID {id} was not found"}), 400

    response_body = {
        "msg": "The following family member was deleted:",
        "first_name": deleted_member["first_name"],
        "id": deleted_member["id"],
        "age": deleted_member["age"],
        "lucky_numbers": deleted_member["lucky_numbers"],
        "done": deleted_member["done"]
    }

    print(response_body)
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
