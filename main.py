from flask import Flask, request, jsonify
# from functools import filter

app = Flask(__name__)

users = [
    {"id": 1,"name": "john", "isActive": True},
    {"id": 2,"name": "jane", "isActive": True}
]

booleanMap = {"True": True, "False": False}

@app.route("/users")
def getUsers():
    return users

def findUserById(id: str):
    for user in users:
        if user["id"] == int (id):
            return user
        
    return None

@app.route("/users/<userId>")
def getSingleUser(userId: str):
    isActive = request.args.get("isActive")

    for user in users:
        if user["id"] != int(userId):
            continue

        if isActive == None:
             return jsonify(user), 200
        
        if user["isActive"] == booleanMap[isActive]:
            return user, 200
        
    
    return "user not found", 404

@app.route("/users", methods=["POST"])
def addUser():
    user = request.get_json()
    userId = user["id"]

    foundUser = findUserById(userId)
    print(foundUser)
    if foundUser != None:
        return f"user with the id {userId} already exits", 409
    
    users.append(user)

    return jsonify(user), 201

@app.route("/users/<userId>", methods=["PUT"])
def updateUser(userId):
    user = request.get_json()
    userId = user["id"]

    foundUser = findUserById(userId)

    if foundUser == None:
        return "user not found", 404
    
    for userItem in users:
        if userItem["id"] == int(userId):
            userItem.update(user)

    return f"user with id {userId} updated", 200

@app.route("/users/<userId>", methods=["DELETE"])
def removeUser(userId):
    global users
    foundUser = findUserById(userId)

    if foundUser == None:
        return "user not found", 404


    filteredUsers = list(filter((lambda user: user["id"] != int(userId)), users))
    
    users = filteredUsers

    return users, 200


if __name__ == "__main__":
    app.run(debug = True)