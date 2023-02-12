from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
# database creation
client = MongoClient("mongodb+srv://<your_username>:<your_password>@cluster0.eszou.mongodb.net/?retryWrites=true&w=majority")
soc_db = client["social"]
db=soc_db['admin']
db_rel=soc_db['relation']

# For managing user

@app.route('/user', methods=['Post'])
def create_user():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('first_name')    
    user = {
        "username": username,
        "email": email,
        "password": password,
        "first_name": first_name,
    }
    
    db.insert_one(user)
    return jsonify({"message": "User created"})

@app.route('/user/<user_id>', methods=['Get'])
def get_user(user_id):
    user = db.find_one({"_id": ObjectId(user_id)})
    user["_id"] = str(user["_id"])
    return jsonify(user)

@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    db.update_one({"_id": ObjectId(user_id)}, {"$set": {"username": username, "email": email, "password": password, "first_name": first_name}})
    return jsonify({"message": "User updated"}), 200

@app.route('/user/<user_id>', methods=['Delete'])
def delete_user(user_id):
    # print("hello")
    # print(db.find_one({"_id": ObjectId(user_id)}))
    db.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"message": "User deleted"})


# Relationship Updation

@app.route('/relationship', methods=['POST'])
def create_relationship():
    user1 = request.json.get('user1')
    user2 = request.json.get('user2')

    user3 = db.find_one({"username": user1})
    # print(user3)
    user4 = db.find_one({"username": user2})

    relationship = {
        "user1": user3["first_name"],
        "user2": user4["first_name"],
        "status": "friend"
    }

    db_rel.insert_one(relationship)
    return jsonify({"message": "Relationship created"})

@app.route('/relationship/<relationship_id>', methods=['Get'])
def get_relationship(relationship_id):
    # print(db_rel.find_one({"_id": ObjectId(relationship_id)}))
    relationship = db_rel.find_one({"_id": ObjectId(relationship_id)})
    relationship["_id"] = str(relationship["_id"])
    return jsonify(relationship)


@app.route('/relationship/<relationship_id>', methods=['PUT'])
def update_relationship(relationship_id):
    user1 = request.json.get('user1')
    user2 = request.json.get('user2')
    status = request.json.get('status')
    # print(user1," ",user2," ",status)
    db_rel.update_one({"_id": ObjectId(relationship_id)}, {"$set": {"user1": user1, "user1": user2, "status": status}})
    return "Relationship updated"

@app.route('/relationship/<relationship_id>', methods=['DELETE'])
def delete_relationship(relationship_id):
    # print(db_rel.find_one({"_id": ObjectId(relationship_id)}))
    db_rel.delete_one({"_id": ObjectId(relationship_id)})
    return "Relationship deleted"

# tested all api using Postman
if __name__ == "__main__":
    app.run()
