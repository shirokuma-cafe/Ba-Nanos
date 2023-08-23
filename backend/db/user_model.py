from hashlib import md5
from pymongo.collection import Collection
from flask import jsonify, Response

def create_user(username: str, password: str, collection):

    # Create and add salt to password
    SALT = "Bananas-foodwards"
    salted_pass = password+SALT

    hashed_pw = md5(salted_pass.encode())
    print(hashed_pw.hexdigest())

    users_collecion: Collection = collection
    try:
        if users_collecion.find_one({"username": username}) is not None:
            return Response(
                f"username {username} is already registered, try a different username",
                400
            )

        users_collecion.insert_one({
            "username": username,
            "password": hashed_pw.hexdigest(),
        })

        return jsonify({
            "message": f"Successfuly created user: {username}",
        })
    except Exception as e:
        print(e)
